import React from "react"
import { useAuth0 } from "@auth0/auth0-react"
import Layout from "./components/Layout"

export default function Home() {
  const { user, isAuthenticated } = useAuth0()

  return (
    <Layout>
      {isAuthenticated && (
        <div className="pricing-header p-3 pb-md-4 mx-auto text-center">
          <h1 className="display-4 fw-normal">Now we know 😋</h1>
          <p className="fs-5 text-muted">
            <strong>
              {user.name} / {user.email}
            </strong>
          </p>
        </div>
      )}
      {!isAuthenticated && (
        <div className="pricing-header p-3 pb-md-4 mx-auto text-center">
          <h1 className="display-4 fw-normal">We don't know who you are 🥲</h1>
          <p className="fs-5 text-muted">Authenticate yourself and check your profile!!</p>
        </div>
      )}
    </Layout>
  )
}
