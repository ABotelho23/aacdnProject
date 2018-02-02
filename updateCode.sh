#!/bin/bash
git pull https://github.com/ABotelho23/aacdnProject $HOSTNAME
sudo cp coap.service /etc/avahi/services/coap.service
