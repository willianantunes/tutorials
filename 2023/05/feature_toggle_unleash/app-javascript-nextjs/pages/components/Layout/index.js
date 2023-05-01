import React, { useEffect } from "react"
import Header from "../Header"
import Footer from "../Footer"
import { useUserAgent } from "../../hooks/user_agent"
import { useUnleash } from "../../contexts/feature-management"

const Layout = ({ children }) => {
  const userAgent = useUserAgent()
  const client = useUnleash()
  useEffect(() => {
    if (userAgent && client) {
      // Let's mock the user ID!
      const userIdPersonalComputer = "40956364-e486-4d8e-b35e-60660721f467"
      const userIdMobile = "d821cbc0-2e4d-49fc-a5b4-990eb991beec"
      const userId = userAgent.device.isMobile ? userIdMobile : userIdPersonalComputer
      client.updateContext({ userId: userId })
    }
  }, [userAgent, client])

  return (
    <div className="container py-3">
      <Header />

      <main>{children}</main>

      <Footer />
    </div>
  )
}

export default Layout
