# SSO with Django Admin through Auth0

Do you want to know about [SSO with Django Admin through Auth0](https://www.willianantunes.com/blog/2022/05/django-admin-authentication-using-sso-through-auth0/)? Look at this project 👀!

## Project details

You first should configure your Auth0 tenant properly! Then retrieve some details from it and configure your backend application. Don't worry, you can do it at once with the following command:

    docker-compose build update-settings && docker-compose up update-settings

After it's done, you can run the project

    docker-compose up admin-backend

To run tests:

    docker-compose up admin-backend-tests
