# Zato web-admin. This will also create the ODB if it does not exist.

FROM ubuntu:14.04

# Install helper tools.
RUN apt-get update
RUN apt-get install -y apt-transport-https \
    python-software-properties \
    software-properties-common \
    curl \
    telnet \
    wget \
    git \
    supervisor

# Prep folders
RUN mkdir -p /opt/zato/
WORKDIR /opt/zato/

# Clone the repo
RUN git clone https://github.com/zatosource/zato current
WORKDIR /opt/zato/current/code/

# Install zato   || Run failover scripts.
RUN ./install.sh || ./bin/python/ bootstrap.py -v 1.7.0 &&  ./bin/buildout


# Yay! Zato installed! Lets get crackin on components!


# Copy the config files, ca and scripts over
COPY ./ca/ /opt/zato/ca/
COPY ./configs/ /opt/zato/configs/
COPY ./scripts/ /opt/zato/scripts/

EXPOSE 8183

# # Make scripts executable.
RUN chmod -R 755 /opt/zato/scripts/

# Environ vars
ENV ODB_NAME PLACE_YOUR_VALUE_HERE
ENV ODB_USER PLACE_YOUR_VALUE_HERE
ENV ODB_PASSWORD PLACE_YOUR_VALUE_HERE
ENV ODB_HOST PLACE_YOUR_VALUE_HERE
ENV ODB_PORT PLACE_YOUR_VALUE_HERE
ENV WA_PASSWORD PLACE_YOUR_VALUE_HERE
ENV KVDB_HOST PLACE_YOUR_VALUE_HERE
ENV KVDB_PORT PLACE_YOUR_VALUE_HERE
ENV KVDB_HOST2 PLACE_YOUR_VALUE_HERE
ENV KVDB_PORT2 PLACE_YOUR_VALUE_HERE
ENV CLUSTER_NAME PLACE_YOUR_VALUE_HERE
ENV CLUSTER_NAME2 PLACE_YOUR_VALUE_HERE
# Update the config files

# ODB Config
RUN sed -i "s/odb_db_name={{ODB_NAME}}/odb_db_name=$ODB_NAME/g" /opt/zato/configs/zato_odb.config
RUN sed -i "s/odb_password={{ODB_PASSWORD}}/odb_password=$ODB_PASSWORD/g" /opt/zato/configs/zato_odb.config
RUN sed -i "s/odb_host={{ODB_HOST}}/odb_host=$ODB_HOST/g" /opt/zato/configs/zato_odb.config
RUN sed -i "s/odb_port={{ODB_PORT}}/odb_port=$ODB_PORT/g" /opt/zato/configs/zato_odb.config
RUN sed -i "s/odb_user={{ODB_USER}}/odb_user=$ODB_USER/g" /opt/zato/configs/zato_odb.config

# update password Config
RUN sed -i "s/password={{WA_PASSWORD}}/password=$WA_PASSWORD/g" /opt/zato/configs/zato_update_password.config

# web_admin config
RUN sed -i "s/odb_db_name={{ODB_NAME}}/odb_db_name=$ODB_NAME/g" /opt/zato/configs/zato_web_admin.config
RUN sed -i "s/odb_password={{ODB_PASSWORD}}/odb_password=$ODB_PASSWORD/g" /opt/zato/configs/zato_web_admin.config
RUN sed -i "s/odb_host={{ODB_HOST}}/odb_host=$ODB_HOST/g" /opt/zato/configs/zato_web_admin.config
RUN sed -i "s/odb_port={{ODB_PORT}}/odb_port=$ODB_PORT/g" /opt/zato/configs/zato_web_admin.config
RUN sed -i "s/odb_user={{ODB_USER}}/odb_user=$ODB_USER/g" /opt/zato/configs/zato_web_admin.config

# Cluster1 config
RUN sed -i "s/broker_host={{KVDB_HOST}}/broker_host=$KVDB_HOST/g" /opt/zato/configs/zato_cluster.config
RUN sed -i "s/broker_port={{KVDB_PORT}}/broker_port=$KVDB_PORT/g" /opt/zato/configs/zato_cluster.config
RUN sed -i "s/odb_db_name={{ODB_NAME}}/odb_db_name=$ODB_NAME/g" /opt/zato/configs/zato_cluster.config
RUN sed -i "s/odb_password={{ODB_PASSWORD}}/odb_password=$ODB_PASSWORD/g" /opt/zato/configs/zato_cluster.config
RUN sed -i "s/odb_host={{ODB_HOST}}/odb_host=$ODB_HOST/g" /opt/zato/configs/zato_cluster.config
RUN sed -i "s/odb_port={{ODB_PORT}}/odb_port=$ODB_PORT/g" /opt/zato/configs/zato_cluster.config
RUN sed -i "s/odb_user={{ODB_USER}}/odb_user=$ODB_USER/g" /opt/zato/configs/zato_cluster.config
RUN sed -i "s/cluster_name={{CLUSTER_NAME}}/cluster_name=$CLUSTER_NAME/g" /opt/zato/configs/zato_cluster.config

# Cluster2 config
RUN sed -i "s/broker_host={{KVDB_HOST}}/broker_host=$KVDB_HOST2/g" /opt/zato/configs/zato_cluster2.config
RUN sed -i "s/broker_port={{KVDB_PORT}}/broker_port=$KVDB_PORT2/g" /opt/zato/configs/zato_cluster2.config
RUN sed -i "s/odb_db_name={{ODB_NAME}}/odb_db_name=$ODB_NAME/g" /opt/zato/configs/zato_cluster2.config
RUN sed -i "s/odb_password={{ODB_PASSWORD}}/odb_password=$ODB_PASSWORD/g" /opt/zato/configs/zato_cluster2.config
RUN sed -i "s/odb_host={{ODB_HOST}}/odb_host=$ODB_HOST/g" /opt/zato/configs/zato_cluster2.config
RUN sed -i "s/odb_port={{ODB_PORT}}/odb_port=$ODB_PORT/g" /opt/zato/configs/zato_cluster2.config
RUN sed -i "s/odb_user={{ODB_USER}}/odb_user=$ODB_USER/g" /opt/zato/configs/zato_cluster2.config
RUN sed -i "s/cluster_name={{CLUSTER_NAME}}/cluster_name=$CLUSTER_NAME2/g" /opt/zato/configs/zato_cluster2.config

# Create the ODB
RUN /opt/zato/scripts/zato_from_config_create_odb

# Create the cluster
RUN /opt/zato/scripts/zato_from_config_create_cluster

# Delete the old web-admin folder
RUN rm -rf /opt/zato/env/web-admin && mkdir -p /opt/zato/env/web-admin

# Create the web admin and update the password
RUN /opt/zato/scripts/zato_from_config_create_web_admin
RUN /opt/zato/scripts/zato_from_config_update_password

# Make the web admin publically accessable
RUN sed -i 's/127.0.0.1/0.0.0.0/g' /opt/zato/env/web-admin/config/repo/web-admin.conf

# Start the web admin
CMD ["/opt/zato/scripts/zato_start_web_admin"]
