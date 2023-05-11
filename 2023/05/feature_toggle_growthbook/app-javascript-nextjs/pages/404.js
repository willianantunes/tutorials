import Layout from "./components/Layout"
import React from "react"
import Link from "next/link"

export default function Custom404() {
  return (
    <Layout>
      <div className="pricing-header p-3 pb-md-4 mx-auto text-center">
        <h1 className="display-4 fw-normal">
          Page not found{" "}
          <span role="img" aria-label="Thinking face">
            🤔
          </span>
        </h1>
        <p className="fs-5 text-muted">
          But here’s something you can always find — <Link href="/">our home page</Link>
        </p>
      </div>
    </Layout>
  )
}
