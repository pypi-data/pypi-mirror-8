#!/usr/bin/env python
#
# Copyright (c) 2014 Chris Maxwell <chris@wrathofchris.com>
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
import boto.ec2.elb
import datetime
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
parser.add_argument("-a", "--ami", help="ami ID")
parser.add_argument("-e", "--environ", help="environment tag")
parser.add_argument("-s", "--service", help="service tag")
parser.add_argument("-n", "--name", help="ami name")
parser.add_argument("group", help="autoscale group to update")
args = parser.parse_args()
if args.group == None:
  parser.print_help()
  sys.exit(1)

if args.region == None:
  args.region = 'us-east-1'

if args.service == None and args.name == None and args.ami == None:
  print "require [-n name] or [-s service] or [-a ami]"
  sys.exit(1)

verbose = args.verbose
awsec2 = boto.ec2.connect_to_region(args.region, aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
awselb = boto.ec2.elb.connect_to_region(args.region, aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
awsasg = boto.ec2.autoscale.connect_to_region(args.region, aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)

def find_amibyname(name, amis):
  for a in amis:
    if str(a.name) == name:
      return a
    if re.match("%s-\d{14}" % name, str(a.name)):
      return a
  return None

ami = None
aminame = None
aminameenv = None

# Search exact ID match
if args.ami:
  amis = awsec2.get_all_images(image_ids=[args.ami])
  if len(amis) > 0:
    ami = amis[0]

# AMI name set by user
if aminame == None and args.name:
  aminame = args.name

# AMI name from service
if aminame == None and args.service:
  if args.service:
    aminame = args.service

# Environ
if aminame and args.environ:
  aminameenv = "%s-%s" % (args.environ, aminame)

if ami == None and aminame == None:
  print "no name or service provided"
  sys.exit(1)

# Search ami list, find best match
# 1. {{env}}-{{aminame}}-{{date}}
# 2. all-{{aminame}}-{{date}}
# 3. {{aminame}}-{{date}}
# 4. {{aminame}}
if ami == None:

  # 1. {{env}}-{{aminame}}-{{date}}
  if aminameenv:
    amifilter = { 'name': "%s-*" % aminameenv }
    amis = awsec2.get_all_images(filters=amifilter)
    if len(amis) > 0:
      ami = find_amibyname(aminameenv, sorted(amis, key=lambda a: a.name, reverse=True))

  # 2. all-{{aminame}}-{{date}}
  if ami == None:
    amifilter = { 'name': "all-%s-*" % aminame }
    amis = awsec2.get_all_images(filters=amifilter)
    if len(amis) > 0:
      ami = find_amibyname("all-%s" % aminame, sorted(amis, key=lambda a: a.name, reverse=True))

  # 3. {{aminame}}-{{date}}
  if ami == None:
    amifilter = { 'name': "%s-*" % aminame }
    amis = awsec2.get_all_images(filters=amifilter)
    if len(amis) > 0:
      ami = find_amibyname("%s" % aminame, sorted(amis, key=lambda a: a.name, reverse=True))

  # 4. {{aminame}}
  if ami == None:
    amifilter = { 'name': aminame }
    amis = awsec2.get_all_images(filters=amifilter)
    if len(amis) > 0:
      ami = amis[0]

if ami == None:
  print "AMI mapping failed for \"%s\" as" % aminame,
  if aminameenv:
    print "%s-*," % aminameenv,
  print "all-%s-*, %s-*, %s" % (aminame, aminame, aminame)
  sys.exit(1)

if verbose:
  print "AMI mapping %s to %s %s (%s)" % (aminame, ami.id, ami.name, ami.description)
  sys.stdout.flush()

#
# Autoscale Group
#

asgupdate = False

asgroups = awsasg.get_all_groups(names=[args.group])
if len(asgroups) < 1:
  print "no autoscale group %s found" % args.group
  sys.exit(1)

asg = asgroups[0]

#
# Launch Configs
#

def find_launch(name, ascs):
  for c in ascs:
    # Exact match
    if str(c.name) == name:
      return c
    # Regex match env-name-YYYYMMDDHHMMSS
    if re.match("%s-\d{14}" % name, str(c.name)):
      return c
  return None

# paged responses are really annoying
def really_get_all_launch_configurations():
  res = []
  lcs = awsasg.get_all_launch_configurations()
  for l in lcs:
    res.append(l)

  while lcs.next_token != None:
    lcs = awsasg.get_all_launch_configurations(next_token=lcs.next_token)
    for l in lcs:
      res.append(l)

  return res

lc = None

# Check active LC
lcconfigs = awsasg.get_all_launch_configurations(names=[asg.launch_config_name])
if len(lcconfigs) > 0:
  lc = lcconfigs[0]

if lc == None or lc.image_id != ami.id:
  asgupdate = True
  if verbose:
    print "active launch config %s ami != %s" % (asg.launch_config_name, ami.id)
    sys.stdout.flush()
  lcconfigs = sorted(really_get_all_launch_configurations(), key=lambda a: a.name, reverse=True)
  newlc = find_launch(args.group, lcconfigs)
  if newlc:
    lc = newlc

if lc != None and lc.image_id != ami.id:
  asgupdate = True
  if verbose:
    print "launch config %s ami %s != %s" % (lc.name, lc.image_id, ami.id)
    sys.stdout.flush()

  # New launch config name
  now = datetime.datetime.utcnow()
  nowstr = now.strftime("%Y%m%d%H%M%S")
  lcnamefull = "%s-%s" % (args.group, nowstr)

  # Public flags are borked
  publicip = None
  try:
    if lc.AssociatePublicIpAddress:
      publicip = True
  except AttributeError:
    publicip = None
  if lc.associate_public_ip_address:
    publicip = True

  instmon = False
  if lc.instance_monitoring.enabled == u'true':
    instmon = True

  #
  # Existing LaunchConfig returns a list of BlockDeviceMapping()
  # Creating LaunchConfig requires a list with a single BlockDeviceMapping(),
  # which is a dict of BlockDeviceType()
  #
  mapping = None
  if len(lc.block_device_mappings) > 0:
    mapping = boto.ec2.blockdevicemapping.BlockDeviceMapping()
    for bdm in lc.block_device_mappings:
      # because, unicode
      devname = str(bdm.device_name)

      if bdm.ebs:
        print "EBS: %s/%s" % (str(bdm.ebs.volume_size), str(bdm.ebs.snapshot_id))
        deleteontermination = True
        try:
          if bdm.ebs.deleteontermination and bdm.ebs.deleteontermination == u'false':
            deleteontermination = False
        except AttributeError:
          deleteontermination = True
        mapping[devname] = boto.ec2.blockdevicemapping.BlockDeviceType(snapshot_id=bdm.ebs.snapshot_id, size=bdm.ebs.volume_size, delete_on_termination=deleteontermination)
      else:
        mapping[devname] = boto.ec2.blockdevicemapping.BlockDeviceType(ephemeral_name=bdm.virtual_name)
    
  maplist = None
  if mapping and len(mapping) > 0:
    maplist = [mapping]
  newlc = boto.ec2.autoscale.LaunchConfiguration(
      name = lcnamefull,
      image_id = ami.id,
      key_name = lc.key_name,
      security_groups = lc.security_groups,
      user_data = lc.user_data,
      instance_type = lc.instance_type,
      kernel_id = lc.kernel_id,
      ramdisk_id = lc.ramdisk_id,
      block_device_mappings = maplist,
      instance_monitoring = instmon,
      spot_price = lc.spot_price,
      instance_profile_name = lc.instance_profile_name,
      ebs_optimized = lc.ebs_optimized,
      associate_public_ip_address = publicip
  )
  req = awsasg.create_launch_configuration(newlc)
  if req == None:
    print "failed creating launch configuration %s" % lcnamefull
    sys.exit(1)
  if verbose:
    print "creating launch config %s ami %s type %s key %s role %s public %s" % (newlc.name, newlc.image_id, newlc.instance_type, newlc.key_name, newlc.instance_profile_name, publicip)
    sys.stdout.flush()
  lc = newlc

# Update Autoscale Group
if asgupdate and lc:
  print "updating %s from %s -> %s" % (asg.name, asg.launch_config_name, lc.name)
  sys.stdout.flush()
  asg.launch_config_name = lc.name
  asg.update()


def main():
  pass
