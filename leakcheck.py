#!/usr/local/bin/python3
#encoding: utf-8
#name: leakcheck
#description: checks given combolists against a private lib of leaks
#version: 0.11, 2020-11-15
#author: DrPython3
#TODO: start writing the code, more information below ...

#((<-- *** NEEDED PACKAGES *** -->))

#TODO: Add packages needed ...
import ctypes, os, sys, threading
import colorama
from colorama import *
init()
print(Fore.LIGHTWHITE_EX + '')

#((<-- *** Variables, Functions, etc. *** -->))

runcounter = int(0) #just a counter for handling menu optically.
public = int(0) #for stats in title bar
private = int(0) #for stats in title bar
leakcount = int(0) #for counting leaks in db
leakdic = [] #for counting leaks in db
combofile = '' #file with combos for checker, updater etc.
newcount = int(0) #new combos processed by checker, updater etc.
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

   support this tool with donations (BTC): 1MiKuJrTCNST3haCX6sCnmMWTxJ4ZXtYgw
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

#clean - clear screen on purpose:
def clean():
    try:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    except: pass

#menu - screen with main menu for user:
def menu():
    global runcounter
    clean()
    print(Fore.LIGHTRED_EX + Style.BRIGHT + str(logo1))
    if runcounter < 1:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + str(logo2))
    else: pass
    print(Fore.LIGHTWHITE_EX + str(mainmenu))
    runcounter += 1
    what = int(input(Fore.LIGHTYELLOW_EX + Style.BRIGHT + '\nYOUR CHOICE: '))
    if what == 1:
        # TODO: write function dbcheck() ...
        dbcheck()
    elif what == 2:
        dbupdate()
    elif what == 3:
        dbcount()
    elif what == 4:
        #TODO: write function dbmaintain() ...
        clean()
        print(Fore.LIGHTRED_EX + Style.BRIGHT + 'Sorry, option not included yet ...\n')
        input(Fore.LIGHTWHITE_EX + Style.BRIGHT + '\nPress [ENTER] to return to main menu.')
        return None
    else:
        clean()
        sys.exit(Fore.LIGHTRED_EX + Style.BRIGHT + exitmsg)

#dbcount - delivers amount of leaks currently saved in db, actually not in use:
def dbcount():
    global leakcount
    clean()
    print(Fore.LIGHTWHITE_EX + Style.BRIGHT + '\nWait a moment, please (...)\n')
    try:
        leakdic = open('leak.db', 'r').read().splitlines()
        leakcount = int(len(leakdic))
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
    clean()
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\n### COMBOLIST-IMPORT TO YOUR LEAKCHECK DB ###\n\n')
    combofile = input(Fore.LIGHTWHITE_EX + Style.BRIGHT + 'Enter Name of your Combofile, e.g. combos.txt: ')
    if combofile == '':
        clean()
        print(Fore.LIGHTRED_EX + Style.BRIGHT + '\nNo filename entered.')
        input(Fore.LIGHTRED_EX + Style.BRIGHT + '\nPress [ENTER] to return to main menu.')
        return None
    else:
        try:
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\n\nStarting the Import of your Combofile ...\n\n')
            newleaks = open(combofile, 'r').read().splitlines()
        except:
            clean()
            print(Fore.LIGHTRED_EX + Style.BRIGHT + '\nCould not find or read combofile.')
            input(Fore.LIGHTRED_EX + Style.BRIGHT + '\nPress [ENTER] to return to main menu.')
            return None
    try:
        counter = len(newleaks)
    except:
        counter = 0
    if counter == 0:
        clean()
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

#dbmaintain - deletes duplicates from the db:
#todo: write code of db cleaner.

#dbresult - writes results to the files and adds automatically private leaks to db:
#todo: write code of results handler.

#dbcheck - antipublic checker using a given combolist:
#todo: write code of the checker.

#dbcheckstart - startup routine for checker using threading:
#todo: write code of the startup for the checker.

#((<<-- *** M*A*I*N *** -->>))
while True:
    menu()
