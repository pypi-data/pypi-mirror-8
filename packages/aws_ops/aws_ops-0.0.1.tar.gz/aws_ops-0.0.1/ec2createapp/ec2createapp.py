#!/usr/bin/env python
#
# Copyright (c) 2013 Chris Maxwell <chris@wrathofchris.com>
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
# Thanks to Mahesh Paolini-Subramanya (@dieswaytoofast) for his help
#
import argparse
import boto
import boto.ec2
import boto.ec2.autoscale
import boto.vpc
import datetime
import json
import yaml
import os
import re
import sys
import time
from pprint import pprint

if 'AWS_ACCESS_KEY' in os.environ:
  aws_key = os.environ['AWS_ACCESS_KEY']
else:
  aws_key = None
if 'AWS_SECRET_KEY' in os.environ:
  aws_secret = os.environ['AWS_SECRET_KEY']
else:
  aws_secret = None

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="verbosity", action="store_true")
parser.add_argument("-r", "--region", help="ec2 region")
parser.add_argument("-f", "--file", help="cloudcaster spec file")
parser.add_argument("name", help="app name to implement")
args = parser.parse_args()
if args.name == None or args.file == None:
  parser.print_help()
  sys.exit(1)

conffile = open(args.file).read()

# If the file ends with .yaml, we're going to enforce
# a standard from here that you need to use filenames.
#
# Otherwise, we're going to assume you're just using json
# without extensions?
#
# - vjanelle
if args.file.lower().endswith(".yaml"):
    conf = yaml.load(conffile)
else:
    conf = json.loads(conffile)

if args.region == None:
  args.region = 'us-east-1'

