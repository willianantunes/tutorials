#!/usr/bin/env bash

set -e

# https://docs.openssl.org/master/man5/x509v3_config/#extended-key-usage
# https://docs.openssl.org/master/man5/x509v3_config/#key-usage
# https://superuser.com/a/1248085
echo "Generating self-signed certificate for the proxy server"
openssl req -x509 -out self_issued_cert.pem -keyout self_issued_key.pem \
  -days 365 \
  -newkey rsa:2048 -nodes -sha256 \
  -subj '/CN=localhost' -extensions EXT -config <( \
   printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth") && \
   chmod 644 self_issued_cert.pem && \
   chmod 600 self_issued_key.pem

ORIGIN_SERVER_ADDRESS=${ORIGIN_SERVER_ADDRESS:-db}
ORIGIN_SERVER_PORT=${ORIGIN_SERVER_PORT:-5432}
echo "You set the origin server address to $ORIGIN_SERVER_ADDRESS and port to $ORIGIN_SERVER_PORT"

# CAS_FOLDER=/etc/pgt_proxy/client_tls/aws_rds/
# CAS_FOLDER=/etc/pgt_proxy/client_tls/firefox/
CAS_FOLDER=/etc/pgt_proxy/client_tls/custom_cas
mkdir -p $CAS_FOLDER

# https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-networking-ssl-tls#download-root-ca-certificates-and-update-application-clients-in-certificate-pinning-scenarios
# openssl s_client -starttls postgres -showcerts -connect $ORIGIN_SERVER_ADDRESS:$ORIGIN_SERVER_PORT
# openssl s_client -starttls postgres -showcerts -connect localhost:5432
echo "Retrieving the origin server's CA certificate"
ORIGIN_CERTS=$(openssl s_client -starttls postgres -showcerts -connect $ORIGIN_SERVER_ADDRESS:$ORIGIN_SERVER_PORT < /dev/null 2>/dev/null | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p')
echo "$ORIGIN_CERTS" | awk 'BEGIN {c=0;} /-BEGIN CERTIFICATE-/{c++} {print > "ca-" c ".pem"}'
cp ca-*.pem $CAS_FOLDER
chmod 600 $CAS_FOLDER/*
ls -la $CAS_FOLDER

echo "Starting the proxy server..."
/etc/pgt_proxy/run --server-private-key-path ./self_issued_key.pem \
--server-certificate-path ./self_issued_cert.pem \
--server-port 9000 \
--client-connection-host-or-ip $ORIGIN_SERVER_ADDRESS \
--client-connection-port $ORIGIN_SERVER_PORT \
--client-tls-validation-host $ORIGIN_SERVER_ADDRESS \
--client-ca-roots-path $CAS_FOLDER \
--log TRACE
