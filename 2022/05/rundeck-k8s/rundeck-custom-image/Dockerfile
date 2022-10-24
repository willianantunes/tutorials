# https://hub.docker.com/r/rundeck/rundeck/tags
ARG RUNDECK_IMAGE=rundeck/rundeck:4.7.0-20221006
FROM ${RUNDECK_IMAGE}

RUN sudo apt-get update && \
    sudo apt-get install -y python python3-pip python3-venv vim

RUN sudo python3 -m venv /venv
RUN sudo chown -R rundeck:root /venv
ENV PATH=/venv/bin:$PATH

RUN pip install kubernetes

# https://docs.rundeck.com/docs/administration/configuration/plugins/installing.html#installation
ARG KUBERNETES_PLUGIN_VERSION=2.0.8
ADD --chown=rundeck:root \
    https://github.com/rundeck-plugins/kubernetes/releases/download/${KUBERNETES_PLUGIN_VERSION}/kubernetes-plugin-${KUBERNETES_PLUGIN_VERSION}.zip \
    /home/rundeck/libext

# https://docs.rundeck.com/docs/administration/configuration/docker/extending-configuration.html#extending-docker-configuration
COPY --chown=rundeck:root remco /etc/remco
