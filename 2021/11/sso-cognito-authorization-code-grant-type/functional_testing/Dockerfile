FROM selenium/standalone-chrome:95.0

RUN sudo apt-get update
RUN sudo apt-get install -y software-properties-common && sudo add-apt-repository ppa:deadsnakes/ppa
RUN sudo apt-get update
RUN sudo apt-get install -y python3.9 python3.9-dev python3.9-venv python3-pip apt-utils && sudo apt-get clean
# https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/
# Why am I using it? Look at more details here: https://www.willianantunes.com/blog/2021/11/sso-with-cognito-through-the-authorization-code-grant-type/
RUN sudo apt-get install -y net-tools nginx

WORKDIR /home/seluser

ENV PATH="/home/seluser/.local/bin:${PATH}"

RUN sudo ln -s /usr/bin/python3.9 /usr/bin/python

COPY Pipfile Pipfile.lock ./

RUN python -m pip install --upgrade pip pipenv --user

RUN pipenv install --system --deploy --ignore-pipfile

COPY . ./

RUN rm Pipfile Pipfile.lock

USER seluser

CMD [ "./scripts/start.sh" ]
