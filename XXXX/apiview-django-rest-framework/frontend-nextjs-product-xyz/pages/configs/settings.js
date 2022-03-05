function getEnvOrRaiseException(envName, envValue) {
  if (!envValue) throw new Error(`Environment variable ${envName} is not set!`)

  return envValue
}

export const NEXT_PUBLIC_IDP_BACKEND_USER_MANAGEMENT_AUDIENCE = getEnvOrRaiseException(
  "NEXT_PUBLIC_IDP_BACKEND_USER_MANAGEMENT_AUDIENCE",
  process.env.NEXT_PUBLIC_IDP_BACKEND_USER_MANAGEMENT_AUDIENCE
)
export const NEXT_PUBLIC_IDP_DOMAIN = getEnvOrRaiseException("NEXT_PUBLIC_IDP_DOMAIN", process.env.NEXT_PUBLIC_IDP_DOMAIN)
export const NEXT_PUBLIC_IDP_CLIENT_ID = getEnvOrRaiseException(
  "NEXT_PUBLIC_IDP_CLIENT_ID",
  process.env.NEXT_PUBLIC_IDP_CLIENT_ID
)
export const NEXT_PUBLIC_IDP_CLIENT_REDIRECT_URI = getEnvOrRaiseException(
  "NEXT_PUBLIC_IDP_CLIENT_REDIRECT_URI",
  process.env.NEXT_PUBLIC_IDP_CLIENT_REDIRECT_URI
)
export const NEXT_PUBLIC_USER_MANAGEMENT_ENDPOINT = getEnvOrRaiseException(
  "NEXT_PUBLIC_USER_MANAGEMENT_ENDPOINT",
  process.env.NEXT_PUBLIC_USER_MANAGEMENT_ENDPOINT
)
