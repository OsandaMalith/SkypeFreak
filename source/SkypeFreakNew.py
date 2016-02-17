#!/usr/bin/python
from __future__ import print_function
import os
import sqlite3
import sys
import time
try:
    input = raw_input
except:
    pass
'''
Title: SkypeFreak
Description: A cross platform forensic tool for Skype
Author: Osanda Malith (@OsandaMalith) 
URL: http://osandamalith.github.io/SkypeFreak/

Disclaimer: This tool is meant for ethical (legal) purposes only.

Notes:  Please note this tool may contain errors, and
    is provided "as it is". There is no guarantee
    that it will work on your target systems(s), as
    the code may have to be adapted. 
    This is to avoid script kiddie abuse as well.
    
License:
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
 
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
 
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
contributors = [

    'Special thanks to Muhammad Yasoob Ullah Khalid @yasoobkhalid for improving\nthe code and extending support'
]

class SkypeJunk(object):
    '''
        This is the main object which contains all of the required functions.
        It contains the following methods:
        *) __init__(self,db)
        *) _get_profile(self)
        *) _get_contacts(self)
        *) _get_calls(self)
        *) _get_msgs(self)
        *) _gen_report(self)
        *) _gen_full_report(self)
        *) _put_to_file(self,filename,data)
        *) _get_choice(self)
        *) _get_save_choice(self)
        
        You just need to pass a skype database path which instantiating this class. 
        For example SkypeJunk('/home/<username>/.Skype/<skype username>/main.db').
        After that you can use any method from this class.
    '''

    def __init__(self,skypedb,pathname):
        self.db     = skypedb
        self.con    = sqlite3.connect(self.db)
        self.path   = pathname
        self.name   = os.path.basename(self.path)
        self.type_of= None

    def _get_profile(self):
        with self.con:
            cur     = self.con.cursor()
            data    = cur.execute("SELECT fullname, skypename, city, country,\
            datetime(profile_timestamp,'unixepoch') FROM Accounts")
        
        for row in data:
            self.details = {
                '[+] User        '          :   str(row[0].encode('utf-8')),
                '[+] Skype Username'    :   str(row[1]),
                '[+] Country        '       :   str(row[2].encode('utf-8')) or "unknown",
                '[+] Location    '      :   str(row[3].encode('utf-8')),
                '[+] Profile Date'  :   str(row[4])
            }
        self.type_of = "profile"
        return self.details

    def _get_contacts(self):
        with self.con:
            cur     =   self.con.cursor()
            data    =   cur.execute("SELECT displayname, skypename, country, city, about, phone_mobile,\
            homepage, birthday , datetime(lastonline_timestamp,'unixepoch') FROM Contacts;")
        self.details = {}
        for count,row in enumerate(data):
            self.details[count] = {}
            self.details[count]['[+] User          '] = str(row[0].encode('utf-8'))
            self.details[count]['[+] Skype Username'] = str(row[1])
            if row[2]:
                self.details[count]['[+] Country       '] = str(row[2].encode('utf-8'))
            elif row[3]:
                self.details[count]['[+] City    '] = str(row[3].encode('utf-8'))
            elif row[4]:
                self.details[count]['[+] About        '] = str(row[4].encode('utf-8'))
            elif row[5]:
                self.details[count]['[+] Mobile No    '] = str(row[5])
            elif row[6]:
                self.details[count]['[+] Homepage'] = str(row[6].encode('utf-8'))
            elif row[7]:
                self.details[count]['[+] Birthday'] = str(row[7])
            elif row[8]:
                self.details[count]['[+] Last Online'] = str(row[8])

        self.type_of = "contacts"
        return self.details

    def _get_calls(self):
        with self.con:
            cur     =   self.con.cursor()
            data    =   cur.execute("SELECT datetime(begin_timestamp,'unixepoch'), \
                        time(duration,'unixepoch'), is_incoming, identity  FROM calls, \
                        conversations WHERE calls.conv_dbid = conversations.id;")
        self.details = {}
        for count, row in enumerate(data):
            self.details[count] = row
        self.type_of = "calls"
        return self.details

    def _get_msgs(self):
        with self.con:
            cur     =   self.con.cursor()
            data    =   cur.execute("SELECT datetime(timestamp,'unixepoch'), \
                        dialog_partner, author, body_xml FROM Messages;")
        self.details = {}
        for count, row in enumerate(data):
            try:
                if 'partlist' not in str(row[3]):
                    if str(row[1]) != str(row[2]):
                        msgDirection = ['[+] To\t', str(row[1])]
                    else:
                        msgDirection = ['[+] From', str(row[2])]
                    self.details[count] = {
                        msgDirection[0] : msgDirection[1],
                        '[+] Time'      : str(row[0]),
                        '[+] Message'       : str(row[3]).encode('utf-8').replace('&apos;',"'")
                    }
            except:
                pass
        self.type_of = "msgs"
        return self.details

    def __status(self,num):
        if num == 0:
            return "Outgoing"
        elif num == 1:
            return "Incomming"
        else:
            return num

    def _get_contributors(self):
        print('\nContributors:\n')
        for one in contributors:
            print(one)
        sys.exit(0)

    def _gen_report(self):
        data = ''
        if self.type_of == "profile":
            data += '\n[*] ----- Found The Profile ----- \n\n'            
            for i in self.details:
                data += i+'\t'+': '+self.details[i]+'\n' 
            return data
        elif self.type_of == "contacts":
            data += '\n[*] ----- Found {0} Contacts ----- \n'.format(len(self.details))
            for i in self.details:
                data += '\n'
                for single in self.details[i]:
                    data += single+'\t'+': '+self.details[i][single]+'\n'
            return data
        elif self.type_of == "calls":
            formating = ['[+] Date\t','[+] Duration','[+] Status\t','[+] User\t']
            data += '\n[*] ----- Found {0} Calls ----- '.format(len(self.details))+'\n'
            for i in self.details:
                data += "\n"
                for c,single in enumerate(self.details[i]):
                    data += formating[c]+'\t: '+str(self.__status(single))+'\n'
            return data
        elif self.type_of == "msgs":
            data += '\n[*] ----- Found {0} Messages ----- '.format(len(self.details))+'\n'
            for i in self.details:
                data += '\n'
                for single in self.details[i]:
                    data += single+'\t: '+self.details[i][single]+"\n"
            return data

    def _gen_full_report(self):
        self._get_profile()
        data = self._gen_report()
        self._get_contacts()
        data += '\n'+self._gen_report()
        self._get_calls()
        data += '\n'+self._gen_report()
        self._get_msgs()
        data += '\n'+self._gen_report()+'\n'
        print(data)
        self._get_save_choice(data)

    def _put_to_file(self,file,data):
        data += "\n[*] This file was Generated by Skype Freak\n[~] http://osandamalith.github.io/SkypeFreak/"
        with open(file,'wb') as f:
            f.write(data.encode('utf-8'))

    def _get_choice(self):
        choice = None
        while choice is None:
            try:
                choice = int(input("[~] What Do You Like to Investigate? \
                    \n1. Profile\n2. Contact\n3. Calls\n4. Messages\n5. Generate Full Report\n\
6. Print the list of contributors & exit\n7. Exit\n" ))
            except ValueError:
                print('[!] Enter Only a Number')
        choices = {
            1   :   self._get_profile,
            2   :   self._get_contacts,
            3   :   self._get_calls,
            4   :   self._get_msgs,
            5   :   self._gen_full_report,
            6   :   self._get_contributors,
            7   :   sys.exit
        }
        if choice not in [5,6]:
            choices.get(choice,sys.exit)()
            data = self._gen_report()
            print(data)
            self._get_save_choice(data)
        else:
            choices.get(choice,sys.exit)()

    def _get_save_choice(self,data):
        choice = None
        while True:
            choice = input('[~] Would you like to save these results in a file?  ')
            if 'y' in choice:
                filename = input('[~] What should be the name of the file?  ')
                self._put_to_file(filename,data)
                print('[*] All of the data is saved')
                time.sleep(1)
                break
            elif 'n' in choice:
                break
            else:
                print('[!] You selected wrong option.\n[!] Please try again!')
        print('out of while choices_save')

def clear_screen():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')

def print_banner():
    print('''
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

