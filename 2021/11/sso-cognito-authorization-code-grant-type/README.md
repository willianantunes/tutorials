# SSO with Cognito through Authorization Code grant type

Do you want to know how to do an [SSO with Cognito through the Authorization Code grant type](https://www.willianantunes.com/blog/2021/11/sso-with-cognito-through-the-authorization-code-grant-type/)? Look at this project!

## Project details

This is separated in 4 projects:

- **cognito_iac**: It contains all the infrastructure code to create your Authorization Server.
- **functional_testing**: When you run it, you can understand how the authorization code grant type works from the user's point of view.
- **product_a**: Just mocking a random product. It's identified by the letter A.
- **product_b**: Just mocking a random product. It's identified by the letter B.

To test this project out, you'll need to do the following:

1. Create the Cognito user pool from the `cognito_iac` folder with the help of `Terraform`.
2. Execute the command `refresh_products_projects.py`. It gathers all the required secrets and params from `terraform output` and configure the products A and B, and the functional testing projects for you automatically. Check it out and see how it works!
3. Start all the services related to products A and B issuing `docker-compose up -d product-a product-b` command.
4. Start the functional testing service through the command `docker-compose up functional-testing`

Test it manually yourself too 😆!
