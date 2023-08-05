#!/bin/env python
# -*- coding: utf8 -*-

import logging
import os
import subprocess
from time import sleep

import paramiko
from libcloud.compute.base import NodeImage
from libcloud.compute.deployment import MultiStepDeployment
from libcloud.compute.deployment import ScriptDeployment, SSHKeyDeployment
from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider, DeploymentException
from libcloud.compute.types import KeyPairDoesNotExistError

import fedimg
import fedimg.messenger
from fedimg.util import get_file_arch, ssh_connection_works


class EC2ServiceException(Exception):
    """ Custom exception for EC2Service. """
    pass


class EC2UtilityException(EC2ServiceException):
    """ Something went wrong with writing the image file to a volume with the
        utility instance. """
    pass


class EC2AMITestException(EC2ServiceException):
    """ Something went wrong when a newly-registered AMI was tested. """
    pass


class EC2Service(object):
    """ A class for interacting with an EC2 connection. """

    def __init__(self):
        # Will be a list of dicts. Dicts will contain AMI info.
        self.amis = list()

        for line in fedimg.AWS_AMIS.split('\n'):
            """ Each line in AWS_AMIS has pipe-delimited attributes at these indicies:
            0: region (ex. eu-west-1)
            1: OS (ex. RHEL)
            2: version (ex. 5.7)
            3: arch (ex. x86_64)
            4: ami name (ex. ami-68e3d32d) """
            # strip line to avoid any newlines or spaces from sneaking in
            attrs = line.strip().split('|')
            info = {'region': attrs[0],
                    'prov': self._region_to_provider(attrs[0]),
                    'os': attrs[1],
                    'ver': attrs[2],
                    'arch': attrs[3],
                    'ami': attrs[4],
                    'aki': attrs[5]}
            self.amis.append(info)

    def _region_to_provider(self, region):
        """ Takes a region name (ex. 'eu-west-1') and returns
        the appropriate libcloud provider value. """
        providers = {'ap-northeast-1': Provider.EC2_AP_NORTHEAST,
                     'ap-southeast-1': Provider.EC2_AP_SOUTHEAST,
                     'ap-southeast-2': Provider.EC2_AP_SOUTHEAST2,
                     'eu-west-1': Provider.EC2_EU_WEST,
                     'sa-east-1': Provider.EC2_SA_EAST,
                     'us-east-1': Provider.EC2_US_EAST,
                     'us-west-1': Provider.EC2_US_WEST,
                     'us-west-2': Provider.EC2_US_WEST_OREGON}
        return providers[region]

    def upload(self, raw_url):
        """ Takes a URL to a .raw.xz file and registers it as an AMI in each
        EC2 region. """

        node = None
        volume = None
        sda_vol = None
        snapshot = None
        image = None
        test_node = None
        build_name = 'Fedimg build'
        destination = 'somewhere'
        test_success = False

        logging.info('EC2 upload process started')

        fedimg.messenger.message('image.upload', build_name, destination,
                                 'started')

        try:
            file_name = raw_url.split('/')[-1]
            build_name = file_name.replace('.raw.xz', '')
            image_arch = get_file_arch(file_name)
            ami = self.amis[0]
            destination = 'EC2 ({region})'.format(region=ami['region'])

            cls = get_driver(ami['prov'])
            driver = cls(fedimg.AWS_ACCESS_ID, fedimg.AWS_SECRET_KEY)

            # select the desired node attributes
            sizes = driver.list_sizes()
            size_id = 'm1.large'
            # check to make sure we have access to that size node
            size = [s for s in sizes if s.id == size_id][0]
            base_image = NodeImage(id=ami['ami'], name=None, driver=driver)

            # deploy node
            name = 'Fedimg AMI builder'
            mappings = [{'VirtualName': None,  # cannot specify with Ebs
                         'Ebs': {'VolumeSize': 12,  # 12 GB should be enough
                                 'VolumeType': 'standard',
                                 'DeleteOnTermination': 'false'},
                         'DeviceName': '/dev/sdb'}]

            # read in ssh key
            with open(fedimg.AWS_PUBKEYPATH, 'rb') as f:
                key_content = f.read()

            # Add key to authorized keys for root user
            step_1 = SSHKeyDeployment(key_content)

            # Add script for deployment
            # Device becomes /dev/xvdb on instance
            script = "touch test"
            step_2 = ScriptDeployment(script)

            # Create deployment object
            msd = MultiStepDeployment([step_1, step_2])

            logging.info('Deploying utility instance')

            # Must be EBS-backed for AMI registration to work.
            while True:
                try:
                    node = driver.deploy_node(name=name, image=base_image,
                                              size=size,
                                              ssh_username=fedimg.UTIL_USER,
                                              ssh_alternate_usernames=[''],
                                              ssh_key=fedimg.AWS_KEYPATH,
                                              deploy=msd,
                                              kernel_id=ami['aki'],
                                              ex_metadata={'build':
                                                           build_name},
                                              ex_keyname=fedimg.AWS_KEYNAME,
                                              ex_security_groups=['ssh'],
                                              ex_ebs_optimized=True,
                                              ex_blockdevicemappings=mappings)

                except KeyPairDoesNotExistError:
                    # The keypair is missing from the current region.
                    # Let's install it.
                    logging.exception('Adding missing keypair to region')
                    driver.ex_import_keypair(fedimg.AWS_KEYNAME,
                                             fedimg.AWS_PUBKEYPATH)
                    continue

                except Exception as e:
                    # We might have an invalid security group, aka the 'ssh'
                    # security group doesn't exist in the current region. The
                    # reason this is caught here is because the related
                    # exception that prints `InvalidGroup.NotFound` is, for
                    # some reason, a base exception.
                    if 'InvalidGroup.NotFound' in e.message:
                        logging.exception('Adding missing security'
                                          'group to region')
                        # Create the ssh security group
                        driver.ex_create_security_group('ssh', 'ssh only')
                        driver.ex_authorize_security_group('ssh', '22', '22',
                                                           '0.0.0.0/0')
                        continue
                    else:
                        raise
                break

            # Wait until the utility node has SSH running
            while not ssh_connection_works(fedimg.UTIL_USER,
                                           node.public_ips[0],
                                           fedimg.AWS_KEYPATH):
                sleep(10)

            logging.info('Utility node started with SSH running')

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(node.public_ips[0], username=fedimg.UTIL_USER,
                           key_filename=fedimg.AWS_KEYPATH)
            cmd = "sudo sh -c 'curl {0} | xzcat > /dev/xvdb'".format(raw_url)
            chan = client.get_transport().open_session()
            chan.get_pty()  # Request a pseudo-term to get around requiretty

            logging.info('Executing utility script')

            chan.exec_command(cmd)
            status = chan.recv_exit_status()
            if status != 0:
                # There was a problem with the SSH command
                logging.error('Problem writing volume with utility instance')
                raise EC2UtilityException("Problem writing image to"
                                          " utility instance volume."
                                          " Command exited with"
                                          " status {0}.\n"
                                          "command: {1}".format(status, cmd))
            client.close()

            # Get volume name that image was written to
            vol_id = [x['ebs']['volume_id'] for x in
                      node.extra['block_device_mapping'] if
                      x['device_name'] == '/dev/sdb'][0]

            logging.info('Destroying utility node')

            # Terminate the utility instance
            driver.destroy_node(node)

            # Wait for utility node to be terminated
            while ssh_connection_works(fedimg.UTIL_USER, node.public_ips[0],
                                       fedimg.AWS_KEYPATH):
                sleep(10)

            # Wait a little longer since loss of SSH connectivity doesn't mean
            # that the node's destroyed
            # TODO: Check instance state rather than this lame sleep thing
            sleep(45)

            # Take a snapshot of the volume the image was written to
            volume = [v for v in driver.list_volumes() if v.id == vol_id][0]
            snap_name = 'fedimg-snap-{0}'.format(build_name)

            logging.info('Taking a snapshot of the written volume')

            snapshot = driver.create_volume_snapshot(volume,
                                                     name=snap_name)
            snap_id = str(snapshot.id)

            while snapshot.extra['state'] != 'completed':
                # need to re-pull snapshot object to get updates
                snapshot = [s for s in driver.list_snapshots()
                            if s.id == snap_id][0]
                sleep(10)

            logging.info('Snapshot taken')

            # Delete the volume now that we've got the snapshot
            driver.destroy_volume(volume)
            volume = None  # make sure Fedimg knows that the vol is gone

            logging.info('Destroyed volume')

            # Block device mapping for the AMI
            mapping = [{'DeviceName': '/dev/sda',
                        'Ebs': {'SnapshotId': snap_id,
                                'VolumeSize': 12,
                                'VolumeType': 'standard',
                                'DeleteOnTermination': 'true'}}]

            # Actually register image
            logging.info('Registering image as an AMI')
            image_name = "{0}-{1}".format(build_name, ami['region'])
            # Avoid duplicate image name by adding a '-' and a number to the
            # end if there is already an AMI with that name.
            dup_count = 0  # counter: number of AMIs with same base image name
            while True:
                try:
                    if dup_count == 1:
                        image_name += '-1'  # avoid duplicate image name
                    elif dup_count > 1:
                        # Remove trailing '-1' or '-2' or '-3' or...
                        image_name = '-'.join(image_name.split('-')[:-1])
                        # Re-add trailing dup number with new count
                        image_name += '-{0}'.format(dup_count)
                    image = driver.ex_register_image(
                        image_name,
                        description=None,
                        root_device_name='/dev/sda',
                        block_device_mapping=mapping,
                        kernel_id=ami['aki'],
                        architecture=image_arch)
                except Exception as e:
                    if 'InvalidAMIName.Duplicate' in e.message:
                        dup_count += 1
                        continue  # Keep trying until an unused name is found
                    else:
                        raise
                break

            logging.info('Completed image registration')

            # Emit success fedmsg
            fedimg.messenger.message('image.upload', build_name, destination,
                                     'completed')

            # Spin up a node of the AMI to test

            # Add script for deployment
            # Device becomes /dev/xvdb on instance
            script = "touch test"
            step_2 = ScriptDeployment(script)

            # Create deployment object
            msd = MultiStepDeployment([step_1, step_2])

            mappings = [{'VirtualName': None,  # cannot specify with Ebs
                         'Ebs': {'VolumeSize': 12,  # 12 GB should be enough
                                 'VolumeType': 'standard',
                                 'DeleteOnTermination': 'true'},
                         'DeviceName': '/dev/sda'}]

            logging.info('Deploying test node')

            name = 'Fedimg AMI tester'
            test_node = driver.deploy_node(name=name, image=image, size=size,
                                           ssh_username=fedimg.TEST_USER,
                                           ssh_alternate_usernames=['root'],
                                           ssh_key=fedimg.AWS_KEYPATH,
                                           deploy=msd,
                                           kernel_id=ami['aki'],
                                           ex_metadata={'build': build_name},
                                           ex_keyname=fedimg.AWS_KEYNAME,
                                           ex_security_groups=['ssh'],
                                           ex_ebs_optimized=True)

            # Wait until the test node has SSH running
            while not ssh_connection_works(fedimg.TEST_USER,
                                           test_node.public_ips[0],
                                           fedimg.AWS_KEYPATH):
                sleep(10)

            logging.info('Starting AMI tests')

            # Alert the fedmsg bus that an image test has started
            fedimg.messenger.message('image.test', build_name, destination,
                                     'started')

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(test_node.public_ips[0], username=fedimg.TEST_USER,
                           key_filename=fedimg.AWS_KEYPATH)
            cmd = "true"
            chan = client.get_transport().open_session()
            chan.get_pty()  # Request a pseudo-term to get around requiretty

            logging.info('Running AMI test script')

            chan.exec_command(cmd)
            if chan.recv_exit_status() != 0:
                # There was a problem with the SSH command
                logging.error('Problem testing new AMI')
                raise EC2AMITestException("Tests on AMI failed.")

            logging.info('AMI test completed')
            fedimg.messenger.message('image.test', build_name, destination,
                                     'completed')
            test_success = True

            logging.info('Destroying test node')

            # Destroy the test node
            driver.destroy_node(test_node)

        except EC2UtilityException as e:
            fedimg.messenger.message('image.upload', build_name, destination,
                                     'failed')
            print "Failure:", e

        except EC2AMITestException as e:
            fedimg.messenger.message('image.test', build_name, destination,
                                     'failed')
            print "Failure:", e

        except DeploymentException as e:
            fedimg.messenger.message('image.upload', build_name, destination,
                                     'failed')
            print "Problem deploying node: {0}".format(e.value)
            print "Terminating instance."
            driver.destroy_node(e.node)

        except Exception as e:
            # Just give a general failure message.
            fedimg.messenger.message('image.upload', build_name, destination,
                                     'failed')
            print "Unexpected exception:", e
            print "Terminating instance and destroying other resources."
            if sda_vol:
                driver.destroy_volume(sda_vol)
            if snapshot:
                if image:
                    driver.delete_image(image)
                    driver.destroy_volume_snapshot(snapshot)

        finally:
            logging.info('Cleaning up resources')
            if node:
                driver.destroy_node(node)
                # Wait for node to be terminated
                while ssh_connection_works('ec2_user', node.public_ips[0],
                                           fedimg.AWS_KEYPATH):
                    sleep(10)
            if sda_vol:
                # Destroy /dev/sda volume if lagging behind
                driver.destroy_volume(sda_vol)
            if volume:
                # Destroy /dev/sdb or whatever
                driver.destroy_volume(volume)
            if test_node:
                driver.destroy_node(test_node)

        if test_success:
            # Copy the AMI to every other region if tests passed
            for ami in self.amis[1:]:
                # Avoid duplicate image name by adding a '-' and a number to
                # the end if there is already an AMI with that name.
                dup_count = 0  # counter: num of AMIs with same base image name
                while True:
                    try:
                        if dup_count == 1:
                            image_name += '-1'  # avoid duplicate image name
                        elif dup_count > 1:
                            # Remove trailing '-1' or '-2' or '-3' or...
                            image_name = '-'.join(image_name.split('-')[:-1])
                            # Re-add trailing dup number with new count
                            image_name += '-{0}'.format(dup_count)
                        alt_dest = 'EC2 ({region})'.format(
                            region=ami['region'])

                        fedimg.messenger.message('image.upload', build_name,
                                                 alt_dest, 'started')

                        alt_cls = get_driver(ami['prov'])
                        alt_driver = alt_cls(fedimg.AWS_ACCESS_ID,
                                             fedimg.AWS_SECRET_KEY)

                        image_name = "{0}-{1}".format(
                            build_name, ami['region'])

                        logging.info('AMI copy to {0} started'.format(
                            ami['region']))

                        alt_driver.copy_image(image, self.amis[0]['region'],
                                              name=image_name)

                        fedimg.messenger.message('image.upload', build_name,
                                                 alt_dest, 'completed')
                    except Exception as e:
                        if 'InvalidAMIName.Duplicate' in e.message:
                            # Keep trying until an unused name is found
                            dup_count += 1
                            continue
                        else:
                            # TODO: Catch a more specific exception
                            logging.exception(
                                'Image copy to {0} failed'.format(
                                    ami['region']))
                            fedimg.messenger.message('image.upload',
                                                     build_name,
                                                     alt_dest, 'failed')
                    break
