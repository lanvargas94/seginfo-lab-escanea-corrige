FROM alpine:3.20
RUN apk add --no-cache vsftpd \
    && mkdir -p /srv/ftp /var/run/vsftpd/empty \
    && echo "Lista de precios inventada para el laboratorio" > /srv/ftp/precios.txt \
    && chown -R root:root /srv/ftp && chmod 555 /srv/ftp
EXPOSE 21
# vsftpd exige que su configuracion pertenezca a root, por eso se copia al arrancar.
CMD ["sh", "-c", "cp /etc/vsftpd/vsftpd.conf /tmp/vsftpd.conf && chown root:root /tmp/vsftpd.conf && chmod 600 /tmp/vsftpd.conf && exec /usr/sbin/vsftpd /tmp/vsftpd.conf"]
