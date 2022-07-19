FROM nginx:1.21-alpine

COPY ./logo.ico /etc/nginx/favicon.ico
COPY ./nginx.conf /etc/nginx/nginx.conf

ENTRYPOINT ["nginx", "-g", "daemon off;"]