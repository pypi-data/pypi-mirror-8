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
import os
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
parser.add_argument("-c", "--count", help="concurrent rotations", default=1)
parser.add_argument("-s", "--sleep", help="wait sleep", default=5)
parser.add_argument("-T", "--turbo", help="turbo mode", action="store_true", default=False)
parser.add_argument("-n", "--num", help="number of hosts to rotate, 0 = all",
        type=int, default=0)
parser.add_argument("-i", "--instance", help="specific instance to rotate")
parser.add_argument("group", help="autoscale group to rotoate")
args = parser.parse_args()
if args.group == None:
  parser.print_help()
  sys.exit(1)

if args.region == None:
  args.region = 'us-east-1'

verbose = args.verbose
awsec2 = boto.ec2.connect_to_region(args.region, aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
awselb = boto.ec2.elb.connect_to_region(args.region, aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
awsasg = boto.ec2.autoscale.connect_to_region(args.region, aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)

oldinst = []
newinst = []
azcount = {}

if verbose:
  print "%s rotating autoscale group in %s with count %i" % (args.group, args.region, args.count)
  sys.stdout.flush()

all_groups = awsasg.get_all_groups([args.group])
if len(all_groups) == 0:
    print "no groups found matching %s, exiting" % (args.group)
    sys.exit(1)

asg = all_groups[0]

capacity = asg.desired_capacity

# start count of AZ instances
for az in asg.availability_zones:
  azcount[str(az)] = 0

# store original instance list
for i in asg.instances:
    # when asked to rotate a single instance, only allow that instance
    if args.instance and i.instance_id != args.instance:
        continue
    oldinst.append(i.instance_id)
    azcount[str(i.availability_zone)] += 1

if len(oldinst) == 0:
    print "no instances to rotate, exiting"
    sys.exit(1)

if verbose:
    if args.num > 0:
        print "%s rotating %i/%i instances" % (args.group, args.num,
                len(oldinst))
    else:
        print "%s rotating %i instances" % (args.group, len(oldinst))
    sys.stdout.flush()

lbs = []
if asg.load_balancers:
  lbs = awselb.get_all_load_balancers(asg.load_balancers)

#
# Warn of dangerous things for ops people
#

if not args.turbo:
  # check for reduced redundancy in each zone, warn if AZ will empty
  for azname, count in azcount.items():
    if count > 0 and count <= args.count and \
            asg.max_size <= asg.desired_capacity:
      print "WARNING: rotation will temporarily reduce redundancy in zone %s" % azname
      sys.stdout.flush()

  if len(oldinst) < 2 and asg.max_size <= asg.desired_capacity:
    print "WARNING: single autoscale instance, using accelerated rotation"
    sys.stdout.flush()

  # check cross-zone load balancing - warn if empty AZ will deadend requests
  for lb in lbs:
    if lb.is_cross_zone_load_balancing() != True:
      for azname, count in azcount.items():
        if count > 0 and count <= 1:
          print "WARNING: rotation will cause user-facing outages in zone %s" % azname

#
# Wait for all instances to register as healthy
#
def elb_wait_healthy(inst=None):
  global asg

  if verbose:
    print "%s verifying all ELB instances healthy" % asg.name
    sys.stdout.flush()
  healthy = False
  while not healthy:
    healthycnt = 0
    healthyneed = 0
    lbs = []
    if asg.load_balancers:
      lbs = awselb.get_all_load_balancers(asg.load_balancers)
    for lb in lbs:
      healths = awselb.describe_instance_health(lb.name)
      healthyneed += len(healths)
      for h in healths:
          if h.state == u'InService':
              healthycnt += 1
          elif inst and str(h.instance_id) == str(inst):
              # old instance does not count, call it healthy
              healthycnt += 1
    if healthycnt == healthyneed:
      healthy = True

    # sleep a few
    if healthy != True:
      time.sleep(args.sleep)

  return

#
# Wait for instance to register to ELB
#
def elb_wait_registered(inst):
  global asg

  if verbose:
    print "%s %s waiting for ELB registration" % (args.group, inst)
    sys.stdout.flush()
  healthy = False
  while not healthy:
    healthycnt = 0
    lbs = []
    if asg.load_balancers:
      lbs = awselb.get_all_load_balancers(asg.load_balancers)
    for lb in lbs:
      healths = awselb.describe_instance_health(lb.name, [inst])
      for h in healths:
        if h.state == u'InService':
          healthycnt += 1
    if healthycnt == len(lbs):
      healthy = True

    # sleep a few
    if healthy != True:
      time.sleep(args.sleep)

  return

def asg_remove_instance(instance, elbwait=True, decrement=False):
    # remove instance from ELB
    elbsleep = 0
    for lb in lbs:
        if verbose:
            print "%s %s removing from ELB %s" % (asg.name, instance, lb.name)
            sys.stdout.flush()
        awselb.deregister_instances(lb.name, instance)
        elbsleep = max(elbsleep,
                lb.health_check.interval * lb.health_check.healthy_threshold)

    # only sleep if this is a controlled rotation
    if elbwait:
        if verbose:
            print "%s %s waiting %d seconds for ELB deregistration" % (
                    args.group, instance, elbsleep)
            sys.stdout.flush()
        time.sleep(elbsleep)

    # remove instance from ASG
    if verbose:
        print "%s %s autoscale terminating" % (args.group, instance)
        sys.stdout.flush()
    awsasg.terminate_instance(instance, decrement_capacity=decrement)
    return

#
# Turbo mode rotation - double, then half
#
if args.turbo:
  print "%s engaging TURBO rotation of %d -> %d hosts" % (args.group, len(oldinst), capacity * 2)
  sys.stdout.flush()

  if asg.max_size < (capacity * 2):
      print "%s cannot use TURBO rotation, max size is %d but need %d" % (args.group, asg.max_size, capacity * 2)
      sys.exit(1)

  # set desired capacity to double
  asg.desired_capacity = capacity * 2
  asg.update()

  # wait for instances to start
  if verbose:
    print "%s waiting for autoscale instances to reach %d" % (args.group, asg.desired_capacity)
    sys.stdout.flush()
  healthy = False
  while not healthy:
    healthycnt = 0
    asg = awsasg.get_all_groups([args.group])[0]
    for i in asg.instances:
      if i.lifecycle_state == u'InService':
        healthycnt += 1
      if i.instance_id not in oldinst and i.instance_id not in newinst:
        newinst.append(i.instance_id)
        thisnewinst = i.instance_id
        if verbose:
          print "%s %s is %s" % (args.group, i.instance_id, str(i.lifecycle_state))
          sys.stdout.flush()
        else:
          print "%s" % i.instance_id
          sys.stdout.flush()
    if healthycnt >= asg.desired_capacity:
      healthy = True

    # sleep a few
    if healthy != True:
      time.sleep(args.sleep)

  # wait for all instances in the autoscale group to register healthy
  elb_wait_healthy()

  # remove old from ELB
  elbsleep = 0
  for i in oldinst:
    for lb in lbs:
      if verbose:
        print "%s %s removing from ELB %s" % (asg.name, i, lb.name)
        sys.stdout.flush()
      try:
        awselb.deregister_instances(lb.name, i)
      except boto.exception.BotoServerError:
        print "%s FAILED deregistering %s from %s" % (asg.name, i, lb.name)
        sys.stdout.flush()
      elbsleep = max(elbsleep, lb.health_check.interval * lb.health_check.healthy_threshold)
  if verbose:
    print "%s waiting %d seconds for ELB deregistration" % (args.group, elbsleep)
    sys.stdout.flush()
  time.sleep(elbsleep)

  # terminate old
  for i in oldinst:
    if verbose:
      print "%s %s autoscale terminating" % (args.group, i)
      sys.stdout.flush()
    try:
      awsasg.terminate_instance(i, decrement_capacity=True)
    except boto.exception.BotoServerError:
      print "%s FAILED terminating %s" % (args.group, i)
      sys.stdout.flush()

  # reduce desired capacity
  if verbose:
    print "%s returning desired capacity from %d -> %d instances" % (args.group, capacity * 2, capacity)
  asg.desired_capacity = capacity
  asg.update()

  # Turbo rotation stops here
  sys.exit(0)

#
# Standard mode rotation:
# - if the autoscale group has capacity, start and wait then terminate
# - otherwise, terminate and wait for new instance to come InService
#
startfirst = False
if asg.max_size > asg.desired_capacity:
    startfirst = True

instrotate = 0
for thisinst in oldinst:
  thisnewinst = None
  elasticip = None
  internalip = None
  internaleni = None

  if args.num > 0 and instrotate >= args.num:
      print "%s finished rotating requested %d/%d instances" % (args.group,
              args.num, len(oldinst))
      sys.exit(0)
  instrotate += 1

  # Determine if ElasticIP is in use, and save it for the new instance
  addrinsts = awsec2.get_only_instances(thisinst)
  for i in addrinsts:
      for ni in i.interfaces:
          # ElasticIPs are owned by account number, standard by 'amazon'
          if hasattr(ni, 'ipOwnerId') and str(ni.ipOwnerId) != 'amazon':
              addrs = awsec2.get_all_addresses(ni.publicIp)
              if len(addrs) > 0:
                  elasticip = addrs[0]
                  break
      if elasticip:
          break

  # Determine if Secondary IP is in use, and save for new instance
  for i in addrinsts:
      for ni in i.interfaces:
          if len(ni.private_ip_addresses) > 1:
              internalip = ni.private_ip_addresses[1].private_ip_address
              internaleni = ni.id
              break

  if not verbose:
    # first part of rotating i-xxxxxx -> i-xxxxxx
    print "%s rotating %s ->" % (args.group, thisinst),
    sys.stdout.flush()

  # only sleep if this is a controlled rotation
  elbwait = True
  if len(oldinst) > 1:
      elbwait = False

  if elasticip:
      if verbose:
          print "%s %s disassociating ElasticIP %s" % (args.group, thisinst,
                  elasticip.public_ip)
          sys.stdout.flush()
      elasticip.disassociate()

  if internalip:
      if verbose:
          print "%s %s disassociating Secondary IP %s" % (args.group, thisinst,
                  internalip)
          sys.stdout.flush()
      awsec2.unassign_private_ip_addresses(
              network_interface_id=internaleni,
              private_ip_addresses=internalip)

  if startfirst:
      asg = awsasg.get_all_groups([args.group])[0]
      asg.desired_capacity += 1
      asg.update()
  else:
      asg_remove_instance(thisinst, elbwait, False)

  # wait for ASG to start new instance
  if verbose:
    print "%s waiting for autoscale instance" % args.group
    sys.stdout.flush()
  healthy = False
  while not healthy:
    healthycnt = 0
    asg = awsasg.get_all_groups([args.group])[0]
    for i in asg.instances:
      if i.lifecycle_state == u'InService':
        healthycnt += 1
      if i.instance_id not in oldinst and i.instance_id not in newinst:
        newinst.append(i.instance_id)
        thisnewinst = i.instance_id
        if verbose:
          print "%s %s is %s" % (args.group, i.instance_id, str(i.lifecycle_state))
          sys.stdout.flush()
        else:
          # second part of rotating i-xxxxxx -> i-xxxxxx
          print "%s" % i.instance_id
          sys.stdout.flush()
    if healthycnt >= asg.desired_capacity:
      healthy = True

    # sleep a few
    if healthy != True:
      time.sleep(args.sleep)

  if elasticip:
      if verbose:
          print "%s %s associating ElasticIP %s" % (args.group, thisnewinst,
                  elasticip.public_ip)
          sys.stdout.flush()
      elasticip.associate(thisnewinst, allow_reassociation=True)

  if internalip:
      if verbose:
          print "%s %s associating Secondary IP %s" % (args.group, thisnewinst,
                  internalip)
          sys.stdout.flush()
      internaleni = None
      for i in awsec2.get_only_instances(thisnewinst):
          internaleni = i.interfaces[0].id
      awsec2.assign_private_ip_addresses(
              network_interface_id=internaleni,
              private_ip_addresses=internalip,
              allow_reassignment=False)

  # wait for new instance to register to the ELB
  elb_wait_registered(thisnewinst)

  # wait for all instances in the autoscale group to register healthy
  elb_wait_healthy(thisinst)

  if startfirst:
      asg_remove_instance(thisinst, elbwait, True)


def main():
  pass
