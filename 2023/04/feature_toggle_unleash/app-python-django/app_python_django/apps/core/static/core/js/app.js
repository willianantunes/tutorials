import { UnleashClient } from "unleash-proxy-client"

const $ = document.querySelector.bind(document)

const unleash = new UnleashClient({
  url: "http://localhost:4242/api/frontend",
  clientKey: "default:development.unleash-insecure-frontend-api-token",
  appName: "app-python-django-frontend",
})

const featureToggleHandler = () => {
  console.log(`Feature toggle handler has been called!`)
  if (unleash.isEnabled("SHOW_EASTER_EGG")) {
    $(".feature-toggle-placeholder").style.display = "inline"
  } else {
    $(".feature-toggle-placeholder").style.display = "none"
  }
}

unleash.on("ready", featureToggleHandler)
unleash.on("update", featureToggleHandler)
unleash.start()
