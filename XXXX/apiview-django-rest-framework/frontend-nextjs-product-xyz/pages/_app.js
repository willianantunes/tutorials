import React, { useEffect } from "react"
import "bootstrap/dist/css/bootstrap.css"
import Router from "next/router"
import { Auth0Provider } from "@auth0/auth0-react"
import {
  NEXT_PUBLIC_IDP_BACKEND_USER_MANAGEMENT_AUDIENCE,
  NEXT_PUBLIC_IDP_CLIENT_ID,
  NEXT_PUBLIC_IDP_CLIENT_REDIRECT_URI,
  NEXT_PUBLIC_IDP_DOMAIN,
} from "./configs/settings"

const onRedirectCallback = appState => {
  Router.replace(appState?.returnTo || "/")
}

function MyApp({ Component, pageProps }) {
  useEffect(() => {
    import("bootstrap/dist/js/bootstrap")
  }, [])

  useEffect(() => {
    typeof document !== undefined ? require("bootstrap/dist/js/bootstrap") : null
  }, [])

  const auth0Props = {
    domain: NEXT_PUBLIC_IDP_DOMAIN,
    clientId: NEXT_PUBLIC_IDP_CLIENT_ID,
    redirectUri: NEXT_PUBLIC_IDP_CLIENT_REDIRECT_URI,
    onRedirectCallback: onRedirectCallback,
    useRefreshTokens: true,
    // Only made for testing purposes 😁
    audience: `https://${NEXT_PUBLIC_IDP_DOMAIN}/api/v2/`,
    // https://auth0.com/docs/secure/tokens/access-tokens/get-management-api-tokens-for-single-page-applications#available-scopes-and-endpoints
    scope: "openid email profile read:current_user update:current_user_identities",
  }

  return (
    <Auth0Provider {...auth0Props}>
      <Component {...pageProps} />
    </Auth0Provider>
  )
}

export default MyApp
