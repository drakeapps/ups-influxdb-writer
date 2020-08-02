#! /bin/sh -e

lsusb

mkdir -m 2750 /dev/shm/nut
chown $USER.$GROUP /dev/shm/nut
[ -e /var/run/nut ] || ln -s /dev/shm/nut /var/run
# Issue #15 - change pid warning message from "No such file" to "Ignoring"
echo 0 > /var/run/nut/upsd.pid && chown $USER.$GROUP /var/run/nut/upsd.pid
echo 0 > /var/run/nut/upsmon.pid

upsdrvctl -u root start
upsd -u root
exec upsmon -D

/usr/src/app/scripts/ups-monitor.py \
	--influx_host $1 \
	--influx_port $2 \
	--influx_db $3 \
	--ups_name $4