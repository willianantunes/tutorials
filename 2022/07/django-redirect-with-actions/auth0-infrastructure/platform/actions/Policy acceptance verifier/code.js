const termsKey = "termsAcceptanceHistory"

/**
 * Handler that will be called during the execution of a PostLogin flow.
 *
 * @param {Event} event - Details about the user and the context in which they are logging in. {@link https://auth0.com/docs/customize/actions/flows-and-triggers/login-flow/event-object|Public documentation}.
 * @param {PostLoginAPI} api - Interface whose methods can be used to change the behavior of the login. {@link https://auth0.com/docs/customize/actions/flows-and-triggers/login-flow/api-object|Public documentation}.
 */
exports.onExecutePostLogin = async (event, api) => {
  // Properties from the event
  const clientIdApplicationTheUserLoggingInTo = event.client.client_id
  const userProperties = event.user
  const currentUserAppMetadata = userProperties.app_metadata
  const currentUserId = userProperties.user_id
  const currentTimestamp = event?.authentication?.methods[0]["timestamp"] || new Date().toISOString()
  // Let's verify if it's the first time the user is logging in!
  // By the way, you could verify if a new policy acceptance flow in indeed required after new logins.
  const isFirstLogin = !currentUserAppMetadata.hasOwnProperty(termsKey)
  if (isFirstLogin) {
    // Craft a signed session token so we can send it to our backend
    const customClaims = {
      id: currentUserId,
      app_metadata: currentUserAppMetadata,
      client_id: clientIdApplicationTheUserLoggingInTo,
      whenTheEventStarted: currentTimestamp,
    }
    const tenMinutes = 60 * 10
    const token = api.redirect.encodeToken({
      secret: event.secrets.THE_SECRET_USED_TO_CREATE_OPEN_AND_VALIDATE_THE_JWT,
      expiresInSeconds: tenMinutes,
      payload: customClaims,
    })
    // Initializing policy acceptance flow
    api.redirect.sendUserTo(event.secrets.BACKEND_DJANGO_ENDPOINT, {
      query: { session_token: token },
    })
  }
}

/**
 * Handler that will be invoked when this action is resuming after an external redirect. If your
 * onExecutePostLogin function does not perform a redirect, this function can be safely ignored.
 *
 * @param {Event} event - Details about the user and the context in which they are logging in. {@link https://auth0.com/docs/customize/actions/flows-and-triggers/login-flow/event-object|Public documentation}.
 * @param {PostLoginAPI} api - Interface whose methods can be used to change the behavior of the login. {@link https://auth0.com/docs/customize/actions/flows-and-triggers/login-flow/api-object|Public documentation}.
 */
exports.onContinuePostLogin = async (event, api) => {
  const queryStringWhereTheTokenIs = "data"
  const payload = api.redirect.validateToken({
    secret: event.secrets.THE_SECRET_USED_TO_CREATE_OPEN_AND_VALIDATE_THE_JWT,
    tokenParameterName: queryStringWhereTheTokenIs,
  })
  // Our backend will do the job for us, then we just need to update/create the claim
  api.user.setAppMetadata(termsKey, payload["other"][termsKey])
}
