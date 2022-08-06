import { $ } from "../utils/dom"

export class TermsController {
  constructor() {
    this._checkBoxAcceptedTerms = $("input[name=acceptedTerms]")
    this._buttonContinueFlow = $("button.continueTermsFlow")
    // Events
    this._initAllEvents()
  }

  _initAllEvents() {
    if (this._checkBoxAcceptedTerms) {
      this._checkBoxAcceptedTerms.addEventListener("click", () => {
        this._buttonContinueFlow.disabled = !this._checkBoxAcceptedTerms.checked
      })
    }
  }
}
