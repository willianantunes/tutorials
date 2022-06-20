require('bundler/setup')

# https://bundler.io/guides/bundler_setup.html
# https://bundler.io/guides/groups.html
Bundler.require(:default)

require_relative('./lib/auth0_liquid_tester')

run(Auth0LiquidTester)
