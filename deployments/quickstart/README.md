# Zato Quickstart
This is based off of [this](https://zato.io/docs/admin/guide/install/docker.html)

I only use this as a dev environment, you should too ;)

### Starting it up
If you have `docker-compose` installed then you can start this by typing `docker-compose up`. This will build everything for you and get everything running. Just give it some time. 

If you don't have docker-compose then you can do this. 
```
docker build -t zato .
```
Then you need to get the web admin password
```
docker run -it zato cat /opt/zato/web_admin_password /opt/zato/zato_user_password
```
Now the documentation says you should run the container after this, you should rather create a volume first (especaily if you don't use `docker-compose`. This will give you persistant storage when you stop and start the service. Its a pain to have to readd all your endpoints, services and things everytime you start zato.

```
docker volume create zato
```
Now we can start the container
```
docker run -it -v zato:/opt/zato -p 8183:8183 -p 8183:8183 zato
```

Once complete, you can log in to your web admin by going to `http://localhost:8183/`

