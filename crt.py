###############################################################
#   CRTOnboard v2.0
#   Now with Arguments!
#   
#   And OOP approach for easy use with other programs. 
#
#   Takes a source csv file of switches in an organization
#   Takes this information and creates sessions in secure crt.
#
#   
#   -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-
#   
#   12/17/2021
###############################################################
import csv
import fileinput 
import os
import platform
from shutil import copy2
import argparse


class CRT():
    def __init__(self):
        self.root_path = r'C:\\%USERPROFILE%\\Documents\\Sessions\\' # UPDATE THIS TO REFLECT YOUR SESSIONS FOLDER PATH
        self.system_os = platform.system()
        self.src_csv = 'crtsource.csv'
        self.src_ini_file = 'crtblank.ini'
        self.client_name = None
        self.prog_root_path = os.getcwd() + '\CRTOnboard'
        # This is the header structure of the source csv file.
        self.file_vars = '[HOSTNAME]', '[HOST_IP]', '[USERNAME]', '[BUILDING]', '[IDF]', '[LOG_DIR]'
        

    def set_src_csv(self, src):
        self.src_csv = src
        return
    
    def print_src_csv(self):
        print(self.src_csv)
    
    def set_root_dir(self, rp):
        self.root_path = rp
        return

    def set_client_name(self, client):
        self.client_name = client
        return
    
    def read_client_name(self):
        # Prompt user for client name
        if self.client_name is None:
            while True:
                client_input = input('Enter client name: ')
                print('-' * 80)
                y = input(f'Client: {client_input}\n Is this correct? (y/n): ')
                if y == 'y':
                    self.set_client_name(client_input)
                    print(f'Client name is set to {self.client_name}')
                    return
                else: 
                    continue

# Create your CRT instance
crt = CRT()

def create_sessions(srcfile):
    # Gets source file and initiates program
    print(f'Source File as defined: {srcfile}')
    os.chdir(crt.prog_root_path)
    print(f'current working directory: {os.getcwd()}\\')

    # Ensure client directory is created
    create_client_dir(crt.client_name)

    try:
        with open(srcfile) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')

            # skip the header
            next(csvreader)

            for row in csvreader:
                create_crt_file(row)
                # print(row)
    except Exception as e:
        print('\n\nThere was a problem importing the source CSV.  \nCheck file formatting or illegal non UTF-8 characters')
        print('\nExiting ')
        print(e)
        quit()

def read_source_file(srcfile):
    # Sends info to create_crt_file() in order to create the ini files.
    # was create_sessions()
    try:
        with open(crt.src_csv) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')

            #skip the header
            next(csvreader)

            for row in csvreader:
                create_crt_file(row)
    except:
        print('\n\nThere was a problem importing the source CSV.  \nCheck file formatting or illegal non UTF-8 characters')
        print('\nExiting ')
        quit()


def create_crt_file(row):
    # Takes each row from create_sessions(0 and creates the new .ini file.
    # Passes output to edit_file() to modify the contents of the file
    filename = '_' + row[0]+'_'+row[1]+'.ini'
    print('Creating File: ' + filename)
    building = row[3]
    idf = row[4]

    dest = crt.root_path + '/' + crt.client_name
    print(f'Destination Folder: {dest}')
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
    sf = crt.prog_root_path + '/' + crt.src_ini_file
    print('SOURCE FILE: '+sf)
    # print(sf + ' ' + dest)
    copy2(sf, dest)
    # Edit The File
    edit_file(row, dest, filename)


def edit_file(row, dest, fn):
    # Updates the new CSV file with the info  from the source csv
    nfn = fn[1:]
    # Rename the file
 
    print('Source File: ' + crt.src_ini_file)
    print('Current Directory: ' + os.getcwd())
    os.rename(crt.src_ini_file, nfn)

    src_search_text = crt.file_vars
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
        print('It broke: %s' % crt.file_vars)



def create_client_dir(client):
    # Creates the client directory in the crt sessions folder
    client_root_path = crt.root_path + '\\' + client

    if client is not None:
        if not os.path.exists(client_root_path):
            try:
                os.makedirs(client_root_path)
            except OSError as e:
                print(f'Failed to create dir {client_root_path}')
                print(e)
        else:
            print(f'Directory {client_root_path} already exists.  Continuing...')


def create_dir(dir):
    try:
        if not os.path.exists(dir):
            os.mkdir(dir)
            return
        else:
            return
    except OSError as e:
        print(f'Error creating directory {dir}')
        print(e)


if __name__ == "__main__":
    helptext = (
    'CRTOnboard takes a source csv file and creates a directory of \n'
    'of SecureCRT sessions.'
    'To create a new source csv file, use the following format:\n'
    'HOSTNAME,HOST_IP,USERNAME,BUILDING,IDF\n\n')

    print(f'Source CSV File: {crt.src_csv}')

    parser = argparse.ArgumentParser(description=helptext)

    parser.add_argument('-c', '--client', type=str, help='Name of the client')
    parser.add_argument('-f', '--file', type=str, help='Enter file name for source CSV')
    parser.add_argument('-p', '--path', type=str, help='Optional enter destination path for session folder')

    args = parser.parse_args()
    if args.client is not None:
        crt.set_client_name(args.client)
    
    if args.file is not None:
        crt.set_src_csv(args.file)

    if args.path is not None:
        crt.set_root_dir(args.path)
    
    # Make sure we get a client name
    if crt.client_name is None:
        crt.read_client_name()

    # Execute the task
    create_sessions(crt.src_csv)
  
