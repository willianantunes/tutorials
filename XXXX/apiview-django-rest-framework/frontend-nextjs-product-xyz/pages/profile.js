import React, { useEffect, useState } from "react"
import { useAuth0, withAuthenticationRequired } from "@auth0/auth0-react"
import Layout from "./components/Layout"
import NotAuthenticated from "./components/NotAuthenticated"
import { retrieveUserAttributes, updateUserAttributes } from "./providers/user-management"
import { Alert, Button, Form } from "react-bootstrap"
import { removeEmptyKeys } from "./utils/objects"
import { NEXT_PUBLIC_IDP_BACKEND_USER_MANAGEMENT_AUDIENCE } from "./configs/settings"

const Claims = () => {
  const audience = NEXT_PUBLIC_IDP_BACKEND_USER_MANAGEMENT_AUDIENCE
  // States
  const { getAccessTokenSilently } = useAuth0()
  const [accessToken, setAccessToken] = useState(null)
  const initialFormState = {
    name: "",
    given_name: "",
    family_name: "",
    user_metadata: null,
    // Messages that we can show
    saveButtonValue: "Update",
    sending: false,
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
  const submitUpdateAttributesHandler = async e => {
    e.preventDefault()
    setFormState(prevState => ({
      ...prevState,
      sending: true,
      saveButtonValue: "Updating ⏳",
      showError: false,
      errorMessage: "",
    }))
    const attributes = {
      name: formState.name,
      given_name: formState.given_name,
      family_name: formState.family_name,
    }
    const cleanedAttributes = removeEmptyKeys(attributes)
    try {
      await updateUserAttributes(accessToken, cleanedAttributes)
      setFormState(prevState => ({
        ...prevState,
        sending: false,
        saveButtonValue: initialFormState.saveButtonValue,
        showError: false,
        errorMessage: "",
      }))
    } catch (e) {
      console.log(e)
      setFormState(prevState => ({
        ...prevState,
        sending: false,
        saveButtonValue: initialFormState.saveButtonValue,
        showError: true,
        errorMessage: `You get the follwing: ${JSON.stringify(e)}`,
      }))
    }
  }
  // Hooks
  useEffect(() => {
    async function retrieveMyProperties() {
      const token = await getAccessTokenSilently({ audience })
      setAccessToken(token)
      try {
        const userAttributes = await retrieveUserAttributes(token)
        setFormState(prevState => ({
          ...prevState,
          name: userAttributes.name,
          given_name: userAttributes.given_name,
          family_name: userAttributes.family_name,
          user_metadata: userAttributes.user_metadata,
        }))
      } catch (e) {
        const errorDetails = e.message
        setFormState(prevState => ({
          ...prevState,
          sending: true,
          saveButtonValue: initialFormState.saveButtonValue,
          showError: true,
          errorMessage: `An error has been caught: ${errorDetails}.`,
        }))
      }
    }
    retrieveMyProperties()
  }, [getAccessTokenSilently])

  return (
    <Layout>
      {!accessToken && <p>Loading...</p>}
      {accessToken && (
        <>
          <Form onSubmit={submitUpdateAttributesHandler} style={{ paddingBottom: "16px" }}>
            {formState.showError && <Alert variant="danger">{formState.errorMessage}</Alert>}
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Name</Form.Label>
              <Form.Control
                value={formState.name}
                onChange={handleChange}
                name="name"
                type="text"
                disabled={formState.sending}
              />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Given name</Form.Label>
              <Form.Control
                value={formState.given_name}
                onChange={handleChange}
                name="given_name"
                type="text"
                disabled={formState.sending}
              />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Family name</Form.Label>
              <Form.Control
                value={formState.family_name}
                onChange={handleChange}
                name="family_name"
                type="text"
                disabled={formState.sending}
              />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>City</Form.Label>
              <Form.Control value={formState.user_metadata?.city} onChange={handleChange} type="text" disabled={true} />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>State or province</Form.Label>
              <Form.Control value={formState.user_metadata?.state} onChange={handleChange} type="text" disabled={true} />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Gender</Form.Label>
              <Form.Control value={formState.user_metadata?.gender} onChange={handleChange} type="text" disabled={true} />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Birthday</Form.Label>
              <Form.Control value={formState.user_metadata?.birthday} onChange={handleChange} type="text" disabled={true} />
            </Form.Group>
            <Button variant="primary" disabled={formState.sending} type="submit">
              {formState.saveButtonValue}
            </Button>
          </Form>
        </>
      )}
    </Layout>
  )
}

export default withAuthenticationRequired(Claims, {
  onRedirecting: () => <NotAuthenticated />,
  returnTo: () => window.location.href,
})
