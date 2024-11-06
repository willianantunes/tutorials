# https://hub.docker.com/r/rundeck/rundeck/tags
ARG RUNDECK_IMAGE=rundeck/rundeck:5.7.0
FROM ${RUNDECK_IMAGE}

RUN sudo apt-get update && \
    sudo apt-get install -y python3 python3-pip python3-venv vim

RUN sudo python3 -m venv /venv
RUN sudo chown -R rundeck:root /venv
ENV PATH=/venv/bin:$PATH

RUN pip install kubernetes

# https://docs.rundeck.com/docs/administration/configuration/plugins/installing.html#installation
ARG KUBERNETES_PLUGIN_VERSION=2.0.14
ADD --chown=rundeck:root \
    https://github.com/rundeck-plugins/kubernetes/releases/download/${KUBERNETES_PLUGIN_VERSION}/kubernetes-${KUBERNETES_PLUGIN_VERSION}.zip \
    /home/rundeck/libext

ARG S3_PLUGIN_VERSION=1.0.16
ADD --chown=rundeck:root \
    https://github.com/rundeck-plugins/rundeck-s3-log-plugin/releases/download/v${S3_PLUGIN_VERSION}/rundeck-s3-log-plugin-${S3_PLUGIN_VERSION}.jar \
    /home/rundeck/libext

# https://docs.rundeck.com/docs/administration/configuration/database/#add-the-jdbc-driver
# https://central.sonatype.com/artifact/com.microsoft.sqlserver/mssql-jdbc
RUN curl -L -o /home/rundeck/server/lib/mssql-jdbc-12.8.1.jre8.jar \
    https://repo1.maven.org/maven2/com/microsoft/sqlserver/mssql-jdbc/12.8.1.jre8/mssql-jdbc-12.8.1.jre8.jar && \
    chown rundeck:root /home/rundeck/server/lib/mssql-jdbc-12.8.1.jre8.jar

# https://docs.rundeck.com/docs/administration/configuration/docker/extending-configuration.html#extending-docker-configuration
COPY --chown=rundeck:root remco /etc/remco
