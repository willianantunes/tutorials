import axios from "axios"
import { NEXT_PUBLIC_USER_MANAGEMENT_ENDPOINT } from "../configs/settings"

export async function retrieveUserAttributes(accessToken) {
  const options = {
    method: "GET",
    timeout: 15 * 1000,
    headers: {
      Accept: "application/json",
    },
  }
  options.url = `${NEXT_PUBLIC_USER_MANAGEMENT_ENDPOINT}/api/v1/users/attributes`
  options.headers = { ...options.headers, ["Authorization"]: `Bearer ${accessToken}` }

  const response = await axios(options)

  return await response.data
}

export async function updateUserAttributes(accessToken, attributes) {
  const options = {
    method: "POST",
    timeout: 15 * 1000,
    headers: {
      Accept: "application/json",
    },
  }
  options.url = `${NEXT_PUBLIC_USER_MANAGEMENT_ENDPOINT}/api/v1/users/attributes`
  options.data = {
    full_name: attributes.full_name,
    given_name: attributes.given_name,
    family_name: attributes.family_name,
  }
  options.headers = { ...options.headers, ["Authorization"]: `Bearer ${accessToken}` }

  const response = await axios(options)

  return response.status
}
