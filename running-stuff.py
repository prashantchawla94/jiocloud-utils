#!/usr/bin/env python
import jenkins
import subprocess
import time
import sys


def p(s):
    print s
    sys.stdout.flush()

p('Getting list of running jobs')

proc = subprocess.Popen('nova list | grep puppet-rjil-gate | cut -f6-9 -d- '
                        '| cut -f1 -d" " | sort | uniq -c', shell=True,
                        stdout=subprocess.PIPE)
stdout, _stderr = proc.communicate()

jobs = {}

fp = open('running.html', 'w')

for l in stdout.split('\n'):
    l = l.strip()
    if not l:
        continue
    count, job = l.split(' ')
    job_number = int(job.split('-')[-1])
    jobs[job_number] = int(count)

jenkins = jenkins.Jenkins(url='http://jiocloud.rustedhalo.com:8080')

now = time.time()
fp.write('''
<table>
  <thead>
    <tr>
      <th>Build number</th>
      <th>Who triggered it?</th>
      <th>What's it for?</th>
      <th>How many minutes has it been running for?</th>
      <th>How much has it cost us so far?</th>
      <th>Terminate</th>
    </tr>
  </thead>
  <tbody>''')

for job in jobs:
    p('Getting info for job %s' % (job,))
    build = jenkins.get_build_info('puppet-rjil-gate', job)
    params = dict([(x['name'], x['value']) for x in build['actions'][0]['parameters']])
    running_for = (now-(build['timestamp']/1000))/60
    fp.write('''
    <tr>
      <td><a href="%s">%s</a></td>
      <td>%s</td>
      <td>%s</td>
      <td>%s</td>
      <td>$%.2f</td>
      <td><a href="http://jiocloud.rustedhalo.com:8080/job/puppet-rjil-gate-delete/buildWithParameters?jobid=%s">Terminate</a></td>
    </tr>
''' % (build['url'], job, params['ghprbTriggerAuthor'], build['description'], running_for, (running_for/60)*1.17, job))

fp.write('''
  </tbody>
</table>''')
fp.close()
