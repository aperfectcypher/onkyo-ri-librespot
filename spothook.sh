#!/bin/bash

exec >> /opt/onkyo/spothook.log
exec 2>&1

echo $PLAYER_EVENT > /opt/onkyo/event_fifo
echo $VOLUME > /opt/onkyo/volume_fifo
