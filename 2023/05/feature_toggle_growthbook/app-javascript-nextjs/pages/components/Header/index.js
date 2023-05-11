import React, { useEffect, useState } from "react"
import Link from "next/link"
import { useGrowthBook } from "@growthbook/growthbook-react"

const Header = () => {
  // States
  const [gameSharkMode, setGameSharkMode] = useState(false)
  const [easterEggDisplay, setEasterEggDisplay] = useState("none")
  // Feature toggle
  const client = useGrowthBook()
  useEffect(() => {
    if (client) {
      setGameSharkMode(client.isOn("GAME_SHARK_MODE".toLowerCase()))
      setEasterEggDisplay(client.isOn("SHOW_EASTER_EGG".toLowerCase()) ? "inline" : "none")
    }
  }, [client])
  const projectTitle = gameSharkMode ? `Product QWERTY - GAME SHARK MODE` : `Product QWERTY`
  const easterEggTag = <span style={{ display: easterEggDisplay }}>👃</span>

  return (
    <header>
      <div className="d-flex flex-column flex-md-row align-items-center pb-3 mb-4 border-bottom">
        <Link href="/">
          <a href="#" className="d-flex align-items-center text-dark text-decoration-none">
            <span className="fs-4">
              {projectTitle} {easterEggTag}
            </span>
          </a>
        </Link>
        <nav className="d-inline-flex mt-2 mt-md-0 ms-md-auto">
          <Link href="/profile">
            <a className="me-3 py-2 text-dark text-decoration-none">Mocked profile</a>
          </Link>
          <Link href="/claims">
            <a className="me-3 py-2 text-dark text-decoration-none">Mocked claims</a>
          </Link>
          <a
            href="https://github.com/growthbook/growthbook/tree/f3cd36de1915ec97f16c69d775b30e121356095a/packages/sdk-js"
            target="_blank"
            rel="noreferrer"
            className="me-3 py-2 text-dark text-decoration-none"
          >
            Know the truth
          </a>
        </nav>
      </div>
    </header>
  )
}

export default Header
