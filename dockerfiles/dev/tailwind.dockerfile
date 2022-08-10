FROM node:16

WORKDIR /code

COPY package.json yarn.lock /code/

RUN yarn

COPY . .