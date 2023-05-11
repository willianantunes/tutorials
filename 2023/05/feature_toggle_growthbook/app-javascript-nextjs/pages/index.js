import React, { useEffect, useState } from "react"
import Layout from "./components/Layout"
import { useGrowthBook } from "@growthbook/growthbook-react"
import { generateListOfProfiles } from "./support/data-provider"

export default function Home() {
  // States
  const [buttonSchemeValue, setButtonSchemeValue] = useState("btn-danger")
  const [showProfiles, setShowProfiles] = useState(false)
  const [allowProfileManagement, setAllowProfileManagement] = useState(false)
  const [textPresentation, setTextPresentation] = useState({
    title: "Hello there 😄!",
    subTitle: "Change how this app behave by changing the feature toggle tool ⚒",
    profileTitle: "Registered profiles",
  })
  const [profiles, setProfiles] = useState(generateListOfProfiles())
  // Events
  const deleteProfile = e => {
    e.preventDefault()
    const form = e.target
    const profileId = form.querySelector(`input[name=profileId]`).value
    const updatedProfiles = profiles.filter(profile => profile.id !== profileId)
    setProfiles(updatedProfiles)
  }
  // Feature toggle
  const growthbook = useGrowthBook()
  useEffect(() => {
    if (!growthbook) return
    let showProfiles = growthbook.isOn("SHOW_PROFILES".toLowerCase())
    console.log(`Should show profiles? ${showProfiles}`)
    setShowProfiles(showProfiles)
    setAllowProfileManagement(growthbook.isOn("ALLOW_PROFILE_MANAGEMENT".toLowerCase()))
    const textPresentationToggle = growthbook.getFeatureValue("TEXT_PRESENTATION".toLowerCase(), {
      title: "Hello there 😄!",
      subTitle: "Change how this app behave by changing the feature toggle tool ⚒",
      profileTitle: "Registered profiles",
    })
    setTextPresentation(textPresentationToggle)
    const buttonSchemeToggle = growthbook.getFeatureValue("PROFILE_MANAGEMENT_BUTTON_SCHEME".toLowerCase(), "btn-danger")
    setButtonSchemeValue(buttonSchemeToggle)
  }, [growthbook])

  return (
    <Layout>
      <div className="pricing-header p-3 pb-md-4 mx-auto text-center">
        <h1 className="display-4 fw-normal">{textPresentation.title}</h1>
        <p className="fs-5 text-muted">{textPresentation.subTitle}</p>
      </div>

      <div className="card">
        <h5 className="card-header">{textPresentation.profileTitle}</h5>
        <div className="card-body">
          {showProfiles && (
            <table className="table">
              <thead>
                <tr>
                  <th scope="col">username</th>
                  <th scope="col">name</th>
                  <th scope="col">sex</th>
                  <th scope="col">address</th>
                  <th scope="col">mail</th>
                  <th scope="col">birthdate</th>
                  {allowProfileManagement && <th scope="col">actions</th>}
                </tr>
              </thead>
              <tbody>
                {profiles.map(profile => (
                  <tr key={profile.username}>
                    <td>{profile.username}</td>
                    <td>{profile.name}</td>
                    <td>{profile.sex}</td>
                    <td>{profile.address}</td>
                    <td>{profile.mail}</td>
                    <td>{profile.birthdate}</td>
                    {allowProfileManagement && (
                      <td>
                        <form onSubmit={deleteProfile}>
                          <button type="submit" className={`btn ${buttonSchemeValue} mb-3 `}>
                            Delete row
                          </button>
                          <input type="hidden" name="profileId" value={profile.id} />
                        </form>
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          )}
          {!showProfiles && <p className="card-text">This is not available. Try again later.</p>}
        </div>
      </div>
    </Layout>
  )
}
