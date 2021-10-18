import axios from "axios"

export async function consultUserData() {
  const options = {
    method: "GET",
    timeout: 15 * 1000,
  }
  options.url = "http://localhost:8000/api/v1/user-info"
  options.headers = { ...options.headers }

  const response = await axios(options)

  return await response.data
}
