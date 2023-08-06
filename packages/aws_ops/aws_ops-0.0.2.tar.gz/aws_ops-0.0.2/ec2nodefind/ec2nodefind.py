#!/usr/bin/env python
#
# Copyright (c) 2013, Chris Maxwell <chris@wrathofchris.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
import argparse
import boto
import boto.ec2
import boto.ec2.autoscale
import boto.utils
import filecmp
import os
import sys
import tempfile

envtag = 'env'
svctag = 'service'
clutag = 'cluster'
autoscalegroup = None

aws_key = None
aws_secret = None
if 'AWS_ACCESS_KEY' in os.environ:
  aws_key = os.environ['AWS_ACCESS_KEY']
if 'AWS_SECRET_KEY' in os.environ:
  aws_secret = os.environ['AWS_SECRET_KEY']

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--auto", help="auto-detect (env,service,cluster)",
    action="store_true")
parser.add_argument("-A", "--autoscalegroup", help="use autoscaling host list",
    action="store_true")
parser.add_argument("-e", "--environ", help="environment tag")
parser.add_argument("-s", "--service", help="service tag")
parser.add_argument("-c", "--cluster", help="cluster tag")
parser.add_argument("-i", "--ipaddress", help="print IP address", action="store_true")
parser.add_argument("-F", "--fqdn", help="print FQDN", action="store_true")
parser.add_argument("-p", "--public", help="print public address/FQDN",
    action="store_true")
parser.add_argument("-v", "--verbose", help="be verbose", action="store_true")
parser.add_argument("-f", "--filename", help="file to write")
parser.add_argument("-r", "--region", help="ec2 region")
args = parser.parse_args()

if args.auto:
    identity = boto.utils.get_instance_identity()
    local_region = identity['document']['region']
    if not args.region:
        args.region = local_region
else:
    local_region = args.region
    if not args.region:
        args.region = 'us-east-1'

awsec2 = boto.ec2.connect_to_region(args.region, aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret)
tagfilter = { 'instance-state-name': 'running',
  'tag:%s' % svctag: args.service
}

# Auto-Discovery: read instance metadata
if args.auto == True:
  meta = boto.utils.get_instance_metadata()
  myinstfilter = { 'resource-id': meta['instance-id'] }
  if str(local_region) != str(args.region):
      localec2 = boto.ec2.connect_to_region(local_region,
              aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
      tags = localec2.get_all_tags(myinstfilter)
  else:
      tags = awsec2.get_all_tags(myinstfilter)
  for t in tags:
    if t.name == envtag:
      tagfilter['tag:%s' % envtag] = t.value
      if args.verbose:
        print "Autodiscovery: env %s" % t.value
    elif t.name == svctag:
      tagfilter['tag:%s' % svctag] = t.value
      if args.verbose:
        print "Autodiscovery: service %s" % t.value
    elif t.name == clutag:
      tagfilter['tag:%s' % clutag] = t.value
      if args.verbose:
        print "Autodiscovery: cluster %s" % t.value
    elif t.name == 'aws:autoscaling:groupName':
      autoscalegroup = t.value
      if args.verbose:
        print "Autodiscovery: autoscalegroup %s" % t.value

# Command-line args replace autodiscovery
if args.environ != None:
  tagfilter['tag:%s' % envtag] = args.environ
if args.service != None:
  tagfilter['tag:%s' % svctag] = args.service
if args.cluster != None:
  tagfilter['tag:%s' % clutag] = args.cluster

if args.autoscalegroup:
  # Use autoscalegroup name to get instances in stack order
  awsasg = boto.ec2.autoscale.connect_to_region(args.region,
          aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
  if not autoscalegroup:
    autoscalegroup = "%s-%s" % (tagfilter['tag:%s' % svctag],
        tagfilter['tag:%s' % envtag])
  asgs = awsasg.get_all_groups(names=[autoscalegroup])
  asg = None
  asginsts = []
  running = []
  if len(asgs) > 0:
    asg = asgs[0]
    for i in asg.instances:
      asginsts.append(i.instance_id)
    # Search for instances in autoscale order
    apiorder = awsec2.get_all_instances(instance_ids=asginsts)
    for a in asg.instances:
      for inst in apiorder:
        for i in inst.instances:
          if i.id == a.instance_id:
            running.append(inst)
else:
  # Search for tagged instances
  running = awsec2.get_all_instances(filters=tagfilter)

# Open temp file after all api work is done
if args.filename != None:
  outfile = tempfile.NamedTemporaryFile(dir=os.path.dirname(args.filename),
      delete=False)
else:
  outfile = sys.stdout

for inst in running:
  for i in inst.instances:
    if args.ipaddress == True:
      if args.public == True:
        outfile.write("%s\n" % i.ip_address)
      else:
        outfile.write("%s\n" % i.private_ip_address)
    elif args.fqdn == True:
      if args.public == True:
        outfile.write("%s\n" % i.public_dns_name)
      else:
        outfile.write("%s\n" % i.private_dns_name)
    else:
      outfile.write("%s\n" % i.private_dns_name.split('.')[0])

if args.filename != None:
  outfile.close()
  if os.path.exists(args.filename) == False or filecmp.cmp(outfile.name, args.filename) == False:
    os.rename(outfile.name, args.filename)
    os.chmod(args.filename, 0644)
  else:
    os.remove(outfile.name)


def main():
  pass
