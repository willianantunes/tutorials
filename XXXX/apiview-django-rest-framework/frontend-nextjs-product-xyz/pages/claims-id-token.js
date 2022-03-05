import React from "react"
import { useAuth0, withAuthenticationRequired } from "@auth0/auth0-react"
import Layout from "./components/Layout"
import { useCallback, useEffect, useState } from "react"
import Table from "./components/Table"
import { useRouter } from "next/router"
import NotAuthenticated from "./components/NotAuthenticated"

const ClaimsIdToken = () => {
  const { getIdTokenClaims } = useAuth0()
  const [claims, setClaims] = useState(null)
  // Hooks
  const retrieveMyClaims = useCallback(async () => {
    const claims = await getIdTokenClaims()
    setClaims(claims)
  }, [])
  useEffect(() => {
    retrieveMyClaims()
  }, [retrieveMyClaims])

  return (
    <Layout>
      <div className="row">
        <div className="col-md-12">
          <h1 className="display-9 fw-normal text-center">See which data is bound to your token</h1>
          <p>
            Technically speaking, this page shows all claims associated with your <strong>ID Token</strong>. This is quite
            helpful for debugging purposes.
          </p>
          <Table keyValueObject={claims} />
        </div>
      </div>
    </Layout>
  )
}

// https://auth0.github.io/auth0-react/modules/with_authentication_required.html
// https://auth0.github.io/auth0-react/interfaces/with_authentication_required.withauthenticationrequiredoptions.html
export default withAuthenticationRequired(ClaimsIdToken, {
  onRedirecting: () => <NotAuthenticated />,
  returnTo: () => window.location.href,
})
