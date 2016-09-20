

cd /etc/pki/tls
sudo openssl req -subj '/CN=ELK_server_fqdn/' \
                -x509 \
                -days 3650 \
                -batch \
                -nodes \
                -newkey rsa:2048 \
                -keyout private/logstash-forwarder.key \
                -out certs/logstash-forwarder.crt

