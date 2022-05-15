#!/usr/bin/env bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -e

# You should run the command at the root folder of `auth0-infrastructure` project
npm run deploy:sandbox

# When running through Compose, you'll be able to configure `.env.development` variable of `apiview_django_rest_framework` project
python scripts/env_setter.py
