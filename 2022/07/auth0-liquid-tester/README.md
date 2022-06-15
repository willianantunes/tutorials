# Auth0 Liquid Tester

Wanna make sure your liquid template is indeed working as expected? Use this project as a playground environment to create your custom templates!

## Project details

Will be available soon! Stay tuned!

In the meantime, know you can start the project with the command:

    docker-compose up

Then you can access the template at `http://localhost:9292/`. Just change the templates and the [auth0_liquid_tester.rb](./lib/auth0_liquid_tester.rb) to match your expected scenario.

This is the home page:

![All templates available, including emails and new universal login samples.](./docs/screenshot-2022-06-15_11-50-09-all-templates.png)

When you click on "Enroll in MFA":

![Email template about MFA invitation.](./docs/screenshot-2022-06-15_11-51-35-enroll-mfa.png)

This is the template about the New Universal Login including with footers:

![New Universal Login with footer.](./docs/screenshot-2022-06-15_11-51-24-nul-footer.png)

## Useful links

- [Customize New Universal Login Pages](https://auth0.com/docs/customize/universal-login-pages/universal-login-page-templates)
- [Liquid Cheat Sheet](https://www.shopify.com/partners/shopify-cheat-sheet)
