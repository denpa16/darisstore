FROM nginx:1.25-alpine
ENV ENVIRONMENT=development \
    HTPASSWD_NODE=off \
    HTPASSWD=override_if_needed \
    MONITORING_HTPASSWD=override_if_needed \
    ADMIN_HTPASSWD=override_if_needed \
    PDF_AUTH=off \
    TLS_MODE=off \
    SITE_HOST=localhost \
    IMGPROXY_SITE_HOST=imgproxy.localhost

EXPOSE 80/tcp 443/tcp

RUN apk upgrade && \
    apk add --no-cache esh curl openssl && \
    curl https://get.acme.sh | sh && \
    ln -s  /root/.acme.sh/acme.sh  /usr/local/bin/acme.sh && \
    rm /etc/nginx/conf.d/default.conf

COPY error_pages/ /var/www/error_pages/

COPY nginx.conf.esh ssl_params backend frontend json_logging /etc/nginx/

CMD ["/bin/sh", "-c", "echo $HTPASSWD >/etc/nginx/.htpasswd && echo $ADMIN_HTPASSWD >/etc/nginx/admin_htpasswd && echo $MONITORING_HTPASSWD >/etc/nginx/monitoring_htpasswd && esh -o /etc/nginx/conf.d/nginx.conf /etc/nginx/nginx.conf.esh && exec nginx -g 'daemon off;'"]
