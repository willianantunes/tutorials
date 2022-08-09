# Redirect with Actions on Auth0 

Require users to accept custom privacy policies during the login flow on Auth0. Don't know how? Let's see one solution for this through [Redirect with Actions](https://www.willianantunes.com/blog/2022/08/terms-of-use-through-auth0-actions/)!

## Running the project

Create an Auth0 tenant for you first; it's for free. So, replace the environment variables in the [Compose file](./docker-compose.yaml). Then, just run the following command:

    docker-compose up update-settings

Now you can run the following service:

    docker-compose up app
