#!/usr/bin/env python

from jenkins import Jenkins

from optparse import OptionParser
import getpass

import re

def reconfig_assigned_node(server, jobNamePattern):
    for j in server.get_job_info_regex(jobNamePattern):
        jobname = j['name']

        config = server.get_job_config(jobname)

        m = re.search('<assignedNode>(.*)</assignedNode>', config)
        if m:
            print("Assigned node for job %s is %s" % (jobname, m.group(1)))
            config = re.sub('<assignedNode>.*</assignedNode>', '<assignedNode>ubuntu-ec2-beefy</assignedNode>', config)

            m = re.search('<assignedNode>(.*)</assignedNode>', config)
            print("Reassigned node for job %s is %s" % (jobname, m.group(1)))
            print("config " + config)

            prompt = raw_input('Reconfig? ')
            server.reconfig_job(jobname, config)
        else:
            print("Unable to identify assignedNode in " + jobname)
    

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
    
    reconfig_assigned_node(server, jobNamePattern)
