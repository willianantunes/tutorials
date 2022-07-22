import Document, { Head, Html, Main, NextScript } from "next/document"

class MyDocument extends Document {
  static async getInitialProps(ctx) {
    const pathName = ctx.pathname

    const initialProps = await Document.getInitialProps(ctx)

    return {
      ...initialProps,
      pathName: pathName,
    }
  }

  render() {
    const { pathName } = this.props

    return (
      <Html>
        <Head>
          <script
            async
            src="https://cdnjs.cloudflare.com/ajax/libs/holder/2.9.8/holder.min.js"
            integrity="sha512-O6R6IBONpEcZVYJAmSC+20vdsM07uFuGjFf0n/Zthm8sOFW+lAq/OK1WOL8vk93GBDxtMIy6ocbj6lduyeLuqQ=="
            crossOrigin="anonymous"
            referrerPolicy="no-referrer"
          />
          {pathName === "/login" && (
            <script
              dangerouslySetInnerHTML={{
                __html: `
                // This will store the configuration received by the Identity Provider!
                var configurationFromProvider, paramsFromProvider, leeway
                try {
                    configurationFromProvider = JSON.parse(decodeURIComponent(escape(window.atob("@@config@@"))))
                    configurationFromProvider.extraParams = configurationFromProvider.extraParams || {}
                    leeway = configurationFromProvider.internalOptions.leeway
                    if (leeway) {
                        const convertedLeeway = parseInt(leeway)
                        if (!isNaN(convertedLeeway)) {
                            configurationFromProvider.internalOptions.leeway = convertedLeeway
                        }
                    }
                    paramsFromProvider = Object.assign(
                        {
                            overrides: {
                                __tenant: configurationFromProvider.auth0Tenant,
                                __token_issuer: configurationFromProvider.authorizationServer.issuer,
                            },
                            domain: configurationFromProvider.auth0Domain,
                            clientID: configurationFromProvider.clientID,
                            redirectUri: configurationFromProvider.callbackURL,
                            responseType: "code",
                        },
                        configurationFromProvider.internalOptions
                    )
                } catch (exception) {
                    console.error("The configuration value hasn't been provided!", exception.stack)
                }
              `,
              }}
            />
          )}
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    )
  }
}

export default MyDocument
