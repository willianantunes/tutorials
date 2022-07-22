import { useEffect } from "react"
import Layout from "../components/Layout"
import UniversalLogin from "../components/UniversalLogin"

export default function Home() {
  useEffect(() => {
    const bodyElement = document.querySelector("body")
    bodyElement.style.backgroundColor = "#adb5bd"
  })

  return (
    <Layout>
      <UniversalLogin />
    </Layout>
  )
}
