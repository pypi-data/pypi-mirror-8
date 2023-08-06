#!/usr/bin/env python

import sys
from optparse import OptionParser
from utils.config import Config
from utils.rds import RDS
from utils.elasticache import Elasticache
from utils.ec2 import EC2
from utils.elb import ELB



def ec2(mode, config):
    x = EC2(config)
    if mode == 'create':
        x.create()
    elif mode == 'delete':
        x.delete()


def elb(mode, config):
    x = ELB(config)
    if mode == 'create':
        x.create()
    elif mode == 'delete':
        x.delete()


def rds(mode, config):
    x = RDS(config)
    if mode == 'create':
        x.create()
    elif mode == 'delete':
        x.delete()


def elasticache(mode, config):
    x = Elasticache(config)
    if mode == 'create':
        x.create()
    elif mode == 'delete':
        x.delete()


def main():
    parser = OptionParser()
    parser.add_option('-a', '--access', dest='aws_access', default=None,
                      help='AWS Access key')
    parser.add_option('-s', '--secret', dest='aws_secret', default=None,
                      help='AWS Secret key')
    parser.add_option('-m', '--mode', dest='mode', default=None,
                      help='Mode [create or delete]')
    parser.add_option('-e', '--env', dest='env', default=None,
                      help='Set the environment')
    parser.add_option('-i', '--item', dest='item', default=None,
                      help='Set the AWS service item you want create/delete [ec2,elb,elasticache,rds]')
    parser.add_option('-c', '--config', dest='config', default='config.yml',
                      help='Override the default config.yml file')

    (options, args) = parser.parse_args()

    """
    Required parameters
    """
    if options.aws_access == None:
        print "\n[ERROR] Please specify an AWS Access key `-a`"
        print sys.exit(1)
    if options.aws_secret == None:
        print "\n[ERROR] Please specify an AWS Secret key `-s`"
        print sys.exit(1)
    if options.mode == None or options.mode not in ['create', 'delete']:
        print "\n[ERROR] Please specify a valid mode e.g. `-m create`"
        print sys.exit(1)
    if options.env == None:
        print "\n[ERROR] Please specify an environment `-e`"
        print sys.exit(1)
    """
    Based on whether an AWS service item was specified, build everything or just one item
    """

    # CONFIG SETUP
    config = Config(options.aws_access, options.aws_secret)
    config.set_config_from_file(options.config, options.env)

    # BUILD
    if options.item != None:
        if options.item in ['ec2', 'elb', 'elasticache', 'rds']:
            if options.item == 'ec2':
                ec2(options.mode, config)
            elif options.item == 'elb':
                elb(options.mode, config)
            elif options.item == 'elasticache':
                elasticache(options.mode, config)
            elif options.item == 'rds':
                rds(options.mode, config)
        else:
            print "\n[ERROR] Please enter a valid item [ec2,elb,elasticache,rds]"
    else:
        print "\n--- APPLYING TO ENTIRE ENV: %s ---\n" % options.env
        rds(options.mode, config)
        elasticache(options.mode, config)
        elb(options.mode, config)
        ec2(options.mode, config)


if __name__ == "__main__":
    main()
