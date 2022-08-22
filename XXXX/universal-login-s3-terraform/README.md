# Universal Login S3 Terraform

First you should create your infrastructure. Don't forget to update the credential and change the variables to match your requirements. Then, access the folder `iac` followed by the command:

    terraform apply

Apply the configuration and wait until it's done. Then build the project `universal-login`:

    ASSET_PREFIX=https://dev-auth0-idp-sandbox npm run build

Configure you `AWS CLI` to use the credentials for the `auth0-uploadfiles-s3-idp` service account. Now, at [this folder](./), execute the following command (remove the flag `--dryrun` when you think it's right):

    aws s3 sync --acl public-read ./universal-login/out/_next/ s3://dev-auth0-idp-sandbox/_next --dryrun

In case you want to erase the bucket:

    aws s3 rm s3://dev-auth0-idp-sandbox --recursive

Finally, we can upload the HTML files to Auth0. You can save them manually on Auth0 or use the following commands:

    aws s3 sync --acl public-read ./universal-login/out/_next/ s3://dev-auth0-idp-sandbox/_next
