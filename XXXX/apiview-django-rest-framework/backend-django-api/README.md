# Django API

How do you create an API that can only be accessed with a valid access token? Check out this project and understand how it works behind the curtain.

## Notes

1. The authentication process method was copied from [jazzband/djangorestframework-simplejwt](https://github.com/jazzband/djangorestframework-simplejwt), but heavily changed to meet our criteria. [JWTTokenUserAuthentication backend](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/experimental_features.html) is indeed a great idea.
