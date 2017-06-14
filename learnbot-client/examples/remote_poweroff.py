#!/usr/bin/env python

# sudo pip install paramiko
from __future__ import print_function
import sys
import socket
import paramiko
#=================================
# Class: PySSH
#=================================
class PySSH(object):
   
   
    def __init__ (self):
        self.ssh = None
        self.transport = None 
 
    def disconnect (self):
        if self.transport is not None:
           self.transport.close()
        if self.ssh is not None:
           self.ssh.close()
 
    def connect(self,hostname,username,password,port=12312):
        self.hostname = hostname
        self.username = username
        self.password = password
 
        self.ssh = paramiko.SSHClient()
        #Don't use host key auto add policy for production servers
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.load_system_host_keys()
        try:
            self.ssh.connect(hostname,port,username,password)
            self.transport=self.ssh.get_transport()
        except (socket.error,paramiko.AuthenticationException) as message:
            print ("ERROR: SSH connection to "+self.hostname+" failed: " +str(message))
            sys.exit(1)
        return  self.transport is not None
 
    def runcmd(self,cmd,sudoenabled=True):
        if sudoenabled:
            fullcmd="echo " + self.password + " |   sudo -S -p '' " + cmd
        else:
            fullcmd=cmd
        if self.transport is None:
            return "ERROR: connection was not established"
        session=self.transport.open_session()
        session.set_combine_stderr(True)
        #print "fullcmd ==== "+fullcmd
        if sudoenabled:
            session.get_pty()
        session.exec_command(fullcmd)
        stdout = session.makefile('rb', -1)
        #print stdout.read()
        output=stdout.read()
        session.close()
        return output
 
#===========================================
# MAIN
#===========================================        
if __name__ == '__main__':
    hostname = 'odroid.local'
    username = 'odroid'
    password = 'yourkey'
    ssh = PySSH()
    ssh.connect(hostname,username,password)
    output=ssh.runcmd('sudo poweroff')
    print (output)
    ssh.disconnect()