verbose = args.verbose
awsec2 = boto.ec2.connect_to_region(args.region, aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
awselb = boto.ec2.elb.connect_to_region(args.region, aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
awsasg = boto.ec2.autoscale.connect_to_region(args.region, aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
awsvpc = boto.vpc.connect_to_region(args.region, aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)

#
# BLOCK DEVICE MAPPINGS - http://aws.amazon.com/ec2/instance-types/
#
bdmapping={}
bdmapping['c1.medium'] = 1
bdmapping['c1.xlarge'] = 1
bdmapping['c3.2xlarge'] = 2
bdmapping['c3.4xlarge'] = 2
bdmapping['c3.8xlarge'] = 2
bdmapping['c3.large'] = 2
bdmapping['c3.xlarge'] = 2
bdmapping['cc2.8xlarge'] = 4
bdmapping['cg1.4xlarge'] = 2
bdmapping['cr1.8xlarge'] = 2
bdmapping['g2.2xlarge'] = 1
bdmapping['hi1.4xlarge'] = 2
bdmapping['hs1.8xlarge'] = 24
bdmapping['i2.2xlarge'] = 2
bdmapping['i2.4xlarge'] = 4
bdmapping['i2.8xlarge'] = 8
bdmapping['i2.xlarge'] = 1
bdmapping['m1.large'] = 2
bdmapping['m1.medium'] = 1
bdmapping['m1.small'] = 1
bdmapping['m1.xlarge'] = 4
bdmapping['m2.2xlarge'] = 1
bdmapping['m2.4xlarge'] = 2
bdmapping['m2.xlarge'] = 1
bdmapping['m3.2xlarge'] = 2
bdmapping['m3.large'] = 1
bdmapping['m3.medium'] = 1
bdmapping['m3.xlarge'] = 2
bdmapping['t2.micro'] = 0
bdmapping['t2.small'] = 0
bdmapping['t2.medium'] = 0

def find_vpc(cidr, vpcs):
  for v in vpcs:
    if v.cidr_block == cidr:
      return v
  return None

def find_sg(sg, sgs):
  for s in sgs:
    if s.name == sg:
      return s
  return None

def find_amibyname(name, amis):
  for a in amis:
    if str(a.name) == name:
      return a
    if re.match("%s-\d{14}" % name, str(a.name)):
      return a
  return None

def find_autoscale(name, asgs):
  for g in asgs:
    if str(g.name) == name:
      return g
  return None

def find_elb_conf(elb, elbs):
  for e in elbs:
    if e['name'] == elb:
      return e
  return None

def find_subnet(cidr, nets):
  for n in nets:
    if n.cidr_block == cidr:
      return n
  return None

for app in conf['apps']:
  if app['name'] != args.name:
    continue
  if 'autoscale' not in app:
    print "no autoscale block, I shouldn't be doing this!"
    sys.exit(1)
    
  # load vpcs, security groups
  vpcs = awsvpc.get_all_vpcs()
  vpc = find_vpc(conf['vpc']['cidr'], vpcs)
  vpcfilter = { 'vpc_id': vpc.id }
  vpc_subnetids = []
  vpc_pubsubnetids = []
  sgs = awsec2.get_all_security_groups(filters=vpcfilter)
  sglist = list()
  if 'group' in app:
      sg = find_sg(app['group'], sgs)
      if not sg:
          print "SGLIST failed to find SG %s" % app['group']
          sys.exit(1)
      sglist.append(str(sg.id))
  if 'groups' in app:
      for gname in app['groups']:
          sg = find_sg(gname, sgs)
          if not sg:
              print "SGLIST failed to find SG %s" % gname
              sys.exit(1)
          if sg.id not in sglist:
              sglist.append(str(sg.id))

  # public ip requested
  publicip = False
  if 'public' in app:
    publicip = True

  # block device mapping
  mapping = None
  if app['type'] in bdmapping:
    mapping = boto.ec2.blockdevicemapping.BlockDeviceMapping()
    for b in range(0, bdmapping[app['type']]):
      # punt on dealing with complex case
      if b > 24:
        print "Seriously?  You want more than 24 devices?  Figure this out yourself."
        break
      # sdc..z
      devname= '/dev/sd%s' % chr(ord('b') + b)
      mapping[devname] = boto.ec2.blockdevicemapping.BlockDeviceType(ephemeral_name="ephemeral%d" % b)
      if verbose:
        print "block device mapping %s to %s" % (mapping[devname].ephemeral_name, devname)

  if 'aminame' in app and not 'ami' in app:
    # Search ami list, find best match
    # 1. {{env}}-{{ami}}-{{date}}
    # 2. all-{{ami}}-{{date}}
    # 3. {{ami}}-{{date}}
    ami = None
    amifilter = { 'name': "%s-%s-*" % (conf['aws']['env'], app['aminame']) }
    amis = awsec2.get_all_images(filters=amifilter)
    if len(amis) > 0:
      ami = find_amibyname("%s-%s" % (conf['aws']['env'], app['aminame']),
          sorted(amis, key=lambda a: a.name, reverse=True))
    if ami == None:
      amifilter = { 'name': "all-%s-*" % app['aminame'] }
      amis = awsec2.get_all_images(filters=amifilter)
      if len(amis) > 0:
        ami = find_amibyname("all-%s" % app['aminame'],
            sorted(amis, key=lambda a: a.name, reverse=True))
    if ami == None:
      amifilter = { 'name': "%s-*" % app['aminame'] }
      amis = awsec2.get_all_images(filters=amifilter)
      if len(amis) > 0:
        ami = find_amibyname("%s" % app['aminame'],
            sorted(amis, key=lambda a: a.name, reverse=True))
    if ami == None:
      amifilter = { 'name': app['aminame'] }
      amis = awsec2.get_all_images(filters=amifilter)
      if len(amis) > 0:
        ami = find_amibyname("%s" % app['aminame'],
            sorted(amis, key=lambda a: a.name, reverse=True))
    if ami != None:
      app['ami'] = ami.id
      print "AMI mapping %s to %s %s (%s)" % (app['aminame'], ami.id, ami.name, ami.description)
    else:
      print "AMI mapping failed for \"%s\" as %s-%s-*, all-%s-*, %s" % (app['aminame'], conf['aws']['env'], app['aminame'], app['aminame'], app['aminame'])
      sys.exit(1)

  now = datetime.datetime.utcnow()
  nowstr = now.strftime("%Y%m%d%H%M%S")
  asgname = "%s-%s" % (app['name'], conf['aws']['env'])
  asgnamefull = "%s-%s" % (asgname, nowstr)
  role = None
  if 'role' in app:
    role = app['role']

  print "Creating Launch Config %s" % asgnamefull
  lc = boto.ec2.autoscale.LaunchConfiguration(
      name = asgnamefull,
      security_groups = sglist,
      image_id = app['ami'],
      key_name = app['keypair'],
      instance_type = app['type'],
      instance_profile_name = role,
      block_device_mappings = [mapping],
      associate_public_ip_address = publicip
  )

  req = awsasg.create_launch_configuration(lc)
  if req == None:
    print "Failed creating launch configuration"
    sys.exit(1)
  if verbose:
    print "%s ami %s type %s key %s role %s" % (lc.name, lc.image_id, lc.instance_type, lc.key_name, lc.instance_profile_name)

  #
  # AutoScale
  #

  astags = []
  astags.append(boto.ec2.autoscale.tag.Tag(
    key='Name', value=asgname,
    propagate_at_launch=True, resource_id=asgname))
  astags.append(boto.ec2.autoscale.tag.Tag(
    key=conf['aws']['envtag'], value=conf['aws']['env'],
    propagate_at_launch=True, resource_id=asgname))
  astags.append(boto.ec2.autoscale.tag.Tag(
    key=conf['aws']['svctag'], value=app['svctag'],
    propagate_at_launch=True, resource_id=asgname))
  astags.append(boto.ec2.autoscale.tag.Tag(
    key='cluster', value=app['cluster'],
    propagate_at_launch=True, resource_id=asgname))

  # Refresh and load subnet IDs
  vpcsubnetfilter = { 'vpcId': [ vpc.id ] }
  nets = awsvpc.get_all_subnets(filters=vpcsubnetfilter)
  if 'subnets' in conf['vpc']:
    for n in conf['vpc']['subnets']:
      net = find_subnet(n, nets)
      vpc_subnetids.append(net.id)
  if 'pubsubnets' in conf['vpc']:
    for n in conf['vpc']['pubsubnets']:
      net = find_subnet(n, nets)
      vpc_pubsubnetids.append(net.id)

  # Find ELB if requested
  elb = None
  app_lbname = None
  if 'elb' in app:
    elbconf = find_elb_conf(app['elb'], conf['elbs'])
    if elbconf != None:
      elbs = awselb.get_all_load_balancers("%s-%s" % (app['elb'], conf['aws']['env']))
    else:
      elbs = awselb.get_all_load_balancers(app['elb'])
    elb = elbs[0]
    app_lbname = [ elb.name ]
  if 'elbs' in app:
      for elbname in app['elbs']:
          # skip if previously created/registered
          if 'elb' in app and elbname == app['elb']:
              continue
      elbconf = find_elb_conf(elbname, conf['elbs'])
      if elbconf != None:
          elbs = awselb.get_all_load_balancers("%s-%s" % (elbname,
              conf['aws']['env']))
      else:
          elbs = awselb.get_all_load_balancers(elbname)
      elb = elbs[0]
      if app_lbname == None:
          app_lbname = []
      app_lbname.append("%s-%s" % (elb.name, conf['aws']['env']))

  asgroups = awsasg.get_all_groups(names=[asgname])
  if 'public' in app:
    subnetlist = ",".join(vpc_pubsubnetids)
  else:
    subnetlist = ",".join(vpc_subnetids)
  ag = find_autoscale(asgname, asgroups)
  if ag == None:
    print "Creating Autoscaling Group %s" % asgname
    ag = boto.ec2.autoscale.AutoScalingGroup(
        group_name = asgname,
        availability_zones = conf['vpc']['azs'],
        launch_config = lc,
        load_balancers = app_lbname,
        min_size = app['autoscale']['min'],
        max_size = app['autoscale']['max'],
        tags = astags,
        vpc_zone_identifier = subnetlist,
        connection = awsasg)
    req = awsasg.create_auto_scaling_group(ag)
    if req == None:
      print "Failed creating launch configuration"
      sys.exit(1)
  if verbose:
    print "autoscale %s size %d-%d elb %s launch %s" % (ag.name, ag.min_size, ag.max_size, ag.load_balancers, ag.launch_config_name)
    if ag.instances != None:
      for i in ag.instances:
        print "autoscale instance %s %s" % (ag.name, i.instance_id)
  print "Updating Autoscaling Group Launch Config %s -> %s" % (ag.launch_config_name, lc.name)
  ag.launch_config_name = lc.name
  req = ag.update()


def main():
  pass
