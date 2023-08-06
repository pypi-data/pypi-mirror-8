#!/usr/bin/python

# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
# Copyright (c) 2013, Benno Joy <benno@ansible.com>
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

try:
    import shade
    from shade_ansible import spec
except ImportError:
    print("failed=True msg='shade is required for this module'")


DOCUMENTATION = '''
---
module: os_image
short_description: Add/Delete images from OpenStack Cloud
extends_documentation_fragment: openstack
description:
   - Add or Remove images from the OpenStack Image Repository
options:
   state:
     description:
        - Indicate desired state of the resource
     choices: ['present', 'absent']
     default: present
   name:
     description:
        - Name that has to be given to the image
     required: true
     default: None
   disk_format:
     description:
        - The format of the disk that is getting uploaded
     required: false
     default: qcow2
   container_format:
     description:
        - The format of the container
     required: false
     default: bare
   owner:
     description:
        - The owner of the image
     required: false
     default: None
   min_disk:
     description:
        - The minimum disk space required to deploy this image
     required: false
     default: None
   min_ram:
     description:
        - The minimum ram required to deploy this image
     required: false
     default: None
   is_public:
     description:
        - Whether the image can be accessed publicly
     required: false
     default: 'yes'
   copy_from:
     description:
        - A url from where the image can be downloaded, mutually exclusive with file parameter
     required: false
     default: None
   timeout:
     description:
        - The time to wait for the image process to complete in seconds
     required: false
     default: 180
   file:
     description:
        - The path to the file which has to be uploaded, mutually exclusive with copy_from
     required: false
     default: None
requirements: ["shade"]
'''

EXAMPLES = '''
# Upload an image from an HTTP URL
- os_image: username=admin
                password=passme
                project_name=admin
                name=cirros
                container_format=bare
                disk_format=qcow2
                state=present
                copy_from=http:launchpad.net/cirros/trunk/0.3.0/+download/cirros-0.3.0-x86_64-disk.img
'''

import time


def _glance_image_create(module, params, client):
    kwargs = {
                'name':             params.get('name'),
                'disk_format':      params.get('disk_format'),
                'container_format': params.get('container_format'),
                'owner':            params.get('owner'),
                'is_public':        params.get('is_public'),
                'copy_from':        params.get('copy_from'),
    }
    try:
        timeout = params.get('timeout')
        expire = time.time() + timeout
        image = client.images.create(**kwargs)
        if not params['copy_from']:
            image.update(data=open(params['file'], 'rb'))
        while time.time() < expire:
            image = client.images.get(image.id)
            if image.status == 'active':
                break
            time.sleep(5)
    except Exception, e:
        module.fail_json(msg="Error in creating image: %s" % e.message)
    if image.status == 'active':
        module.exit_json(changed=True, result=image.status, id=image.id)
    else:
        module.fail_json(msg=" The module timed out, please check manually " + image.status)


def _glance_delete_image(module, params, client):
    try:
        for image in client.images.list():
            if image.name == params['name']:
                client.images.delete(image)
    except Exception, e:
        module.fail_json(msg="Error in deleting image: %s" % e.message)
    module.exit_json(changed=True, result="Deleted")


def main():

    argument_spec = spec.openstack_argument_spec(
        name              = dict(required=True),
        disk_format       = dict(default='qcow2', choices=['aki', 'vhd', 'vmdk', 'raw', 'qcow2', 'vdi', 'iso']),
        container_format  = dict(default='bare', choices=['aki', 'ari', 'bare', 'ovf']),
        owner             = dict(default=None),
        min_disk          = dict(default=None),
        min_ram           = dict(default=None),
        is_public         = dict(default=True),
        copy_from         = dict(default= None),
        file              = dict(default=None),
    )
    module_kwargs = spec.openstack_module_kwargs(
        mutually_exclusive = [['file','copy_from']],
    )
    module = AnsibleModule(argument_spec, **module_kwargs)

    if module.params['state'] == 'present':
        if not module.params['file'] and not module.params['copy_from']:
            module.fail_json(msg="Either file or copy_from variable should be set to create the image")

    try:
        cloud = shade.openstack_cloud(**module.params)

        id = cloud.get_image_id(module.params['name'])

        if module.params['state'] == 'present':
            if not id:
                _glance_image_create(module, module.params, cloud.glance_client)
            module.exit_json(changed=False, id=id, result="success")

        if module.params['state'] == 'absent':
            if not id:
                module.exit_json(changed=False, result="Success")
            else:
                _glance_delete_image(module, module.params, cloud.glance_client)
    except shade.OpenStackCloudException as e:
        module.fail_json(msg=e.message)

# this is magic, see lib/ansible/module_common.py
from ansible.module_utils.basic import *
from ansible.module_utils.openstack import *
main()
