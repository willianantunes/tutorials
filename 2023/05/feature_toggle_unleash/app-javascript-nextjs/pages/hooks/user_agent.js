import React, { useMemo, useState } from "react"
import { UAParser } from "ua-parser-js"

export function useUserAgent() {
  const [userAgent, setUserAgent] = useState(null)

  useMemo(() => {
    if (typeof window !== "undefined") {
      const currentUserAgent = window.navigator.userAgent
      const userAgentParser = new UAParser(currentUserAgent)
      const { browser, cpu, device } = userAgentParser.getResult()
      device["isMobile"] = device.hasOwnProperty("type") && device.type === "mobile"
      setUserAgent({
        browser,
        cpu,
        device,
      })
    }
  }, [])

  return userAgent
}
