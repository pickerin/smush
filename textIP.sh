#!/bin/bash
# Texts current IP address to a recipient.
# Update wget line with SmushBox username/password, currently set to smushbox/smushbox
#Last known IP address
IPFILE=/tmp/ipaddress
#Sleep to ensure IP address is configured.
sleep 60
#Retrieve and assign Public IP address to PUBLIC_IP
PUBLIC_IP=$(wget -q -O - http://icanhazip.com)
#Retrieve and assign Private IP address to PRIVATE_IP
PRIVATE_IP=$(ifconfig | grep -Po "inet addr:.+Bcast" | grep -Po '(?:\d{1,3}\.){3}\d{1,3}' | sed ':a;N;s/\n/+/g')
DATUM="$(date)"
#Assign the phone number, change to recipient mobile phone
SMSNUM="5135551212"
#Verify that ipaddress file exists, compare to the current, update file
if [ -f $IPFILE ]; then
KNOWN_IP=$(cat $IPFILE)
else
KNOWN_IP=
fi
if [ "$PRIVATE_IP" != "$KNOWN_IP" ]; then
echo $PRIVATE_IP > $IPFILE
#Customize message
/usr/bin/wget --quiet --output-document=output.log "http://localhost/messagelist/send?number=${SMSNUM}&message=Current+Private+IP+address+is+:+$PRIVATE_IP&username=smushbox&password=smushbox"
logger -t ipcheck -- IP changed to $PRIVATE_IP
else
logger -t ipcheck -- No IP change
fi
