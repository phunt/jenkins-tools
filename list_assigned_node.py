#!/usr/bin/env python

from jenkins import Jenkins

from optparse import OptionParser
import getpass

import re

def list_assigned_node(server, jobNamePattern):
    for j in server.get_job_info_regex(jobNamePattern):
        jobname = j['name']
        print("jobname " + jobname)

        config = server.get_job_config(jobname)

        m = re.search('<assignedNode>(.*)</assignedNode>', config)
        if m:
            print("Assigned node for job %s is %s" % (jobname, m.group(1)))
    

if __name__ == '__main__':
    usage = "usage: %prog [options] username jenkinsURL jobNamePattern"
    parser = OptionParser(usage=usage)

    (options, args) = parser.parse_args()

    if len(args) != 3:
        parser.error("need username, jenkins URL, and naming pattern for the job")
    username = args[0]
    jenkinsURL = args[1]
    jobNamePattern = args[2]
    
    password = getpass.getpass(prompt='password? ')

    server = Jenkins(jenkinsURL, username, password)
    
    list_assigned_node(server, jobNamePattern)
