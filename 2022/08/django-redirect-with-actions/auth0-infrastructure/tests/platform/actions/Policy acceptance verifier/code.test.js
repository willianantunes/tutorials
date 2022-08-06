const { onExecutePostLogin, onContinuePostLogin } = require("../../../../platform/actions/Policy acceptance verifier/code.js")

const expectedPropertyKey = "termsAcceptanceHistory"

describe("Policy acceptance verifier: Post login", () => {
  let baseEventLoginContext
  let auth0Api
  const fakeToken = "eyJ0eXAiOiJZb3UgYXJlIGN1cmlvdXMsIGFyZW4ndCB5b3U_IiwiYWxnIjoiSFMyNTYifQ.."

  beforeEach(() => {
    baseEventLoginContext = {
      secrets: {
        THE_SECRET_USED_TO_CREATE_OPEN_AND_VALIDATE_THE_JWT: "salt",
        BACKEND_DJANGO_ENDPOINT: "https://BACKEND_DJANGO_ENDPOINT.ngrok.io",
      },
      authentication: {
        methods: [
          {
            name: "pwd",
            timestamp: "2018-11-13T20:20:39+00:00",
          },
        ],
      },
      client: {
        client_id: "YOUR_APP_ID_GOES_HERE",
      },
      user: {
        user_id: "USER_ID",
        app_metadata: {},
      },
    }
    auth0Api = {
      user: {
        setAppMetadata: jest.fn(),
      },
      redirect: {
        encodeToken: jest.fn(() => fakeToken),
        sendUserTo: jest.fn(),
      },
    }
  })

  describe("When first login in any application", () => {
    it("Should add new entry when the first login ever", async () => {
      // Act
      await onExecutePostLogin(baseEventLoginContext, auth0Api)
      // Assert
      expect(auth0Api.user.setAppMetadata).toBeCalledTimes(0)
      const mockEncodeToken = auth0Api.redirect.encodeToken
      expect(mockEncodeToken).toBeCalledTimes(1)
      const expectedValueForEncodeToken = {
        secret: baseEventLoginContext.secrets.THE_SECRET_USED_TO_CREATE_OPEN_AND_VALIDATE_THE_JWT,
        expiresInSeconds: 60 * 10,
        payload: {
          id: baseEventLoginContext.user.user_id,
          app_metadata: baseEventLoginContext.user.app_metadata,
          client_id: baseEventLoginContext.client.client_id,
          whenTheEventStarted: baseEventLoginContext.authentication.methods[0]["timestamp"],
        },
      }
      expect(mockEncodeToken.mock.calls[0][0]).toStrictEqual(expectedValueForEncodeToken)
      const mockSendUserTo = auth0Api.redirect.sendUserTo
      expect(mockSendUserTo).toBeCalledTimes(1)
      const [receivedEndpoint, receivedOptions] = mockSendUserTo.mock.calls[0]
      expect(receivedEndpoint).toBe(baseEventLoginContext.secrets.BACKEND_DJANGO_ENDPOINT)
      const expectedValueForSendUserTo = {
        query: { session_token: fakeToken },
      }
      expect(receivedOptions).toStrictEqual(expectedValueForSendUserTo)
    })
  })

  describe("When second login in any application", () => {
    it("Should do nothing", async () => {
      // Arrange
      baseEventLoginContext.user.app_metadata = {
        [expectedPropertyKey]: {},
      }
      // Act
      await onExecutePostLogin(baseEventLoginContext, auth0Api)
      // Assert
      expect(auth0Api.user.setAppMetadata).toBeCalledTimes(0)
      expect(auth0Api.redirect.encodeToken).toBeCalledTimes(0)
      expect(auth0Api.redirect.sendUserTo).toBeCalledTimes(0)
    })
  })
})

describe("Policy acceptance verifier: On continue post login", () => {
  let baseEventLoginContext
  let auth0Api
  const fakePayload = {
    other: {
      [expectedPropertyKey]: [{ version: "1", registeredAt: new Date().toISOString() }],
    },
  }

  beforeEach(() => {
    baseEventLoginContext = {
      secrets: {
        THE_SECRET_USED_TO_CREATE_OPEN_AND_VALIDATE_THE_JWT: "salt",
      },
    }
    auth0Api = {
      user: {
        setAppMetadata: jest.fn(),
      },
      redirect: {
        validateToken: jest.fn(() => fakePayload),
      },
    }
  })

  describe("When the user returns to Auth0", () => {
    it("Should apply what the flow receives from the backend", async () => {
      // Act
      await onContinuePostLogin(baseEventLoginContext, auth0Api)
      // Assert
      const mockValidateToken = auth0Api.redirect.validateToken
      expect(mockValidateToken).toBeCalledTimes(1)
      const expectedValueForValidateToken = {
        secret: baseEventLoginContext.secrets.THE_SECRET_USED_TO_CREATE_OPEN_AND_VALIDATE_THE_JWT,
        tokenParameterName: "data",
      }
      expect(mockValidateToken.mock.calls[0][0]).toStrictEqual(expectedValueForValidateToken)
      const mockSetAppMetadata = auth0Api.user.setAppMetadata
      expect(mockSetAppMetadata).toBeCalledTimes(1)
      const [propertyName, propertyValue] = mockSetAppMetadata.mock.calls[0]
      expect(propertyName).toBe(expectedPropertyKey)
      expect(propertyValue).toStrictEqual(fakePayload["other"][expectedPropertyKey])
    })
  })
})
