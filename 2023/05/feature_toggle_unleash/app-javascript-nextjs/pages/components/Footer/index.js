import React from "react"

const Footer = () => {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="pt-4 pt-md-5 border-top">
      <div className="container">&copy; {currentYear} - Product QWERTY</div>
    </footer>
  )
}

export default Footer
