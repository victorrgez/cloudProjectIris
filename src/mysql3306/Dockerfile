FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=cloudprojectiris
ENV MYSQL_USER=webapp
ENV MYSQL_PASSWORD=webapp

ADD setup.sql /docker-entrypoint-initdb.d/setup.sql

EXPOSE 3306 33060

#docker run -d -p=0.0.0.0:3306:3306 --name mysql victorrgez/cloudprojectirismysql