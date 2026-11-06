FROM nginx:1.27-alpine
COPY sitio/ /usr/share/nginx/html/
COPY git_config_expuesto /usr/share/nginx/html/.git/config
RUN chmod -R a+rX /usr/share/nginx/html
