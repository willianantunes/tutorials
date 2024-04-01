#!/usr/bin/env bash

set -e

export DEBIAN_FRONTEND=noninteractive

sudo apt update

echo "<<<<<< General packages"
sudo apt-get install -yq git \
  network-manager \
  curl \
  vim \
  linux-generic \
  build-essential \
  jq \
  nmap \
  net-tools \
  putty \
  httpie \
  apt-transport-https \
  ca-certificates

echo "<<<<<< Installing OpenVPN Community Edition"
# https://openvpn.net/community-resources/
# The latest version of the script can be consulted at: https://github.com/angristan/openvpn-install
# The script below is a fork of the original script.
curl -O https://raw.githubusercontent.com/dumrauf/openvpn-install/master/openvpn-install.sh
chmod +x openvpn-install.sh
sudo AUTO_INSTALL=y \
  APPROVE_IP=${public_ip} \
  ENDPOINT=${public_dns_or_ip} \
  ./openvpn-install.sh
mv openvpn-install.sh /home/${user}/openvpn-management.sh
sudo chown -R ${user}:${user} /home
# Command below fix the issue related to `Can't load /etc/openvpn/easy-rsa/pki/.rnd into RNG` during certificate generation and revoke
# https://github.com/OpenVPN/easy-rsa/issues/261
# https://superuser.com/a/1485182
openssl rand -writerand  /etc/openvpn/easy-rsa/pki/.rnd
