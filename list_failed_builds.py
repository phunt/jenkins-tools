#!/usr/bin/env python

from jenkins import Jenkins

from optparse import OptionParser
import getpass

import pprint

def list_failed_builds(server, jobName):
    jobinfo = server.get_job_info(jobName)
    for b in jobinfo['builds']:
        buildnumber = b['number']
        buildinfo = server.get_build_info(jobName, buildnumber)
        if buildinfo['result'] == 'FAILURE':
            print(buildnumber)
            #pprint.pprint(buildinfo)
    

if __name__ == '__main__':
    usage = "usage: %prog [options] username jenkinsURL jobNamePattern"
    parser = OptionParser(usage=usage)

    (options, args) = parser.parse_args()

    if len(args) != 3:
        parser.error("need username, jenkins URL, and job name")
    username = args[0]
    jenkinsURL = args[1]
    jobName = args[2]
    
    password = getpass.getpass(prompt='password? ')

    server = Jenkins(jenkinsURL, username, password)
    
    list_failed_builds(server, jobName)
