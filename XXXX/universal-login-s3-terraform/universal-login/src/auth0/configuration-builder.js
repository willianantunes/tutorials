export function buildConfigurationFromEnvironmentToAuth0js() {
  const isOnClientSide = typeof window !== "undefined"

  if (isOnClientSide && window.paramsFromProvider) return window.paramsFromProvider

  // In order to get this sample, I've just initiated an authorization code grant type from my App to Universal Login
  return {
    language: "pt-br",
    overrides: { __tenant: "antunes", __token_issuer: "https://login.willianantunes.com/" },
    domain: "login.willianantunes.com",
    clientID: "LnqZXPprrsDaxEYbWfXpPJEmbtuc1F4E",
    redirectUri: "http://app.local:8000/api/v1/response-oidc",
    responseType: "code",
    protocol: "oauth2",
    response_type: "code",
    scope: "openid profile email",
    plugins: { plugins: [] },
    _sendTelemetry: true,
    _timesToRetryFailedRequests: 0,
    tenant: "antunes",
    token_issuer: "https://login.willianantunes.com/",
    rootUrl: "https://login.willianantunes.com",
    universalLoginPage: true,
  }
}
