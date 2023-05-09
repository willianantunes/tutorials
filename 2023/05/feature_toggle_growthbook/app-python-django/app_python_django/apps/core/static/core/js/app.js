import { GrowthBook } from "@growthbook/growthbook"

const $ = document.querySelector.bind(document)

const growthBook = new GrowthBook({
  apiHost: "http://localhost:3100",
  clientKey: "sdk-XPTKBIkHfBGS6E",
  enableDevMode: true,
})

const featureToggleHandler = () => {
  console.log(`Feature toggle handler has been called!`)
  if (growthBook.isOn("SHOW_EASTER_EGG".toLowerCase())) {
    $(".feature-toggle-placeholder").style.display = "inline"
  } else {
    $(".feature-toggle-placeholder").style.display = "none"
  }
}
growthBook.setRenderer(featureToggleHandler)
growthBook.loadFeatures({ autoRefresh: true }).then(() => console.log("Features have been loaded"))
