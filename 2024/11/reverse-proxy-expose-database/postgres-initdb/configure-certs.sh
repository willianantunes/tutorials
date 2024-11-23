#!/bin/bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -ex

cd $PGDATA

# CREATE ROOT CA
openssl genrsa -out root-ca.key 4096
openssl req -x509 -new -nodes -key root-ca.key -sha256 -days 3650 -out root-ca.crt \
-subj "/C=US/ST=State/L=City/O=My God CA/OU=Root CA/CN=root-ca" \
-addext "basicConstraints=critical,CA:true,pathlen:0" \
-addext "keyUsage=critical,keyCertSign,cRLSign,digitalSignature" \
-addext "subjectKeyIdentifier=hash" \
-addext "authorityKeyIdentifier=keyid:always,issuer"
# CREATE CERTIFICATE SIGNING REQUEST FOR SERVER
openssl genrsa -out postgresql-server.key 2048
openssl req -new -key postgresql-server.key -out postgresql-server.csr \
-subj "/C=US/ST=State/L=City/O=My Domain/OU=Domain Cert/CN=db"
# SIGN SERVER CERTIFICATE USING ROOT CA
openssl x509 -req -in postgresql-server.csr -CA root-ca.crt -CAkey root-ca.key -CAcreateserial \
-out postgresql-server.crt -days 365 -sha256 \
-extfile <(printf "basicConstraints=CA:FALSE\nkeyUsage=digitalSignature,keyEncipherment\nextendedKeyUsage=serverAuth,clientAuth\nsubjectAltName=DNS:db")
# BUILD CERTIFICATE CHAIN
cat postgresql-server.crt root-ca.crt > postgresql-server-chain.crt

chmod 600 postgresql-server.key
ls -la
