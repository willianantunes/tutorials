import React, { useState } from "react"
import Layout from "./components/Layout"
import { Alert, Button, Form } from "react-bootstrap"

export default function Profile() {
  // States
  const [formState, setFormState] = useState({
    email: "",
    full_name: "",
    saveButtonValue: "Persist data",
    errorMessage: "",
    loadingMessage: "",
    showError: false,
    sending: false,
  })
  // Events
  const handleChange = e => {
    const { name, value } = e.target
    setFormState(prevState => ({ ...prevState, [name]: value }))
  }
  const submitUpdateAttributesHandler = async e => {
    e.preventDefault()
    alert(`We have: ${JSON.stringify(formState)}`)
  }
  return (
    <Layout>
      <p>
        Your data: <br />
        <br /> {JSON.stringify(formState)}
      </p>
      <hr />
      <Form onSubmit={submitUpdateAttributesHandler}>
        {formState.showError && <Alert variant="danger">{formState.errorMessage}</Alert>}
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Full name</Form.Label>
          <Form.Control
            value={formState.full_name}
            onChange={handleChange}
            name="full_name"
            type="text"
            disabled={formState.sending}
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>E-mail</Form.Label>
          <Form.Control value={formState.email} onChange={handleChange} name="email" type="text" disabled={formState.sending} />
        </Form.Group>
        <Form.Group className="mb-3">
          <Button variant="primary" disabled={formState.sending} type="submit">
            {formState.saveButtonValue}
          </Button>
        </Form.Group>
      </Form>
    </Layout>
  )
}