''')
    print('[*] A creation of Osanda Malith \n\
[*] Follow @OsandaMalith \n\
[*] URL: http://osandamalith.github.io/SkypeFreak/\n')

def main():
    clear_screen()
    username = input('[~] Enter your Skype Username: ')
    clear_screen()
    try:
        db,path = gen_path(username)
    except TypeError:
        print('[!] The name you entered was not correct')
        sys.exit(0)
    skype = SkypeJunk(db,path)
    try:
        while True:
            print_banner()
            skype._get_choice()
            clear_screen()
    except KeyboardInterrupt:
        print('\n[!] Got Ctrl+C key. Shutting down gracefully\n')
        sys.exit(0)

def gen_path(username):
    if os.name == "nt":
        PathName = os.getenv('appdata') + "\\Skype\\" + username
    elif os.name == "posix":
        PathName = os.getenv('HOME') + "/.Skype/" + username
    if PathName == None : 
        print('[!] Please Enter a valid Skype username ')
    elif ((os.name == "posix") and (os.path.isdir(PathName) == False)):
        PathName = os.getenv('HOME') + "/Library/Application Support/Skype/" + username
        skypeDB = os.path.join(PathName, 'main.db')
        if os.path.isfile(skypeDB):
            return skypeDB,PathName
    elif os.path.isdir(PathName) == False:
        print('[!] Username Does Not Exist ')
    else:
        skypeDB = os.path.join(PathName, 'main.db')
        if os.path.isfile(skypeDB):
            return skypeDB,PathName

if __name__ == '__main__':
    main()
