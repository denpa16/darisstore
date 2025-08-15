FROM node:20.5.1-alpine

ARG SERVER_API_URL
ENV SERVER_API_URL=$SERVER_API_URL
ARG SENTRY_DSN_FRONTEND
ENV SENTRY_DSN_FRONTEND=$SENTRY_DSN_FRONTEND
ARG IMGPROXY_SITE_HOST
ENV IMGPROXY_SITE_HOST=$IMGPROXY_SITE_HOST

WORKDIR /app
COPY package.json package-lock.json /app/
RUN apk add --no-cache --virtual build-deps make gcc g++ python3 && npm i && apk del --no-cache build-deps
COPY ./ /app
RUN chmod +x entrypoint.production.sh
RUN npm run build
