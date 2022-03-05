import React from "react"
import { useAuth0 } from "@auth0/auth0-react"
import Link from "next/link"

const Header = () => {
  const { isAuthenticated, loginWithRedirect, logout } = useAuth0()
  // Events
  const logoutHandler = e => {
    e.preventDefault()
    logout({ returnTo: window.location.origin })
  }
  const loginHandler = async e => {
    e.preventDefault()
    await loginWithRedirect()
  }
  // Custom components
  const Options = () => {
    if (isAuthenticated) {
      return (
        <>
          <Link href="/profile">
            <a className="me-3 py-2 text-dark text-decoration-none">Profile</a>
          </Link>
          <Link href="/claims-access-token">
            <a className="me-3 py-2 text-dark text-decoration-none">Claims Access Token</a>
          </Link>
          <Link href="/claims-id-token">
            <a className="me-3 py-2 text-dark text-decoration-none">Claims ID Token</a>
          </Link>
          <a href="#" onClick={logoutHandler} className="me-3 py-2 text-dark text-decoration-none">
            Logout
          </a>
        </>
      )
    } else {
      return (
        <a href="#" onClick={loginHandler} className="me-3 py-2 text-dark text-decoration-none">
          Log in
        </a>
      )
    }
  }

  return (
    <header>
      <div className="d-flex flex-column flex-md-row align-items-center pb-3 mb-4 border-bottom">
        <Link href="/">
          <a href="#" className="d-flex align-items-center text-dark text-decoration-none">
            <span className="fs-4">Product XYZ</span>
          </a>
        </Link>
        <nav className="d-inline-flex mt-2 mt-md-0 ms-md-auto">
          <Options />
        </nav>
      </div>
    </header>
  )
}

export default Header
