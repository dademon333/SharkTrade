ARG COMPOSE_PROJECT_NAME
FROM ${COMPOSE_PROJECT_NAME}_frontend as frontend

FROM nginx:1.21-alpine

COPY ./logo.ico /etc/nginx/favicon.ico
COPY ./nginx.conf /etc/nginx/nginx.conf

COPY --from=frontend /frontend/build/static /frontend/build/static

ENTRYPOINT ["nginx", "-g", "daemon off;"]