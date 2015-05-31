import os
import ftplib
import fnmatch
import ConfigParser
from contextlib import closing

Config = ConfigParser.ConfigParser()
Config.read("C:/Apps/LiClipse Workspace/samplePython/ftpsamples/filegenie.ini")

def ConfigSectionMap(section):
    attrib = {}
    options = Config.options(section)
    for option in options:
        try:
            attrib[option] = Config.get(section, option)
            if attrib[option] == -1:
                #DebugPrint("skip: %s" % option)
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            attrib[option] = None
    return attrib

ftp_account = 'hadjisg31'

with closing(ftplib.FTP()) as ftp:
    try:

        host = ConfigSectionMap(ftp_account)['host']
        port = ConfigSectionMap(ftp_account)['port']
        login = ConfigSectionMap(ftp_account)['login']
        passwd = ConfigSectionMap(ftp_account)['passwd']
        orig_filename = ConfigSectionMap(ftp_account)['src_fname']
        #local_filename = ConfigSectionMap(ftp_account)['tgt_fname']
        
        print ( 'Accessing ' + login + '@'+ host + ' at port ' + port )
        ftp.connect(host, port, 30*5) #5 mins timeout
        ftp.login(login, passwd)
        ftp.set_pasv(True)
        
        ftp_list = []
        ftp.retrlines("LIST", ftp_list.append)    
        
        print "Looking up pattern: ", orig_filename

        for line in ftp_list:
            words = line.split(None, 8)
            ftp_file = words[-1].lstrip()

            if fnmatch.fnmatch(ftp_file, orig_filename):

                local_filename = ftp_file            
                print( 'Downloading remote file ' + ftp_file + ' to local ' + local_filename)

                with open(local_filename, 'w+b') as f:
                    res = ftp.retrbinary('RETR %s' % ftp_file, f.write)
                    #print str(res) 
        
                    if not res.startswith('226'):
                        print('Download of file {0} is not complete.'.format(orig_filename))
                        os.remove(local_filename)
                        exit(1)
                    
        ftp.close()
        
    except:
            print('Error during download from FTP ' + host + ' with file: ' + orig_filename)
            exit(1) 
            

print('Successful download from FTP ' + host)

exit(0)

