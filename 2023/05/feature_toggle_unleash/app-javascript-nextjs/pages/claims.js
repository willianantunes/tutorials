import React, { useEffect, useState } from "react"
import { faker } from "@faker-js/faker"
import Layout from "./components/Layout"
import Table from "./components/Table"
import { useRouter } from "next/router"
import { useUnleash } from "./contexts/feature-management"

function Claims() {
  const claims = {
    __raw:
      "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZhWVp3X0NFSTBJUnotU2FHOWJoaSJ9.eyJnaXZlbl9uYW1lIjoiQWxhZGRpbiIsImZhbWlseV9uYW1lIjoiSWFnbyIsIm5pY2tuYW1lIjoid2lsbGlhbi5saW1hLmFudHVuZXMiLCJuYW1lIjoiV2lsbGlhbiBBbnR1bmVzIiwicGljdHVyZSI6Imh0dHBzOi8vcy5ncmF2YXRhci5jb20vYXZhdGFyLzM4ZWNmYmM1NjcxODUzNmNhNTFmY2FhZTdkN2RhOWIzP3M9NDgwJnI9cGcmZD1odHRwcyUzQSUyRiUyRmNkbi5hdXRoMC5jb20lMkZhdmF0YXJzJTJGd2kucG5nIiwidXBkYXRlZF9hdCI6IjIwMjMtMDQtMjdUMjE6MTE6MzUuNjA3WiIsImVtYWlsIjoid2kubGwuaWFuLmxpbWEuYW50dW5lc0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImlzcyI6Imh0dHBzOi8vYW50dW5lcy51cy5hdXRoMC5jb20vIiwiYXVkIjoidHdxRUVKd0FrbXZaN2hiV0JpUzFHQ0RyN2dkWnFwOUgiLCJpYXQiOjE2ODI2Mjk4OTcsImV4cCI6MTY4MjY2NTg5Nywic3ViIjoiYXV0aDB8NjNhMGU1Njc4NTZiOGYyZGVlMWE4N2ZiIiwic2lkIjoiS0ZSSUdRSVpXQVJxVThNa0FSdktqd1BtLXFkMkloOHIiLCJub25jZSI6IlVsWlRkM0JPZFZwMGNYVm9VVVJ2ZFd0bGFTMWtMamhhTm1GUVVFbDBlVFp4TURCUmJubHFTekpCVVE9PSJ9.vtBRY_lZpNedGotQA_pvSsENx9ZFBEF9JKoJaRw9PsazMab48pYkbj7yQtijEYfbGscHT6kRrBTbrUp7Sul9pxVc1aWqUGOaWPP3MvvesZrlzXwaPctkNCmC4G0yQ_iPTaPwq7UEWslzWSuk3djgy8zJTwWYmgZpWd1IBdWBBd2fISrgTpCGjMsKno8PcNZVNWUSERcdn5sNl8RuK3C8_X-QgB_vNanBT4rRfgBlq_jIWCxl1nRrxU15fDJ1kZtddx5yOdQMa8Q0kQRDckW1pKFvh4p2O93k75ugG8T0pHz5L5-JkkHoU0x6nCYm7HRxMrEzzrww6E_8KxR9g5qk_g",
    given_name: "Aladdin",
    family_name: "Iago",
    nickname: "willian.lima.antunes",
    name: "Willian Antunes",
    picture:
      "https://s.gravatar.com/avatar/38ecfbc56718536ca51fcaae7d7da9b3?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fwi.png",
    updated_at: "2023-04-27T21:11:35.607Z",
    email: faker.internet.email(),
    email_verified: false,
    iss: "https://antunes.us.auth0.com/",
    aud: "twqEEJwAkmvZ7hbWBiS1GCDr7gdZqp9H",
    iat: 1682629897,
    exp: 1682665897,
    sub: "auth0|63a0e567856b8f2dee1a87fb",
    sid: "KFRIGQIZWARqU8MkARvKjwPm-qd2Ih8r",
    nonce: "UlZTd3BOdVp0cXVoUURvdWtlaS1kLjhaNmFQUEl0eTZxMDBRbnlqSzJBUQ==",
  }

  return (
    <Layout>
      <div className="row">
        <div className="col-md-12">
          <h1 className="display-9 fw-normal text-center">Check out a sample content of a real ID Token</h1>
          <Table keyValueObject={claims} />
          <p>This page is helpful for debugging. Check out which claims are available in the ID Token.</p>
        </div>
      </div>
    </Layout>
  )
}

export default function WrappedClaimsPage() {
  // You can add a loading state to avoid flashes of content. Just ask ChatGPT case you need it.
  const [disableClaimsPage, setDisableClaimsPage] = useState(false)
  const router = useRouter()
  const whenNewConfigurationAvailableHandler = client => {
    setDisableClaimsPage(client.isEnabled("DISABLE_CLAIMS_PAGE"))
  }
  const client = useUnleash(whenNewConfigurationAvailableHandler)
  useEffect(() => {
    if (client && disableClaimsPage) {
      router.replace("/404")
    }
  }, [router, disableClaimsPage, client])

  return <Claims />
}
