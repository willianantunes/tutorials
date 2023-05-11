import React, { useEffect } from "react"
import "bootstrap/dist/css/bootstrap.css"
import { FeaturesReady, GrowthBook, GrowthBookProvider } from "@growthbook/growthbook-react"
import { useUserAgent } from "./hooks/user_agent"
import { uuidv4 } from "./support/data-provider"
import LoadingFeatures from "./components/LoadingFeatures"
import { useRouter } from "next/router"

const gb = new GrowthBook({
  apiHost: process.env.NEXT_PUBLIC_GROWTHBOOK_API_HOST,
  clientKey: process.env.NEXT_PUBLIC_GROWTHBOOK_CLIENT_KEY,
  enableDevMode: true,
})

function MyApp({ Component, pageProps }) {
  const router = useRouter()
  const userAgent = useUserAgent()

  useEffect(() => {
    const handleRouteChangeStart = url => gb.setURL(url)
    router.events.on("routeChangeStart", handleRouteChangeStart)
    return () => {
      router.events.off("routeChangeStart", handleRouteChangeStart)
    }
  }, [router])

  useEffect(() => {
    import("bootstrap/dist/js/bootstrap")
    // You must use gb.refreshFeatures() if you want to refresh the features!
    gb.loadFeatures({ autoRefresh: true }).then(() => console.log("Features have been loaded"))
  }, [])

  useEffect(() => {
    if (typeof document !== undefined) {
      require("bootstrap/dist/js/bootstrap")
    }
  }, [])

  useEffect(() => {
    if (userAgent) {
      const userIdPersonalComputer = "40956364-e486-4d8e-b35e-60660721f467"
      const userIdMobile = "d821cbc0-2e4d-49fc-a5b4-990eb991beec"
      let userId = userAgent.device.isMobile ? userIdMobile : userIdPersonalComputer
      const browser = userAgent.browser.name.toLowerCase()
      if (browser === "firefox") {
        // Just to mimic random users as there is no such option on GrowthBook
        userId = uuidv4()
      }
      gb.setAttributes({
        userId: userId,
        browser: browser,
      })
    }
  }, [userAgent])

  return (
    <FeaturesReady timeout={2000} fallback={<LoadingFeatures />}>
      <GrowthBookProvider growthbook={gb}>
        <Component {...pageProps} />
      </GrowthBookProvider>
    </FeaturesReady>
  )
}

export default MyApp
