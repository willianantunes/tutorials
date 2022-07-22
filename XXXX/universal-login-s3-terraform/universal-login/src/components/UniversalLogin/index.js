import React, { useState } from "react"
import * as S from "./styled"
import { Button, Card, Container, Form } from "react-bootstrap"
import DatabaseLogin from "../DatabaseLogin"
import OneTimePasswordLogin from "../OneTimePasswordLogin"
// https://auth0.com/docs/libraries/auth0js
import { WebAuth } from "auth0-js"
import { buildConfigurationFromEnvironmentToAuth0js } from "../../auth0/configuration-builder"
import SocialLogins from "../SocialLogins"
import RecoverPassword from "../RecoverPassword"
import SignUp from "../SignUp"
import { ImageWrapper } from "./styled"

const UniversalLogin = () => {
  // Auth0
  const config = buildConfigurationFromEnvironmentToAuth0js()
  const webAuth = new WebAuth(config)
  // States
  const initialClassicUniversalLoginState = {
    signUpForm: false,
    showChangePasswordForm: false,
    oneTimePasswordEnabled: false,
    buttonLoginStrategyFieldValue: "Receber chave de acesso rápido por email",
  }
  const [classicUniversalLoginState, setClassicUniversalLoginState] = useState(initialClassicUniversalLoginState)
  // Events
  const authenticationMethodToggle = event => {
    if (classicUniversalLoginState.oneTimePasswordEnabled || classicUniversalLoginState.showChangePasswordForm) {
      setClassicUniversalLoginState(initialClassicUniversalLoginState)
    } else {
      setClassicUniversalLoginState(prevState => ({
        ...prevState,
        oneTimePasswordEnabled: !classicUniversalLoginState.oneTimePasswordEnabled,
        buttonLoginStrategyFieldValue: "Logar com senha",
      }))
    }
  }
  const refreshToChangePasswordForm = () => {
    console.log("Refreshing UI to change password form")
    setClassicUniversalLoginState(prevState => ({
      ...prevState,
      showChangePasswordForm: true,
      buttonLoginStrategyFieldValue: "Logar com senha",
    }))
  }
  const signUpToggle = event => {
    event.preventDefault()
    setClassicUniversalLoginState(prevState => ({
      ...prevState,
      signUpForm: !classicUniversalLoginState.signUpForm,
    }))
  }
  // UI handling
  const CompanyImage = () => {
    return (
      <S.ImageWrapper>
        <Card.Img variant="top" src="holder.js/100px180?text=XYZ company" />
      </S.ImageWrapper>
    )
  }
  const standardUi = innerForm => {
    return (
      <S.CustomCard>
        <CompanyImage />
        <Card.Body>
          <Card.Title>Bem-vindo</Card.Title>
          <Card.Text>
            Faça login na sua conta <strong>XYZ</strong> e continue em nosso site.
          </Card.Text>
          <Card.Text>
            Novo? Faça seu{" "}
            <a href="#" onClick={signUpToggle}>
              cadastro agora
            </a>
            .
          </Card.Text>
          <hr />
          {innerForm}
          <hr />
          <Button variant="outline-primary" onClick={authenticationMethodToggle}>
            {classicUniversalLoginState.buttonLoginStrategyFieldValue}
          </Button>
          <hr />
          <SocialLogins auth0={webAuth} />
        </Card.Body>
        <Card.Footer className="text-center">
          Ao fazer login, você concorda com nossa{" "}
          <a
            href="https://github.com/willianantunes/auth0-custom-universal-login-with-sample-app/blob/main/LICENSE"
            target="blank"
          >
            política de privacidade
          </a>
        </Card.Footer>
      </S.CustomCard>
    )
  }
  const standardForSignUp = innerForm => {
    return (
      <S.CustomCard>
        <CompanyImage />
        <Card.Body>
          <Card.Title>Bem-vindo</Card.Title>
          <Card.Text>
            Faça sua conta <strong>XYZ</strong> e continue em nosso site.
          </Card.Text>
          <Card.Text>
            <a href="#" onClick={signUpToggle}>
              Quer se autenticar?
            </a>
            .
          </Card.Text>
          <hr />
          {innerForm}
        </Card.Body>
        <Card.Footer className="text-center">
          Ao fazer cadastro/login, você concorda com nossa{" "}
          <a href="https://github.com/willianantunes/tutorials/blob/master/LICENSE" target="blank">
            política de privacidade
          </a>
        </Card.Footer>
      </S.CustomCard>
    )
  }

  if (classicUniversalLoginState.signUpForm) {
    return standardForSignUp(<SignUp auth0={webAuth} />)
  } else {
    if (classicUniversalLoginState.showChangePasswordForm) {
      return standardUi(<RecoverPassword auth0={webAuth} />)
    }
    if (classicUniversalLoginState.oneTimePasswordEnabled) {
      return standardUi(<OneTimePasswordLogin auth0={webAuth} />)
    } else {
      return standardUi(<DatabaseLogin auth0={webAuth} changePasswordHook={refreshToChangePasswordForm} />)
    }
  }
}

export default UniversalLogin
