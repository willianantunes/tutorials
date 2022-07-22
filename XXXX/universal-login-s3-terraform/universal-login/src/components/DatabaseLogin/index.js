import React, { useState } from "react"
import { Alert, Button, Form } from "react-bootstrap"

const DatabaseLogin = ({ auth0, changePasswordHook }) => {
  // Variables
  const databaseConnectionName = "Username-Password-Authentication"
  // States
  const initialFormState = {
    username: "",
    password: "",
    signInFieldValue: "Continuar",
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
  const submitDatabaseLogin = event => {
    event.preventDefault()
    console.log("Initializing database login flow")
    setFormState(prevState => ({
      ...prevState,
      sending: true,
      signInFieldValue: "Autenticando ⏳",
      showError: false,
      errorMessage: "",
    }))
    const options = {
      realm: databaseConnectionName,
      username: formState.username,
      password: formState.password,
    }
    const callback = error => {
      if (error) {
        console.error(`Received error: ${JSON.stringify(error)}`)
        let message = error.description
        if (error.original.error_description === "Wrong email or password.") {
          message = "Acesso negado: Senha inválida."
        }
        setFormState(prevState => ({
          ...prevState,
          sending: false,
          signInFieldValue: "Continuar",
          showError: true,
          errorMessage: message,
        }))
      }
    }
    // https://auth0.com/docs/libraries/auth0js#webauth-login-
    auth0.login(options, callback)
  }
  const forgotPassword = event => {
    event.preventDefault()
    changePasswordHook()
  }

  return (
    <Form onSubmit={submitDatabaseLogin}>
      {formState.showError && <Alert variant="danger">{formState.errorMessage}</Alert>}
      <Form.Group className="mb-3" controlId="formBasicEmailOrUsername">
        <Form.Label>E-mail ou CPF</Form.Label>
        <Form.Control placeholder="Digite aqui ✍" value={formState.username} onChange={handleChange} name="username" />
      </Form.Group>
      <Form.Group className="mb-3" controlId="formBasicPassword">
        <Form.Label>Sua senha</Form.Label>
        <Form.Control type="password" value={formState.password} onChange={handleChange} name="password" />
        <a href="#" className="text-muted" onClick={forgotPassword}>
          Esqueci minha senha
        </a>
      </Form.Group>
      <Button variant="primary" disabled={formState.sending} type="submit">
        {formState.signInFieldValue}
      </Button>
    </Form>
  )
}

export default DatabaseLogin
