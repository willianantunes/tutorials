import { Alert, Button, Container, Row, Stack } from "react-bootstrap"
import React, { useState } from "react"

const SocialLogins = ({ auth0 }) => {
  // States
  const initialSocialLoginState = {
    errorMessage: "",
    showError: false,
  }
  const [socialLoginState, setSocialLoginState] = useState(initialSocialLoginState)
  // Variables
  const connectionNameForGoogle = "google-oauth2"
  const connectionNameForFacebook = "facebook"
  // Handlers
  const handleCallbackFromAuth0 = error => {
    if (error) {
      console.log(`Received error: ${JSON.stringify(error)}`)
      let message = error.policy || error.description
      setSocialLoginState({ showError: true, errorMessage: message })
    }
  }
  // Events
  const initializeLoginWithGoogle = () => {
    console.log("Log in with Google")
    const options = {
      connection: connectionNameForGoogle,
    }
    auth0.authorize(options, handleCallbackFromAuth0)
  }
  const initializeLoginWithFacebook = () => {
    console.log("Log in with Facebook")
    const options = {
      connection: connectionNameForFacebook,
    }
    auth0.authorize(options, handleCallbackFromAuth0)
  }

  return (
    <Stack gap={3}>
      {socialLoginState.showError && <Alert variant="danger">{socialLoginState.errorMessage}</Alert>}
      <Button variant="danger" onClick={initializeLoginWithGoogle}>
        <i className="bi bi-google" /> Entrar com o Google
      </Button>
      <Button variant="primary" onClick={initializeLoginWithFacebook}>
        <i className="bi bi-facebook" /> Entrar com o Facebook
      </Button>
    </Stack>
  )
}

export default SocialLogins
