#!/usr/bin/python
# smush.py - Manage and Interface a SmushBox
import argparse, re, json, sys, urllib2, time
from datetime import datetime
from datetime import timedelta
__author__ = 'RobPickering.com'
 
# Define functions

# Process Errors
def handleError( e ):
   print ("Error: %s" % e)
   return

# Connect to SmushBox
def smushBox(url):
   try:
     result = json.load(urllib2.urlopen(url))
     if result['success']:
        return result
     else:
        print result['errors']
   except urllib2.URLError, e:
     handleError(e)
   sys.exit()

def sendText():
   # Replace spaces in the Text Message with Plus signs
   message = re.sub('[ ]', '+', args.message)
   # Text Message is limited to 160 characters (at this time)
   message = (message[:157] + '...') if len(message) > 160 else message
   url = 'http://'+args.host+'/messagelist/send?number='+args.number+'&message='+message+'&username='+username+'&password='+password   
   result = smushBox(url)
   if result['success']:
      print result['message']
   else: 
      print result['errors']
   sys.exit()

def listIncoming():   
   url = 'http://'+args.host+'/messagelist/list/incoming/al?&username='+username+'&password='+password
   result = smushBox(url)
   if result['success']:
      print "#\tPhone Number\tDate\t\t\tRead\tMessage"
      for message in result['message']:
         print "%s\t%s\t%s\t%s\t%s" % (message['phone_id'],message['number'],message['format_time'],message['read'],message['message'])
   else: 
      print result['errors']
   sys.exit()

def listOutgoing():
   url = 'http://'+args.host+'/messagelist/list/outgoing/all?username='+username+'&password='+password
   result = smushBox(url)
   if result['success']:
      print "#\tMessage ID\tPhone Number\tDate\t\t\tMessage"
      for message in result['message']:
         print "%s\t%s\t\t%s\t%s\t%s" % (message['phone_id'],message['message_id'],message['number'],message['format_sent'],message['message'])
   else: 
      print result['errors']
   sys.exit()

def listContacts():
   url = 'http://'+args.host+'/phonebook/list?username='+username+'&password='+password
   result = smushBox(url)
   if result['success']:
      print "#\tPhone Number\tDisabled\tGroup"
      for contact in result['message']:
         print "%s\t%s\t%s\t\t%s" % (contact['phone_id'],contact['number'],contact['disabled'],contact['group_member'])
   else: 
      print result['errors']
   sys.exit()

def checkUpdate():
   statusUrl = 'http://'+args.host+'/system/systemstats?username='+username+'&password='+password
   status = smushBox(statusUrl)
   if status['success']:
      url = 'http://'+args.host+'/system/checkforfirmwareupdate?username='+username+'&password='+password
      result = smushBox(url)
      if result['success']:
         print "System version:   ",status['message']['version']
         print "Current version:  ",result['message']['version']
         if float(status['message']['version']) == float(result['message']['version']):
            return 0
         else:
            return 1
      else: 
         print result['errors']
         sys.exit()
   else: 
      print result['errors']
   sys.exit()
	
def checkStatus():
   url = 'http://'+args.host+'/system/systemstats?username='+username+'&password='+password
   result = smushBox(url)
   if result['success']:
      print "Uptime:        %s" % niceTime(int(result['message']['uptime']))
      print "Time Zone:    ",result['message']['timezone_id']
      print "System Time:  ",result['message']['system_time']
      print "Local Time:   ",result['message']['local_time']
      print "OS Version:    v%s" % result['message']['version']
      print "Signal Level:  %.2f%%" % (float(result['message']['signal_level']) / 0.32)
      print "IMEI:         ",result['message']['IMEI']
   else: 
      print result['errors']
   sys.exit()   

def performUpgrade():
   statusUrl = 'http://'+args.host+'/system/updatetolatestfirmware?username='+username+'&password='+password
   print "About to upgrade SmushBox, this process may take a few minutes, do not interrupt."
   status = smushBox(statusUrl)
   print status
   sys.exit()

# Credit to SmushMobile for the Javascript version of this code
def niceTime( totalSec ):
	days = int( totalSec / (3600 * 24) )
	hours = int( totalSec / 3600 ) % 24
	minutes = int( totalSec / 60 ) % 60
	seconds = totalSec % 60

	result = ""
	if (days != 0):
		result = "%s" % days + " day" + ("s" if days > 1 else "") + ", %s" % hours + " hour" + ("s" if hours > 1 else "") + ", %s" % minutes + " minute" + ("s" if minutes > 1 else "") + ", %s" % seconds + " second" + ("s" if seconds > 1 else "")
	elif (hours != 0):
		result = "%s" % hours + " hour" + ("s" if hours > 1 else "") + ", %s" % minutes + " minute" + ("s" if minutes > 1 else "") + ", %s" % seconds + " second" + ("s" if seconds > 1 else "")
	elif (minutes != 0):
		result = "%s" % minutes + " minute" + ("s" if minutes > 1 else "") + ", %s" % seconds + " second" + ("s" if seconds > 1 else "")
	else:
		result = "%s" % seconds + " second" + ("s" if seconds > 1 else "")
	return result
	
# Add valid arguments to application
parser = argparse.ArgumentParser(description='Manage a SmushBox by RobPickering.com.',epilog='Example: smush.py 172.31.20.5 -t -n 6145551212 -m "Testing 123"')
parser.add_argument('host',help='SmushBox IP or FQDN')
group = parser.add_mutually_exclusive_group()
text_group = group.add_argument_group()
text_group.add_argument('-t','--text',help='Send SMS message',action='store_true')
text_group.add_argument('-n','--number',help='Recipient mobile number',required=False)
text_group.add_argument('-m','--message',help='Text message to send, use quoted string',required=False)
group.add_argument('-i','--incoming',help='Display all incoming messages',action='store_true')
group.add_argument('-o','--outgoing',help='Display all outgoing messages',action='store_true')
group.add_argument('-c','--contacts',help='Display phonebook',action='store_true')
group.add_argument('-cu','--checkupdate',help='Check for available update',action='store_true')
group.add_argument('-pu','--performupgrade',help='Upgrade your SmushBox, performs --checkupdate first',action='store_true')
group.add_argument('-s','--status',help='Retrieve SmushBox status',action='store_true')
group.add_argument('-do','--deleteout',help='Deletes message DELETEOUT (# or all) -- Not implemented yet',required=False)
group.add_argument('-v', '--version', action='version', version='%(prog)s 1.2')
authgroup = parser.add_argument_group('authentication')
authgroup.add_argument('-u','--username',help='SmushBox username, defaults to "smushbox"',required=False)
authgroup.add_argument('-p','--password',help='SmushBox password, defaults to "smushbox"',required=False)

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

# Send a Text (SMS) Message
if args.text:
   sendText()   
# List incoming messages   
elif args.incoming:
   listIncoming()   
# List outgoing messages   
elif args.outgoing:
   listOutgoing()   
# List contacts   
elif args.contacts:
   listContacts()   
# Check for available update   
elif args.checkupdate:
   if checkUpdate():
      print "Update available: ",result['message']['URL']
   else:
      print "No update available"   
# Perform upgrade, if available   
elif args.performupgrade:
   if checkUpdate():
      print "Upgrading via: ",result['message']['URL']
      performUpgrade()
   else:
      print "No update available, not upgrading."   
# Provide SmushBox status   
elif args.status:
   checkStatus()   
# Delete outgoing messages   
elif args.deleteout:
   url = 'http://'+args.host+'/messagelist/delete/outgoing/all?username='+username+'&password='+password
   smushBox(url)
   sys.exit()
else:
   print "Command options not understood."