import React, { useState } from "react"
import { Alert, Button, Form } from "react-bootstrap"
import OneTimePasswordLoginLastStep from "../OneTimePasswordLoginLastStep"

const OneTimePasswordLogin = ({ auth0 }) => {
  // Auth0 stuff
  const connectionName = "email"
  // States
  const initialFormState = {
    email: "",
    sending: false,
    // When first step concludes
    firstStepConcluded: false,
    transactionId: null,
    // When the last step goes wrong
    startAgain: false,
    whyShouldStartAgain: "",
    // Messages that we can show
    errorMessage: "",
    loadingMessage: "",
    showError: false,
  }
  const [formState, setFormState] = useState(initialFormState)
  // Events
  const endFlowInformingError = message => {
    setFormState(prevState => ({ ...prevState, startAgain: true, whyShouldStartAgain: message }))
  }
  const handleChange = e => {
    const { name, value } = e.target
    setFormState(prevState => ({ ...prevState, [name]: value }))
  }
  const submitEmailLogin = event => {
    event.preventDefault()
    console.log("Initializing passwordless with email flow")
    const providedEmail = formState.email
    const options = {
      connection: connectionName,
      send: "code",
      email: providedEmail,
    }
    setFormState(prevState => ({
      ...prevState,
      sending: true,
      loadingMessage: `Enviando código temporário para ${providedEmail} ⏳`,
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
        }))
      } else if (response) {
        console.log(`Received response: ${JSON.stringify(response)}`)
        const transactionId = response.Id
        setFormState(prevState => ({
          ...prevState,
          sending: false,
          loadingMessage: "",
          firstStepConcluded: true,
          transactionId,
        }))
      }
    }
    // https://auth0.com/docs/libraries/auth0js#start-passwordless-authentication
    auth0.passwordlessStart(options, callback)
  }
  const submitStartAgain = event => {
    event.preventDefault()
    console.log("Starting again passwordless flow")
    setFormState(initialFormState)
  }

  if (formState.startAgain) {
    return (
      <Form onSubmit={submitStartAgain}>
        <Alert variant="danger">{formState.whyShouldStartAgain}</Alert>
        <Button variant="primary" type="submit">
          Tentar de novo
        </Button>
      </Form>
    )
  }
  if (formState.firstStepConcluded) {
    return (
      <OneTimePasswordLoginLastStep
        auth0={auth0}
        connectionName={connectionName}
        email={formState.email}
        transactionId={formState.transactionId}
        endFlowInformingErrorHook={endFlowInformingError}
      />
    )
  } else {
    return (
      <Form onSubmit={submitEmailLogin}>
        {formState.showError && <Alert variant="danger">{formState.errorMessage}</Alert>}
        {(() => {
          if (formState.sending) {
            return <Alert variant="primary">{formState.loadingMessage}</Alert>
          } else {
            return (
              <>
                <Form.Group className="mb-3" controlId="formBasicEmailOrUsername">
                  <Form.Label>Endereço de e-mail</Form.Label>
                  <Form.Control
                    type="email"
                    placeholder="Digite aqui ✍"
                    value={formState.email}
                    onChange={handleChange}
                    name="email"
                  />
                </Form.Group>
                <Button variant="primary" disabled={formState.sending} type="submit">
                  Enviar código temporário 📩
                </Button>
              </>
            )
          }
        })()}
      </Form>
    )
  }
}

export default OneTimePasswordLogin
