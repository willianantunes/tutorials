const { onExecutePostLogin } = require("./Enrich JWT with Groups from AD")
const { ManagementClient } = require("auth0")

jest.mock("auth0")

describe("B2E: Post login -> Enrich JWT with Groups from AD", () => {
  it("Should add custom claim", async () => {
    // Arrange
    const eventLoginContext = {
      user: {
        user_id: "waad|0ukNcu0aWv9Fe05Tn_0K6gDwp_YAWzyQheHF_2_NdgQ",
      },
      secrets: {
        TENANT: "TENANT",
        AUDIENCE: "AUDIENCE",
        APP_CLIENT_ID: "APP_CLIENT_ID",
        APP_CLIENT_SECRET: "APP_CLIENT_SECRET",
      },
    }
    const auth0Api = {
      idToken: {
        setCustomClaim: jest.fn(),
      },
    }
    const fakeUserDetailsFromManagementApi = {
      groups: [
        "B2E_APP_MANAGEMENT_VIEWER",
        "B2E_APP_MANAGEMENT_SUPPORT",
        "B2E_APP_MANAGEMENT_BUSINESS",
        "B2E_APP_MANAGEMENT_DEVELOPER",
      ],
    }
    const getUserMock = jest
      .spyOn(ManagementClient.prototype, "getUser")
      .mockImplementation(() => fakeUserDetailsFromManagementApi)
    // Act
    await onExecutePostLogin(eventLoginContext, auth0Api)
    // Arrange
    expect(getUserMock).toHaveBeenCalledWith({ id: eventLoginContext.user.user_id })
    const mockSetCustomClaims = auth0Api.idToken.setCustomClaim
    expect(mockSetCustomClaims.mock.calls.length).toBe(1)
    const [claimKey, claimValue] = mockSetCustomClaims.mock.calls[0]
    expect(claimKey).toBe("https://www.willianantunes.com/ad/groups")
    expect(claimValue).toBe(fakeUserDetailsFromManagementApi.groups)
  })
})
