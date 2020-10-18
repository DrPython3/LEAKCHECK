#!/usr/local/bin/python3
#encoding: utf-8
#name: leakcheck
#description: checks given combolists against a private lib of leaks
#version: 0.1 / 2020-10-16
#author: DrPython3
#todo: write dbcount(), write new function for maintining the db and much more ...

#((<-- *** NEEDED MODULES *** -->))

import ctypes, os, sys, threading
import colorama
from colorama import *
init()
print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '')

#((<-- *** VARIOUS STUFF *** -->))

public = 0 #for stats in title bar
private = 0 #for stats in title bar
leakcount = 0 #for counting leaks in db
leakdic = [] #for counting leaks in db
combofile = '' #file with combos for checker, updater etc.
newcount = 0 #new combos processed by checker, updater etc.
newleaks = [] #combos to check, import etc.

logo1 = '''
@@@      @@@@@@@@  @@@@@@  @@@  @@@  @@@@@@@ @@@  @@@ @@@@@@@@  @@@@@@@ @@@  @@@
@@!      @@!      @@!  @@@ @@!  !@@ !@@      @@!  @@@ @@!      !@@      @@!  !@@
@!!      @!!!:!   @!@!@!@! @!@@!@!  !@!      @!@!@!@! @!!!:!   !@!      @!@@!@!
!!:      !!:      !!:  !!! !!: :!!  :!!      !!:  !!! !!:      :!!      !!: :!!
: ::.: : : :: ::   :   : :  :   :::  :: :: :  :   : : : :: ::   :: :: :  :   ::: '''

logo2 = '''
________________________________________________________________________________
           personal antipublic db with checker | DrPython3 (C) 2020

   support this tool with donations (BTC): 1M8PrpZ3VFHuGrnYJk63MtoEmoJxwiUxYf
           (!) all donations help with providing future updates (!)'''

mainmenu = '''

             ### -- M*A*I*N   M*E*N*U -- ###
----------------------------------------------------------
[1] Check your Combofile for Public Leaks and clean it up.
[2] Add Combos to Database without.
[3] Status of your Personal DB.
[4] Maintain DB (delete duplicates etc).
----------------------------------------------------------
[0] Any other input: << QUIT >>
'''

exitmsg = '''

... your choice: (!) QUIT LEAKCHECK (!)

Do you like the tool?
Then send a donation, please: (BTC) 1MiKuJrTCNST3haCX6sCnmMWTxJ4ZXtYgw
All donations help with providing future updates and upgrades.'''

#((<-- *** FUNCTIONS *** -->))

#cleaner - clear screen on purpose:
def cleaner():
    try:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    except:
        pass

#menu - screen with main menu for user:
def menu():
    cleaner()
    print(Fore.LIGHTWHITE_EX + Style.BRIGHT + mainmenu)
    what = input(Fore.LIGHTYELLOW_EX + Style.BRIGHT + '\nYOUR CHOICE: ')
    if what == 1:
        dbcheck()
        #TODO: write function dbcheck()
    elif what == 2:
        dbupdate()
    elif what == 3:
        dbcount()
    else:
        cleaner()
        sys.exit(Fore.LIGHTRED_EX + Style.BRIGHT + exitmsg)

#dbcount - delivers amount of leaks currently saved in db, actually not in use:
def dbcount():
    global leakcount
    cleaner()
    print(Fore.LIGHTWHITE_EX + Style.BRIGHT + '\nWait a moment, please (...)\n')
    try:
        leakdic = open('leak.db', 'r').read().splitlines()
        vics1 = len(leakdic)
        leakcount = int(vics1)
        leakdic.clear()
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'TOTAL AMOUNT OF LEAKS IN DB: ' + str(leakcount) + '\n')
        input(Fore.LIGHTWHITE_EX + Style.BRIGHT + '\nPress [ENTER] to return to main menu.')
        return None
    except:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + 'An error occured. Sorry!\n')
        input(Fore.LIGHTWHITE_EX + Style.BRIGHT + '\nPress [ENTER] to return to main menu.')
        return None

#dbupdate - adds leaks from a combolist to the db:
def dbupdate():
    global newcount
    cleaner()
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\n### COMBOLIST-IMPORT TO YOUR LEAKCHECK DB ###\n\n')
    combofile = input(Fore.LIGHTWHITE_EX + Style.BRIGHT + 'Enter Name of your Combofile, e.g. combos.txt: ')
    if combofile == '':
        cleaner()
        print(Fore.LIGHTRED_EX + Style.BRIGHT + '\nNo filename entered.')
        input(Fore.LIGHTRED_EX + Style.BRIGHT + '\nPress [ENTER] to return to main menu.')
        return None
    else:
        try:
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\n\nStarting the Import of your Combofile ...\n\n')
            newleaks = open(combofile, 'r').read().splitlines()
        except:
            cleaner()
            print(Fore.LIGHTRED_EX + Style.BRIGHT + '\nCould not find or read combofile.')
            input(Fore.LIGHTRED_EX + Style.BRIGHT + '\nPress [ENTER] to return to main menu.')
            return None
    try:
        counter = len(newleaks)
    except:
        counter = 0
    if counter == 0:
        cleaner()
        print(Fore.LIGHTRED_EX + Style.BRIGHT + '\nNo Combos found for Import.')
        input(Fore.LIGHTRED_EX + Style.BRIGHT + '\nPress [ENTER] to return to main menu.')
        return None
    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + '\nFound ' + str(counter) + ' New Combos to import.\n')
    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + 'This will take a moment. Please wait ...!')
    newcount = 0
    while len(newleaks) > 0:
        try:
            addleak = newleaks.pop(0)
            with open('leak.db', 'a+') as receiver:
                receiver.seek(0)
                done = receiver.read(100)
                if len(done) > 0:
                    receiver.write('\n')
                receiver.write(addleak)
                receiver.close()
            newcount += 1
        except:
            continue
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\n\nA Total of ' + str(newcount) + 'Combos have been imported.')
    input(Fore.LIGHTWHITE_EX + Style.BRIGHT + '\nPress [ENTER] to return to main menu.')
    return None

#dbcleaner - deletes duplicates from the db:
#todo: write code of db cleaner.

#dbresult - writes results to the files and adds automatically private leaks to db:
#todo: write code of results handler.

#dbcheck - antipublic checker using a given combolist:
#todo: write code of the checker.

#dbcheckstart - startup routine for checker using threading:
#todo: write code of the startup for the checker.

#((<<-- *** M*A*I*N *** -->>))
cleaner()
print(logo1)
print(logo2)
print(mainmenu)
menu()
