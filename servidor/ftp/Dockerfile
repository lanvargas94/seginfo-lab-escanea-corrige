FROM alpine:3.20
RUN apk add --no-cache vsftpd \
    && mkdir -p /srv/ftp /var/run/vsftpd/empty \
    && echo "Lista de precios inventada para el laboratorio" > /srv/ftp/precios.txt \
    && chown -R root:root /srv/ftp && chmod 555 /srv/ftp
EXPOSE 21
CMD ["/usr/sbin/vsftpd", "/etc/vsftpd/vsftpd.conf"]
