#!/bin/env python
# -*- coding: utf8 -*-
"""
Utility functions for fedimg.
"""

import socket
import subprocess

import paramiko

import fedimg


def get_file_arch(file_name):
    """ Takes a file name (probably of a .raw.xz image file) and returns
    the suspected architecture of the contained image. If it doesn't look
    like a 32-bit or 64-bit image, None is returned. """
    if file_name.find('i386') != -1:
        return 'i386'
    elif file_name.find('x86_64') != -1:
        return 'x86_64'
    else:
        return None


def get_rawxz_url(task_result):
    """ Returns the URL of the raw.xz file produced by the Koji
    task ID represented by the task_result argument. """
    # I think there might only ever be one qcow2 file per task,
    # but doing it this way plays it safe.
    file_name = [f for f in task_result['files'] if f.endswith('.raw.xz')][0]
    task_id = task_result['task_id']

    # extension to base URL to exact file directory
    koji_url_extension = "/{}/{}".format(str(task_id)[3:], str(task_id))
    full_file_location = fedimg.BASE_KOJI_TASK_URL + koji_url_extension

    return full_file_location + "/{}".format(file_name)


def ssh_connection_works(username, ip, keypath):
    """ Returns True if an SSH connection can me made to `username`@`ip`. """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    works = False
    try:
        ssh.connect(ip, username=username,
                    key_filename=keypath)
        works = True
    except (paramiko.BadHostKeyException,
            paramiko.AuthenticationException,
            paramiko.SSHException, socket.error) as e:
        pass
    ssh.close()
    return works
