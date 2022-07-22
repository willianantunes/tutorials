import { Alert, Button, Form } from "react-bootstrap"
import React, { useState } from "react"

const SignUp = ({ auth0 }) => {
  // Variables
  const databaseConnectionName = "Username-Password-Authentication"
  // States
  const initialFormState = {
    username: "",
    email: "",
    password: "",
    signUpFieldValue: "Continuar",
    sending: false,
    // Messages that we can show
    errorMessage: "",
    showError: false,
  }
  const [formState, setFormState] = useState(initialFormState)
  // Events
  const handleChange = e => {
    const { name, value } = e.target
    setFormState(prevState => ({ ...prevState, [name]: value }))
  }
  const submitSignUp = event => {
    event.preventDefault()
    console.log("Initializing sign-up flow")
    const options = {
      connection: databaseConnectionName,
      email: formState.email,
      username: formState.username,
      password: formState.password,
      user_metadata: { whereTheRegistrationHappened: "EVENT-UNIVERSAL-LOGIN" },
    }
    setFormState(prevState => ({
      ...prevState,
      sending: true,
      signUpFieldValue: "Registrando ⏳",
      showError: false,
      errorMessage: "",
    }))
    // Read below why this is required
    let loginPhase = false
    const callback = error => {
      if (error) {
        console.error(`Received error: ${JSON.stringify(error)}`)
        let message = error.description
        setFormState(prevState => ({
          ...prevState,
          sending: false,
          signUpFieldValue: "Continuar",
          showError: true,
          errorMessage: message,
        }))
      } else if (loginPhase === false) {
        // This signup does not sign in the user, then either we ask the user to authenticate or do a gambiarra :)
        const options = {
          realm: databaseConnectionName,
          username: formState.username,
          password: formState.password,
        }
        loginPhase = true
        auth0.login(options, callback)
      }
    }
    // https://auth0.com/docs/libraries/auth0js#signup
    auth0.signup(options, callback)
  }

  return (
    <Form onSubmit={submitSignUp}>
      {formState.showError && <Alert variant="danger">{formState.errorMessage}</Alert>}
      <Form.Group className="mb-3" controlId="formBasicEmail">
        <Form.Label>E-mail</Form.Label>
        <Form.Control
          placeholder="Digite aqui seu e-mail ✍"
          value={formState.email}
          onChange={handleChange}
          name="email"
          type="email"
          disabled={formState.sending}
        />
      </Form.Group>
      <Form.Group className="mb-3" controlId="formBasicUsername">
        <Form.Label>CPF</Form.Label>
        <Form.Control
          placeholder="Digite aqui seu CPF ✍"
          value={formState.username}
          onChange={handleChange}
          name="username"
          disabled={formState.sending}
        />
      </Form.Group>
      <Form.Group className="mb-3" controlId="formBasicPassword">
        <Form.Label>Sua senha</Form.Label>
        <Form.Control
          type="password"
          value={formState.password}
          onChange={handleChange}
          name="password"
          disabled={formState.sending}
        />
      </Form.Group>
      <Button variant="primary" disabled={formState.sending} type="submit">
        {formState.signUpFieldValue}
      </Button>
    </Form>
  )
}

export default SignUp
