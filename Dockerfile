FROM python:3-buster

# RUN apk add --no-cache -X http://dl-cdn.alpinelinux.org/alpine/edge/testing nut
RUN apt-get update && apt-get install -y nut usbutils


WORKDIR /usr/src/app

COPY ./nut-config/* /etc/nut/

RUN chmod -R 777 /etc/nut/

COPY ./scripts ./scripts

RUN pip3 install -r scripts/requirements.txt


ENV INFLUX_HOST influx.xrho.com
ENV INFLUX_PORT 8086
ENV INFLUX_DB ups-generic
ENV UPS_NAME amazonbasics


CMD /usr/src/app/scripts/ups-monitor.py \
	--influx_host $INFLUX_HOST \
	--influx_port $INFLUX_PORT \
	--influx_db $INFLUX_DB \
	--ups_name $UPS_NAME