import React, { useEffect, useState } from "react"
import Layout from "./components/Layout"
import { useUnleash } from "./contexts/feature-management"
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
  /**
   * @param client {UnleashClient}
   */
  const configureBehaviorThroughFeatures = client => {
    setShowProfiles(client.isEnabled("SHOW_PROFILES"))
    setAllowProfileManagement(client.isEnabled("ALLOW_PROFILE_MANAGEMENT"))
    const textPresentationToggle = client.getVariant("TEXT_PRESENTATION")
    if (textPresentationToggle.enabled) {
      // You can always get the same variant by defining the stickiness
      setTextPresentation(JSON.parse(textPresentationToggle.payload.value))
    }
    const buttonSchemeToggle = client.getVariant("PROFILE_MANAGEMENT_BUTTON_SCHEME")
    if (buttonSchemeToggle.enabled) {
      // You can always get the same variant by defining the stickiness
      setButtonSchemeValue(buttonSchemeToggle.payload.value)
    }
  }
  const whenNewConfigurationAvailableHandler = client => {
    configureBehaviorThroughFeatures(client)
  }
  const client = useUnleash(whenNewConfigurationAvailableHandler)
  useEffect(() => {
    if (client) {
      configureBehaviorThroughFeatures(client)
    }
  }, [client])

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
