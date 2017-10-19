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

# Prepare additional config files, CA certificates, keys and starter scripts
WORKDIR /opt/zato/
RUN mkdir /opt/zato/ca/
RUN mkdir /opt/zato/configs/
RUN mkdir /opt/zato/scripts/

# Copy the config files, ca and scripts over
COPY ./ca/ /opt/zato/ca/
COPY ./configs/ /opt/zato/configs/
COPY ./scripts/ /opt/zato/scripts/

# Expose the appropriate ports
EXPOSE 11223 20151 17011 17012 17013 17014

# # Make scripts executable.
RUN chmod -R 755 /opt/zato/scripts/

# Environment Variables
ENV CLUSTER_NAME PLACE_YOUR_VALUE_HERE
ENV JWT_SECRET PLACE_YOUR_VALUE_HERE
ENV ODB_NAME PLACE_YOUR_VALUE_HERE
ENV ODB_USER PLACE_YOUR_VALUE_HERE
ENV ODB_PASSWORD PLACE_YOUR_VALUE_HERE
ENV ODB_HOST PLACE_YOUR_VALUE_HERE
ENV ODB_PORT PLACE_YOUR_VALUE_HERE
ENV KVDB_HOST PLACE_YOUR_VALUE_HERE
ENV KVDB_PORT PLACE_YOUR_VALUE_HERE

# Delete the old load balancer if it exists
RUN rm -rf /opt/zato/env/load-balancer && mkdir -p /opt/zato/env/load-balancer

# Create the load balancer
RUN /opt/zato/scripts/zato_from_config_create_load_balancer

# Expose the load balancer publically
RUN sed -i 's/localhost/0.0.0.0/g' /opt/zato/env/load-balancer/config/repo/lb-agent.conf
RUN sed -i 's/127.0.0.1:11223/0.0.0.0:11223/g' /opt/zato/env/load-balancer/config/repo/zato.config

# Delete old server configs
RUN rm -rf /opt/zato/env/server1 && mkdir -p /opt/zato/env/server1
RUN rm -rf /opt/zato/env/server2 && mkdir -p /opt/zato/env/server2
RUN rm -rf /opt/zato/env/server3 && mkdir -p /opt/zato/env/server3
RUN rm -rf /opt/zato/env/server4 && mkdir -p /opt/zato/env/server4

# Update Server 1 config file
RUN sed -i "s/cluster_name={{CLUSTER_NAME}}/cluster_name=$CLUSTER_NAME/g" /opt/zato/configs/zato_server1.config
RUN sed -i "s/kvdb_host={{KVDB_HOST}}/kvdb_host=$KVDB_HOST/g" /opt/zato/configs/zato_server1.config
RUN sed -i "s/kvdb_port={{KVDB_PORT}}/kvdb_port=$KVDB_PORT/g" /opt/zato/configs/zato_server1.config
RUN sed -i "s/odb_db_name={{ODB_NAME}}/odb_db_name=$ODB_NAME/g" /opt/zato/configs/zato_server1.config
RUN sed -i "s/odb_password={{ODB_PASSWORD}}/odb_password=$ODB_PASSWORD/g" /opt/zato/configs/zato_server1.config
RUN sed -i "s/odb_host={{ODB_HOST}}/odb_host=$ODB_HOST/g" /opt/zato/configs/zato_server1.config
RUN sed -i "s/odb_port={{ODB_PORT}}/odb_port=$ODB_PORT/g" /opt/zato/configs/zato_server1.config
RUN sed -i "s/odb_user={{ODB_USER}}/odb_user=$ODB_USER/g" /opt/zato/configs/zato_server1.config
RUN sed -i "s/jwt_secret={{JWT_SECRET}}/jwt_secret=$JWT_SECRET/g" /opt/zato/configs/zato_server1.config

