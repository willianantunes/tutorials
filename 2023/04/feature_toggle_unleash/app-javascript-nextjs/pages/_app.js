import React, { useEffect } from "react"
import "bootstrap/dist/css/bootstrap.css"
import { UnleashProvider } from "./contexts/feature-management"

function MyApp({ Component, pageProps }) {
  useEffect(() => {
    import("bootstrap/dist/js/bootstrap")
  }, [])

  useEffect(() => {
    typeof document !== undefined ? require("bootstrap/dist/js/bootstrap") : null
  }, [])

  return (
    <UnleashProvider>
      <Component {...pageProps} />
    </UnleashProvider>
  )
}

export default MyApp
