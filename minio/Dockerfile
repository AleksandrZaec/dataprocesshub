FROM minio/minio:latest

COPY conf_minio.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/conf_minio.sh

ENTRYPOINT ["/usr/local/bin/conf_minio.sh"]