FROM node:18-alpine

WORKDIR /usr/src/app/frontend/

COPY package.json .
RUN npm install --only=prod --force

ARG REACT_APP_SERVER_URL

COPY . .
RUN  \
    REACT_APP_SERVER_URL=$REACT_APP_SERVER_URL \
    GENERATE_SOURCEMAP=false \
    npm run build