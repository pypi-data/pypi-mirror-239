# Ansible Automation Platform Python Module

This is unofficial wrapper for Ansible Automation Platform (AAP) API.

To see an example how this module can be used please view [\_\_main\_\_.py](https://gitlab.corp.redhat.com/network/python-aap/-/blob/main/src/aap/__main__.py)

## Executing jobs from CLI

Python module can be invoked directly to execute job in aap and report status to terminal. AAP Credentials need to be specified either via CLI arguments or env variables



Usage:
```
usage: python3 -m aap [-h] -i ID [-f] [-p PASSWORD] [-u USERNAME] [-s URL]
                      [--insecure] [-l LIMIT] [-e EXTRA] [-r RETRIES]
                      [-t TIMEOUT] [--ignore-fail]
                      {run-job}

Trigger jobs and workflows from terminal

positional arguments:
  {run-job}

optional arguments:
  -h, --help            show this help message and exit
  -i ID, --id ID        ID of job to run
  -f, --follow          Wait for job to finish execution and report its status
  -p PASSWORD, --password PASSWORD
                        Password used for authentication to AAP API (env:
                        AAP_PASSWORD)
  -u USERNAME, --username USERNAME
                        Username used for authentication to AAP API (env:
                        AAP_USERNAME)
  -s URL, --url URL     URL of AAP instance (env: AAP_URL)
  --insecure            Dont verify ssl certificate
  -l LIMIT, --limit LIMIT
                        Limit as comma separated list
  -e EXTRA, --extra-vars EXTRA
                        json formatted extra variables
  -r RETRIES, --retries RETRIES
                        Number of retries on API error
  -t TIMEOUT, --poll-timeout TIMEOUT
                        Number of seconds between 2 polling requests to aap
  --ignore-fail         Program will return successfull even if job fails
```


Example run
```
$ python3 -m aap --id 7848 -l sw01-dist.itdev --insecure run-job -f
Searching job 7848
Job: Juniper - gather facts
        limit: ['sw01-dist.itdev']
        extra variables: {}
        job id: 2161058
----------------------------------------
Job is running
[DEPRECATION WARNING]: COMMAND_WARNINGS option, the command warnings feature is
 being removed. This feature will be removed from ansible-core in version 2.14.
 Deprecation warnings can be disabled by setting deprecation_warnings=False in 
ansible.cfg.
[DEPRECATION WARNING]: [defaults]callback_whitelist option, normalizing names 
to new standard, use callbacks_enabled instead. This feature will be removed 
from ansible-core in version 2.15. Deprecation warnings can be disabled by 
setting deprecation_warnings=False in ansible.cfg.

PLAY [all] *********************************************************************

TASK [Set tower run variable] **************************************************
ok: [sw01-dist.itdev]

TASK [Set manip if oob] ********************************************************
skipping: [sw01-dist.itdev]

TASK [Check inbound management IP] *********************************************
skipping: [sw01-dist.itdev]

TASK [Check inbound management IP] *********************************************
ok: [sw01-dist.itdev]

TASK [Set username] ************************************************************
skipping: [sw01-dist.itdev]

TASK [set_fact] ****************************************************************
skipping: [sw01-dist.itdev]

TASK [set_fact] ****************************************************************
skipping: [sw01-dist.itdev]

TASK [set_fact] ****************************************************************
ok: [sw01-dist.itdev]

TASK [Check management IP] *****************************************************
skipping: [sw01-dist.itdev]

TASK [Check management IP] *****************************************************
skipping: [sw01-dist.itdev]

TASK [set_fact] ****************************************************************
skipping: [sw01-dist.itdev]

TASK [set_fact] ****************************************************************
skipping: [sw01-dist.itdev]

TASK [set_fact] ****************************************************************
skipping: [sw01-dist.itdev]

TASK [set_fact] ****************************************************************
skipping: [sw01-dist.itdev]

TASK [Set connection variables] ************************************************
ok: [sw01-dist.itdev]

TASK [Get Facts] ***************************************************************
ok: [sw01-dist.itdev]
Playbook run took 0 days, 0 hours, 0 minutes, 12 seconds
PLAY RECAP *********************************************************************
sw01-dist.itdev            : ok=5    changed=0    unreachable=0    failed=0    skipped=11   rescued=0    ignored=0   
Playbook run took 0 days, 0 hours, 0 minutes, 12 seconds
```
