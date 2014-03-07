import os, sqlite3, optparse
import sys



def Profile(skypeDB, PathName):
	connexion = sqlite3.connect(skypeDB)
	c = connexion.cursor()
	c.execute("SELECT fullname, skypename, city, country,\
		datetime(profile_timestamp,'unixepoch') FROM Accounts")
	for row in c:
		print '[*] --- Details of %s' % (os.path.basename(PathName)) +' ---'
		print '[+] User: %s ' %(str(row[0]))
		print '[+] Skype Username: %s'%(str(row[1]))
		print '[+] Country: %s' % (str(row[2]))
		print '[+] Location: %s'% (str(row[3]))
		print '[+] Profile Date: %s'%(str(row[4]))


def Contacts(skypeDB):
	connexion = sqlite3.connect(skypeDB)
	c = connexion.cursor()
	c.execute("SELECT displayname, skypename, country, city, about, phone_mobile, homepage, \
		birthday , datetime(lastonline_timestamp,'unixepoch') FROM Contacts;")
	for row in c:
		print '\n[*] --- Found Contact --- '
		print '[+] User: %s' %(str(row[0]))
		print '[+] Skype Username: %s' %(str(row[1]))
		if str(row[2])!= 'None':
			print '[+] Country: %s' %(str(row[2]))
		if str(row[3])!= 'None':
			print '[+] City: %s' %(str(row[3]))
		if str(row[4])!= 'None':
			print '[+] About Text: %s' %(str(row[4]))
		if str(row[5])!= 'None':
			print '[+] Mobile Number: %s' %(str(row[5]))
		if str(row[6])!= 'None':
			print '[+] Homepage URL: %s' %(str(row[6]))
		if str(row[7])!= 'None':
			print '[+] Birthday: %s' %(str(row[7]))
		if str(row[8])!= 'None':
			print '[+] Last Online Date: %s' %(str(row[8]))

def Calls(skypeDB):
	connexion = sqlite3.connect(skypeDB)
	c = connexion.cursor()
	c.execute("SELECT datetime(begin_timestamp,'unixepoch'), identity  FROM calls, \
		conversations WHERE calls.conv_dbid = conversations.id;")
	for row in c:
		print '\n[*] --- Found Calls --- '
		print '[+] Call Duration: %s'%(str(row[0]))+ ' | Partner: %s' %(str(row[1]))

def Msgs(skypeDB):
	connexion = sqlite3.connect(skypeDB)
	c = connexion.cursor()
	c.execute("SELECT datetime(timestamp,'unixepoch'), \
		dialog_partner, author, body_xml FROM Messages;")
	for row in c:
		try:
			if 'partlist' not in str(row[3]):
				if str(row[1]) != str(row[2]):
					msgDirection = 'To ' + str(row[1]) + ': '
				else:
					msgDirection = 'From ' + str(row[2]) + ': '
				print 'Time: ' + str(row[0]) + ' ' \
				+ msgDirection + str(row[3])
		except:
			pass

def banner():
	print '''
8""""8                         
8      e   e  e    e eeeee eeee
8eeeee 8   8  8    8 8   8 8   
    88 8eee8e 8eeee8 8eee8 8eee
e   88 88   8   88   88    88  
8eee88 88   8   88   88    88ee
                               
	8""""                         
	8     eeeee  eeee eeeee e   e 
	8eeee 8   8  8    8   8 8   8 
	88    8eee8e 8eee 8eee8 8eee8e
	88    88   8 88   88  8 88   8
	88    88   8 88ee 88  8 88   8

'''
	print  '%s' %('Coded by @OsandaMalith') + '\n'


def main():
	#os.system('color 17')
	parser = optparse.OptionParser("usage: %prog -u <skype username> ")
	parser.add_option('-u', dest='PathName', type='string',	help='Specify Skype Username  [default: %default]')
	(options, args) = parser.parse_args()

	PathName = os.getenv('appdata') + "\\Skype\\" +options.PathName
	print "Path : " + PathName + '\n'
	if PathName == None : 
		print parser.usage
		exit(0)
	elif os.path.isdir(PathName) == False:
		print >>stream, Fore.RED + '[!] Path Does Not Exist: ' 
		exit(0)
	else:
		skypeDB = os.path.join(PathName, 'main.db')
		print "Location of DB: " + skypeDB + '\n'
		if os.path.isfile(skypeDB):
			banner()
			Profile(skypeDB, PathName)
			Contacts(skypeDB)
			Calls(skypeDB)
			Msgs(skypeDB)
		else:
			print >> stream, Fore.RED + '[!] Skype Database '+\
			'does not exist: ' 

if __name__ == "__main__": 
	main()	