# Update Server 2 config file
RUN sed -i "s/cluster_name={{CLUSTER_NAME}}/cluster_name=$CLUSTER_NAME/g" /opt/zato/configs/zato_server2.config
RUN sed -i "s/kvdb_host={{KVDB_HOST}}/kvdb_host=$KVDB_HOST/g" /opt/zato/configs/zato_server2.config
RUN sed -i "s/kvdb_port={{KVDB_PORT}}/kvdb_port=$KVDB_PORT/g" /opt/zato/configs/zato_server2.config
RUN sed -i "s/odb_db_name={{ODB_NAME}}/odb_db_name=$ODB_NAME/g" /opt/zato/configs/zato_server2.config
RUN sed -i "s/odb_password={{ODB_PASSWORD}}/odb_password=$ODB_PASSWORD/g" /opt/zato/configs/zato_server2.config
RUN sed -i "s/odb_host={{ODB_HOST}}/odb_host=$ODB_HOST/g" /opt/zato/configs/zato_server2.config
RUN sed -i "s/odb_port={{ODB_PORT}}/odb_port=$ODB_PORT/g" /opt/zato/configs/zato_server2.config
RUN sed -i "s/odb_user={{ODB_USER}}/odb_user=$ODB_USER/g" /opt/zato/configs/zato_server2.config
RUN sed -i "s/jwt_secret={{JWT_SECRET}}/jwt_secret=$JWT_SECRET/g" /opt/zato/configs/zato_server2.config

# ODB Config
RUN sed -i "s/odb_db_name={{ODB_NAME}}/odb_db_name=$ODB_NAME/g" /opt/zato/configs/zato_odb.config
RUN sed -i "s/odb_password={{ODB_PASSWORD}}/odb_password=$ODB_PASSWORD/g" /opt/zato/configs/zato_odb.config
RUN sed -i "s/odb_host={{ODB_HOST}}/odb_host=$ODB_HOST/g" /opt/zato/configs/zato_odb.config
RUN sed -i "s/odb_port={{ODB_PORT}}/odb_port=$ODB_PORT/g" /opt/zato/configs/zato_odb.config
RUN sed -i "s/odb_user={{ODB_USER}}/odb_user=$ODB_USER/g" /opt/zato/configs/zato_odb.config

# Cluster config
RUN sed -i "s/broker_host={{KVDB_HOST}}/broker_host=$KVDB_HOST/g" /opt/zato/configs/zato_cluster.config
RUN sed -i "s/broker_port={{KVDB_PORT}}/broker_port=$KVDB_PORT/g" /opt/zato/configs/zato_cluster.config
RUN sed -i "s/odb_db_name={{ODB_NAME}}/odb_db_name=$ODB_NAME/g" /opt/zato/configs/zato_cluster.config
RUN sed -i "s/odb_password={{ODB_PASSWORD}}/odb_password=$ODB_PASSWORD/g" /opt/zato/configs/zato_cluster.config
RUN sed -i "s/odb_host={{ODB_HOST}}/odb_host=$ODB_HOST/g" /opt/zato/configs/zato_cluster.config
RUN sed -i "s/odb_port={{ODB_PORT}}/odb_port=$ODB_PORT/g" /opt/zato/configs/zato_cluster.config
RUN sed -i "s/odb_user={{ODB_USER}}/odb_user=$ODB_USER/g" /opt/zato/configs/zato_cluster.config
RUN sed -i "s/cluster_name={{CLUSTER_NAME}}/cluster_name=$CLUSTER_NAME/g" /opt/zato/configs/zato_cluster.config

# Create the servers
RUN /opt/zato/scripts/zato_from_config_create_servers

# Update the workers and set the ports
RUN sed -i 's/0.0.0.0:17010/0.0.0.0:17011/g' /opt/zato/env/server1/config/repo/server.conf
RUN sed -i 's/0.0.0.0:17010/0.0.0.0:17012/g' /opt/zato/env/server2/config/repo/server.conf

RUN sed -i 's/gunicorn_workers=2/gunicorn_workers=1/g' /opt/zato/env/server1/config/repo/server.conf
RUN sed -i 's/gunicorn_workers=2/gunicorn_workers=1/g' /opt/zato/env/server2/config/repo/server.conf

USER root
CMD /usr/bin/supervisord -c /opt/zato/configs/supervisord.conf
