#!/bin/sh

#sudo mkdir -p /var/log/microdom
#sudo chmod 0777 /var/log/microdom
#sudo cp -uva etc/microdom.conf /etc

echo "Building microdom-cloud-alexa docker image..."
docker build -t microdom-cloud-alexa .
echo "Stop microdom-cloud-alexa..."
docker stop microdom-cloud-alexa
sleep 1
echo "Remove microdom-cloud-alexa..."
docker rm microdom-cloud-alexa
sleep 1
docker run -it \
  -d --restart unless-stopped \
  -e DBUSER=dompi_cloud \
  -e DBPASSWORD=dompi_cloud \
  -e DBHOST=192.168.10.32 \
  -e DBNAME=DB_DOMPICLOUD \
  --name microdom-cloud-alexa \
  -v /var/log/microdom:/app/logs \
  -p 8083:8083 microdom-cloud-alexa
