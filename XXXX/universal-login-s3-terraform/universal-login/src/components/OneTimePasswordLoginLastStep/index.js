import React, { useState } from "react"
import { Alert, Button, Form } from "react-bootstrap"

const OneTimePasswordLoginLastStep = ({ auth0, email, transactionId, connectionName, endFlowInformingErrorHook }) => {
  // States
  const initialFormState = {
    code: "",
    sending: false,
    signInFieldValue: "Submeter código",
    // Messages that we can show
    errorMessage: "",
    loadingMessage: "",
    showError: false,
  }
  const [formState, setFormState] = useState(initialFormState)
  // Events
  const handleChange = e => {
    const { name, value } = e.target
    setFormState(prevState => ({ ...prevState, [name]: value }))
  }
  const submitPasswordlessLogin = event => {
    event.preventDefault()
    console.log("Finalizing passwordless with email flow")
    setFormState(prevState => ({
      ...prevState,
      sending: true,
      signInFieldValue: `Autenticando ⏳`,
      showError: false,
      errorMessage: "",
    }))
    const options = {
      connection: connectionName,
      email,
      verificationCode: formState.code,
    }
    const callback = (error, response) => {
      if (error) {
        console.error(`Received error: ${JSON.stringify(error)}`)
        let message = error.description
        if (message === "Wrong email or verification code.") {
          message = "E-mail ou código inválido."
        } else if (message === "The verification code has expired. Please try to login again.") {
          message = "O código de verificação expirou. Por favor tente de novo."
        }
        endFlowInformingErrorHook(message)
      }
    }
    // In order to simulate an action
    // https://auth0.com/docs/libraries/auth0js#complete-passwordless-authentication
    auth0.passwordlessLogin(options, callback)
  }

  return (
    <Form onSubmit={submitPasswordlessLogin}>
      {formState.showError && <Alert variant="danger">{formState.errorMessage}</Alert>}
      <Alert variant="success">
        Verifique sua caixa postal! O código expira em 10 minutos e só pode ser usado uma única vez.
      </Alert>
      <Form.Group className="mb-3" controlId="formBasicEmailOrUsername">
        <Form.Label>Código temporário de 6 dígitos</Form.Label>
        <Form.Control
          type="number"
          disabled={formState.sending}
          placeholder="Exemplo: 123456"
          value={formState.code}
          onChange={handleChange}
          name="code"
        />
      </Form.Group>
      <Alert variant="secondary">Não recebeu o e-mail? Veja sua caixa de spam</Alert>
      <Button variant="primary" disabled={formState.sending} type="submit">
        {formState.signInFieldValue}
      </Button>
    </Form>
  )
}

export default OneTimePasswordLoginLastStep
