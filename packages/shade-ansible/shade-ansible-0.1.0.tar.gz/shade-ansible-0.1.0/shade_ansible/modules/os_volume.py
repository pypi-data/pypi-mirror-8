#!/usr/bin/python

# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
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

import time

try:
    from shade_ansible import spec
    import shade
except ImportError:
    print("failed=True msg='shade is required for this module'")

from cinderclient import exceptions as cinder_exc


DOCUMENTATION = '''
---
module: os_volume
short_description: Create/Delete Cinder Volumes
extends_documentation_fragment: openstack
description:
   - Create or Remove cinder block storage volumes
options:
   state:
     description:
        - Indicate desired state of the resource
     choices: ['present', 'absent']
     default: present
   size:
     description:
        - Size of volume in GB
     requried: true
     default: None
   display_name:
     description:
        - Name of volume
     required: true
     default: None
   display_description:
     description:
       - String describing the volume
     required: false
     default: None
   volume_type:
     description:
       - Volume type for volume
     required: false
     default: None
   image_id:
     descritpion:
       - Image id for boot from volume 
     required: false
     default: None
   image_name:
     descritpion:
       - Image name for boot from volume 
     required: false
     default: None
   snapshot_id:
     description:
       - Volume snapshot id to create from
     required: false
     default: None
requirements: ["shade"]
'''

EXAMPLES = '''
# Creates a new volume
- name: create a volume
  hosts: localhost
  tasks:
  - name: create 40g test volume
    os_volume:
      state: present
      username: username
      password: Equality7-2521
      project_name: username-project1
      auth_url: https://region-b.geo-1.identity.hpcloudsvc.com:35357/v2.0/
      region_name: region-b.geo-1
      availability_zone: az2
      size: 40
      display_name: test_volume
'''

def _present_volume(module, cinder, cloud):
    for v in cinder.volumes.list():
        if v.display_name == module.params['display_name']:
            module.exit_json(changed=False, id=v.id, info=v._info)
    image_id = module.params['image_id']
    if module.params['image_name']:
        image_id = cloud.get_image_id(module.params['image_name'])
    volume_args = dict(
        size=module.params['size'],
        volume_type=module.params['volume_type'],
        display_name=module.params['display_name'],
        display_description=module.params['display_description'],
        imageRef=image_id,
        snapshot_id=module.params['snapshot_id'],
        availability_zone=module.params['availability_zone'],
    )
    try:
        vol = cinder.volumes.create(**volume_args)
    except Exception as e:
        module.fail_json(msg='Error creating volume:%s' % str(e))

    if module.params['wait']:
        expires = module.params['timeout'] + time.time()
        while time.time() < expires:
            volume = cinder.volumes.get(vol.id)
            if volume.status == 'available':
                break
            if volume.status == 'error':
                module.fail_json(msg='Error creating volume')
            time.sleep(5)
    module.exit_json(changed=True, id=vol.id, info=vol._info)


def _wait_for_delete(cinder, vol_id, timeout):
    expires = timeout + time.time()
    while time.time() < expires:
        try:
            cinder.volumes.get(vol_id)
        except cinder_exc.NotFound:
            return True
        time.sleep(5)
    return False


def _absent_volume(module, cinder, cloud):

    volume_id = cloud.get_volume_id(module.params['display_name'])
    if not volume_id:
        module.exit_json(changed=False, result="Volume not Found")
    try:
        cinder.volumes.delete(v.id)
    except cinder_exc, e:
        module.fail_json(msg='Cannot delete volume:%s' % str(e))
    if module.params['wait']:
        if not _wait_for_delete(cinder, v.id, module.params['timeout']):
            module.exit_json(changed=False, result="Volume deletion timed-out")
    module.exit_json(changed=True, result='Volume Deleted')


def main():
    argument_spec = spec.openstack_argument_spec(
        size=dict(required=True),
        volume_type=dict(default=None),
        display_name=dict(required=True),
        display_description=dict(default=None),
        image_id=dict(default=None),
        image_name=dict(default=None),
        snapshot_id=dict(default=None),
    )
    module_kwargs = spec.openstack_module_kwargs(
        mutually_exclusive = [
            ['image_id', 'snapshot_id'],
            ['image_name', 'snapshot_id'],
            ['image_id', 'image_name']
        ],
    )
    module = AnsibleModule(argument_spec=argument_spec, **module_kwargs)

    try:
        cloud = shade.openstack_cloud(**module.params)
        cinder = cloud.cinder_client
        if module.params['state'] == 'present':
            _present_volume(module, cinder, cloud)
        if module.params['state'] == 'absent':
            _absent_volume(module, cinder, cloud)
    except shade.OpenStackCloudException as e:
        module.fail_json(msg=e.message)

# this is magic, see lib/ansible/module_common.py
from ansible.module_utils.basic import *
from ansible.module_utils.openstack import *
main()
