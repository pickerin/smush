#!/usr/bin/python
# smush.py - Manage and Interface a SmushBox
import argparse, re, sys, urllib2
__author__ = 'RobPickering.com'
 
# Define functions

# Process SmushBox JSON Response
def processJSON( result ):
   print ("Result: %s" % result)
   return

# Process Errors
def handleError( e ):
   print ("Error: %s" % e)
   return

# Connect to SmushBox
def smushBox(url):
   try:
     result = urllib2.urlopen(url)
     print result.read()
   except urllib2.URLError, e:
     handleError(e)
   sys.exit()


# Add valid arguments to application
parser = argparse.ArgumentParser(description='Manage a SmushBox by RobPickering.com.')
parser.add_argument('host',help='SmushBox IP or FQDN')
group = parser.add_mutually_exclusive_group()
text_group = group.add_argument_group()
text_group.add_argument('-t','--text',help='Send SMS message',action='store_true')
text_group.add_argument('-n','--number',help='Recipient mobile number',required=False)
text_group.add_argument('-m','--message',help='Text message to send, use quoted string',required=False)
group.add_argument('-i','--incoming',help='SmushBox incoming messages',action='store_true')
group.add_argument('-o','--outgoing',help='SmushBox outgoing messages',action='store_true')
group.add_argument('-c','--contacts',help='SmushBox phonebook',action='store_true')
parser.add_argument('-u','--username',help='SmushBox username',required=False)
parser.add_argument('-p','--password',help='SmushBox password',required=False)

# Define defaults (will be overridden by options above)
username = "smushbox"
password = "smushbox"

# Grab arguments
args = parser.parse_args()

# Override defaults with options

if args.username:
   username = args.username

if args.password:
   password = args.password

# If message is defined, then user must want to send a message
if args.text:
   # Replace spaces in the Text Message with Plus signs
   message = re.sub('[ ]', '+', args.message)
   # Text Message is limited to 160 characters (at this time)
   message = (message[:157] + '...') if len(message) > 160 else message
   url = 'http://'+args.host+'/messagelist/send?number='+args.number+'&message='+message+'&username='+username+'&password='+password   
   smushBox(url)
   
if args.incoming:
   url = 'http://'+args.host+'/messagelist/list/incoming/all&username='+username+'&password='+password
   smushBox(url)

if args.outgoing:
   url = 'http://'+args.host+'/messagelist/list/outgoing/all&username='+username+'&password='+password
   smushBox(url)

if args.contacts:
   url = 'http://'+args.host+'/phonebook/list&username='+username+'&password='+password
   smushBox(url)

