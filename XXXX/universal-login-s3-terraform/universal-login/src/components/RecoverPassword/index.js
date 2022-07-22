import React, { useState } from "react"
import { Alert, Button, Form } from "react-bootstrap"

const RecoverPassword = ({ auth0 }) => {
  // Variables
  const databaseConnectionName = "Username-Password-Authentication"
  // States
  const initialFormState = {
    email: "",
    signInFieldValue: "Enviar e-mail",
    sending: false,
    // Messages that we can show
    errorMessage: "",
    showError: false,
    showSuccess: false,
  }
  const [formState, setFormState] = useState(initialFormState)
  // Events
  const handleChange = e => {
    const { name, value } = e.target
    setFormState(prevState => ({ ...prevState, [name]: value }))
  }
  const submitEmailRecoverPasswordFlow = event => {
    event.preventDefault()
    const options = {
      email: formState.email,
      connection: databaseConnectionName,
    }
    setFormState(prevState => ({
      ...prevState,
      sending: true,
      signInFieldValue: "Enviando ⏳",
      showError: false,
      errorMessage: "",
    }))
    const callback = (error, response) => {
      if (error) {
        console.error(`Received error: ${JSON.stringify(error)}`)
        let message = error.description
        setFormState(prevState => ({
          ...prevState,
          sending: false,
          showError: true,
          errorMessage: message,
          signInFieldValue: "Enviar e-mail",
        }))
      } else {
        console.log(`Received response: ${JSON.stringify(response)}`)
        setFormState(prevState => ({
          ...prevState,
          showSuccess: true,
        }))
      }
    }
    // https://auth0.github.io/auth0.js/WebAuth.html
    auth0.changePassword(options, callback)
  }
  return (
    <Form onSubmit={submitEmailRecoverPasswordFlow}>
      <h3 className="text-center">Resetar senha</h3>
      {(() => {
        if (formState.showSuccess) {
          return (
            <Alert variant="success">
              Verifique sua caixa postal! Enviamos um e-mail com os detalhes para resetar sua senha.
            </Alert>
          )
        } else {
          return (
            <>
              {formState.showError && <Alert variant="danger">{formState.errorMessage}</Alert>}
              <Form.Group className="mb-3" controlId="formBasicEmailOrUsername">
                <Form.Label>E-mail</Form.Label>
                <Form.Control
                  type="email"
                  placeholder="Digite aqui ✍"
                  value={formState.username}
                  onChange={handleChange}
                  name="email"
                />
              </Form.Group>
              <Button variant="primary" disabled={formState.sending} type="submit">
                {formState.signInFieldValue}
              </Button>
            </>
          )
        }
      })()}
    </Form>
  )
}

export default RecoverPassword
