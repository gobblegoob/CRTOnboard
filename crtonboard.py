###############################################################
#   Takes a source csv file of switches in an organization
#   Takes this information and creates sessions in secure crt.
#
#   -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-
#   
#   8/6/2018
###############################################################
from __future__ import print_function

import csv
import fileinput
import getopt
import os
import platform
import sys
from shutil import copy2

# win_root_path is the root directory of your crt sessions folder.  This
# is where the new files will be created.
root_path = ''
# EDIT win_root_path OR macos_root_path  VARIABLE WITH YOUR ROOT PATH
win_root_path = r'C:/Users/%USERPROFILE%/Documents/Sessions/'
macos_root_path = r'/Users/%USER%/Documents/Sessions/'

system_os = ''
src_ini_file = "crtblank.ini"
src_csv = 'crtsource.csv'
src_is_set = False
client = None
client_root_path = None
client_building_path = None
client_closet_path = None
prog_root_path = None
# This is the header structure of the source csv file.
file_vars = '[HOSTNAME]', '[HOST_IP]', '[USERNAME]', '[BUILDING]', '[IDF]', '[LOG_DIR]'


def initialize():
    global prog_root_path
    global src_is_set
    set_root_dir()
    prog_root_path = os.getcwd()
    # print(os.getcwd())
    get_client_name()

    # If you set the source file with an argument, don't call set_source_file function
    if src_is_set is False:
        set_source_file()

    get_source_file(src_csv)


def get_system_os():
    # Gets system OS
    os = platform.system()
    return os


def set_root_dir():
    # set the root path based on OS
    global win_root_path
    global macos_root_path
    global root_path
    system_os = get_system_os()
    if system_os == 'Darwin':
        root_path = macos_root_path
    else:
        root_path = win_root_path
    str1 = 'OS Detected:'
    str2 = 'Root Path:'
    print(f'{str1:<15} {system_os:>50}')
    print(f'{str2:<15} {root_path:>50}')
    return


def get_client_name():
    # Prompts for input to name client.  This will name the directory for the crt session files
    # as well as create the logs folder path.
    global client

    if client is None:
        while True:
            client_input = input("Enter client name: ")
            while True:
                print('-------------------------------')
                print(client_input)
                y = input('Is this correct? (y/n)')
                if y == 'y':
                    client = client_input
                    create_client_dir(client)
                    return client
                break
    else:
        return client


# Allows the user to set the source file. Simply updates the global variable src_csv and returns null
def set_source_file():
    global src_csv
    print("Current Source file: " + src_csv)
    if src_csv is not None:
        while True:
            print('-'*30)
            y = input('CHANGE SOURCE FILE? (y/n) ')
            y = y.upper()
            if y == 'Y':
                i = input('Enter File Name: ')
                if i.endswith('.csv'):
                    src_csv = i
                    print('SOURCE FILE IS NOW: ' + src_csv)
                    return
                else:
                    print('-'*30)
                    print('Source file must be .csv')
                    print('-'*30)
            else:
                return
    return


# Sends info to create_crt_file() in order to create the .ini files
def get_source_file(srcfile):
    try:
        with open(srcfile) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')

            # skip the header
            next(csvreader)

            for row in csvreader:
                create_crt_file(row)
                # print(row)
    except:
        print('\n\nThere was a problem importing the source CSV.  Check file formatting or illegal non UTF-8 characters')
        print('\nExiting ')
        quit()


# Takes each row from get_source_file() and creates hte new .ini file.  Passes output to edit_file()
# to modify the contents of the file.
def create_crt_file(row):
    filename = '_' + row[0]+'_'+row[1]+'.ini'
    print('Creating File: ' + filename)
    building = row[3]
    idf = row[4]
    global prog_root_path

    dest = client_root_path
    os.chdir(dest)

    if building != '':

        print('Buidling = '+building)
        dest = dest+'/'+building+'/'
        create_dir(building)
        os.chdir(dest)
        create_dir('logs')

    if idf != '':
        dest = dest+idf+'/'
        create_dir(idf)
        os.chdir(dest)
        create_dir('logs')

    print("Destination directory : "+dest)
    sf = prog_root_path + '/' + src_ini_file
    print('SOURCE FILE: '+sf)
    # print(sf + ' ' + dest)
    copy2(sf, dest)
    # Edit The File
    edit_file(row, dest, filename)


# Updates the new CSV file with the info from the source csv.
def edit_file(row, dest, fn):
    nfn = fn[1:]
    # Rename the file
    global src_ini_file
    print('Source File: ' + src_ini_file)
    print('Current Directory: ' + os.getcwd())
    os.rename(src_ini_file, nfn)
    global file_vars
    src_search_text = file_vars
    replacement_text = None
    log_dir = os.getcwd() + '/logs/'
    try:
        os.chdir(dest)
        for i in range(len(src_search_text)):
            text_to_search = src_search_text[i]
            if i < len(row):
                replacement_text = row[i]

            if i == len(row):
                replacement_text = log_dir

            with fileinput.FileInput(nfn, inplace=True) as file:
                for line in file:
                    print(line.replace(text_to_search, replacement_text), end='')

        print('--------------------------')
        print('Created File: %s' % nfn)
        print('--------------------------')
    except OSError:
        print('It broke: %s' % file_vars)


def create_client_dir(client):
    # Creates the client  directory in the crt sessions folder.
    # Also sets the client_root_path variable that cna be called as each directory is created.
    global client_root_path

    client_root_path = root_path+client
    if client is not None:
        if not os.path.exists(client_root_path):
            try:
                os.makedirs(client_root_path)
            except OSError:
                print('Failed to create directory %s' % client_root_path)
        else:
            print('Directory %s already exists.' % client_root_path)


def create_dir(dir):
    try:
        if not os.path.exists(dir):
            os.mkdir(dir)
            return
        else:
            return
    except OSError:
        print('Error creating directory %s' % dir)


def main():
    return


def main(argv):
    global src_csv
    global src_is_set
    helptext = ('\n\n--------------------------------------------------------------\n'
        'CRTOnboard takes a source csv file and creates a directory of \n'
        'of SecureCRT sessions.\n\n\n'
        'Arguments:\n\n'
        '\t-h\t\t\t This Help Dialog\n\n'
        '\t-f <sourcefile.csv>\t (Optional) Loads Source CSV as argument\n'
        '\t\t\t\t  The default source file is crtsource.csv'
        '\n'
        '-----------------------------------------------------------------\n'
        'To create a new source csv file, use the following format:\n'
        'HOSTNAME,HOST_IP,USERNAME,BUILDING,IDF\n\n')
    try:
        opts, args = getopt.getopt(argv, 'hi:o:',['ifile='])
    except getopt.GetoptError:
        print(helptext)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(helptext)
            sys.exit(2)
        elif opt in ('-i,','--ifile'):
            inputfile = arg
            if inputfile.endswith('.csv'):
                src_csv = inputfile
                src_is_set = True
                return
            else:
                print('crtonboard.py -i <sourcefile.csv>')
                sys.exit(2)
        else:
            return


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
        # srcfile = str(sys.argv[1])
        initialize()
    except KeyboardInterrupt:
        print('You have cancelled the operation')
