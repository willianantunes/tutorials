import React, { createContext, useContext, useEffect, useState } from "react"
import { UnleashClient } from "unleash-proxy-client"

const UnleashContext = createContext(null)

/**
 * @param onConfigurationUpdate {Function}
 * @returns {UnleashClient || null}
 */
const useUnleash = (onConfigurationUpdate = null) => {
  const unleash = useContext(UnleashContext)
  useEffect(() => {
    if (unleash && onConfigurationUpdate) {
      unleash.on("update", () => onConfigurationUpdate(unleash))
    }
  }, [onConfigurationUpdate, unleash])

  return unleash
}

const UnleashProvider = ({ children }) => {
  const [unleash, setUnleash] = useState(null)

  useEffect(() => {
    const unleashClient = new UnleashClient({
      url: process.env.NEXT_PUBLIC_UNLEASH_FRONTEND_API_URL,
      clientKey: process.env.NEXT_PUBLIC_UNLEASH_FRONTEND_API_TOKEN,
      appName: process.env.NEXT_PUBLIC_UNLEASH_APP_NAME,
    })
    unleashClient.on("initialized", () => {
      setUnleash(unleashClient)
    })
    // Start the background polling
    unleashClient.start()
    return () => {
      // It's a cleanup function, which is part of the useEffect hook!
      // It is called when the component using the UnleashProvider unmounts.
      unleashClient.stop()
    }
  }, [])

  return <UnleashContext.Provider value={unleash}>{children}</UnleashContext.Provider>
}

export { UnleashProvider, useUnleash }
