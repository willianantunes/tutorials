FROM node:18-alpine as build

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci

COPY . ./

CMD npm run dev
