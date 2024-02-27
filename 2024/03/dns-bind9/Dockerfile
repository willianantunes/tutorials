# https://bind9.readthedocs.io/en/latest/chapter1.html
# https://ubuntu.com/server/docs/service-domain-name-service-dns
# https://hub.docker.com/r/ubuntu/bind9
FROM ubuntu/bind9:9.18-22.04_beta

RUN apt update && apt install -y dnsutils iputils-ping

EXPOSE 53/udp
