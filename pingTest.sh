#!/bin/sh
# 
# Use with following CRON job:
# */5 * * * * /home/ubuntu/pingTest.sh
#
# -q quiet
# -c nb of pings to perform

# Make sure to update the wget line with the username and password of the smushbox, currently set at default 
# of smushbox/smushbox

# Replace gateway with the default gateway of the SmushBox
GATEWAY=172.16.1.1
# Replace SMSNUM with the recipient number you wish to notify
SMSNUM=5135551212
 
ping -q -c5 $GATEWAY > /dev/null
 
if [ $? -ne 0 ]
then
        /usr/bin/wget --quiet --output-document=output.log "http://localhost/messagelist/send?number=${SMSNUM}&message=No+network+access&username=smushbox&password=smushbox"
fi
