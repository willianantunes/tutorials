/**
* Handler that will be called during the execution of a PostLogin flow.
*
* @param {Event} event - Details about the user and the context in which they are logging in.
* @param {PostLoginAPI} api - Interface whose methods can be used to change the behavior of the login.
*/
exports.onExecutePostLogin = async (event, api) => {
  // Collecting secrets
  const tenant = event.secrets.TENANT
  const audience = event.secrets.AUDIENCE
  const clientId = event.secrets.APP_CLIENT_ID
  const clientSecret = event.secrets.APP_CLIENT_SECRET
  // Creating management API
  const ManagementClient = require("auth0").ManagementClient
  const managementClient = new ManagementClient({
    domain: tenant,
    scope: "read:users",
    clientId,
    clientSecret,
    audience,
  })
  // Main routine
  const userId = event.user.user_id
  const user = await managementClient.getUser({ id: userId })
  const shouldEnrichJWTWithGroups = user.hasOwnProperty("groups")
  if (shouldEnrichJWTWithGroups) {
    const claimKey = "https://www.willianantunes.com/ad/groups"
    const claimValue = user.groups
    api.idToken.setCustomClaim(claimKey, claimValue)
  }
}
