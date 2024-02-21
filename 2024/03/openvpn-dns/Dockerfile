FROM docker:latest

RUN apk add --no-cache bash vim openvpn wget unzip curl sshpass openssh-client python3 py3-pip git github-cli jq groff mandoc

# https://stackoverflow.com/a/77334728/3899136
RUN echo "[global]" >> /etc/pip.conf && echo "break-system-packages = true" >> /etc/pip.conf
RUN pip3 install awscli

# Latest Terraform version
RUN wget https://releases.hashicorp.com/terraform/1.3.6/terraform_1.3.6_linux_amd64.zip && \
    unzip terraform_1.3.6_linux_amd64.zip -d /usr/local/bin/ && \
    rm terraform_1.3.6_linux_amd64.zip

# Azure CLI
# https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=script
# https://github.com/Azure/azure-cli/issues/24872
RUN apk add --no-cache -q --virtual=build gcc musl-dev python3-dev libffi-dev openssl-dev cargo make \
     && pip install --no-cache-dir azure-cli -q \
     && apk del --purge build

# Terrascan is a static code analyzer for Infrastructure as Code.
# https://github.com/tenable/terrascan/tree/3bf466ddffb5993290a09730450addc3e6f036da?tab=readme-ov-file#quick-start
RUN curl -L "$(curl -s https://api.github.com/repos/tenable/terrascan/releases/latest | grep -o -E "https://.+?_Linux_x86_64.tar.gz")" > terrascan.tar.gz && \
    tar -xf terrascan.tar.gz terrascan && rm terrascan.tar.gz && \
    install terrascan /usr/local/bin && rm terrascan

# tfsec uses static analysis of your terraform code to spot potential misconfigurations
RUN curl -s https://raw.githubusercontent.com/aquasecurity/tfsec/master/scripts/install_linux.sh | sed 's/ --quiet//g' | bash

# Install kubectl and kubelogin
RUN az aks install-cli

WORKDIR /app
