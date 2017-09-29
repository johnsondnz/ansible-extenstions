"""
(c) 2017 Donald Johnson <donald@it-ninja.xyz>

This file is part of Ansible

Ansible is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Ansible is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
"""
from ansible.module_utils.basic import AnsibleModule, return_values


DOCUMENTATION = '''
---
module: unit_test
author: "Donald Johnson (@johnsondnz)"
version_added: "0.1"
short_description: "Custom module to decern pass/fail of a specified test and return as ansible facts."
description:
    - "Custom module to decern pass/fail of a specified test and return as ansible facts."
options:
    fact_name: Desired fact name, auto prepended with 'unit_test_'
    data: JSON data to iterate over
    condition: condition that must be met to 'PASS'
    key: the key to check either exists or value is present
    search: value to look for
    test_name: Name of test
    description: Brief description of the unit test
'''

EXAMPLE = '''

- set_fact: test_name=System Alarms
- name: "{{test_name}} Check"
  unit_test:
    fact_name: system_alarms
    test_name: "{{test_name}}"
    description: Check for alarms
    key: no-active-alarms
    data: "{{getter_system_alarms}}"
    condition: key-exists

ansible_fact:
"unit_test_system_alarms": {
  "test_result": "[PASS]",
  "test_name": "System",
  "test_description": "Check for alarms"
}

'''

RETURN = '''
ansible_facts:
    description: "Facts based on test conditions"
    returned: PASS / FAIL
    type: dict
'''


def main():
    # define the available arguments/parameters that a user can pass to
    # the module
    module_args = dict(
        fact_name=dict(type='str', required=True),
        test_name=dict(type='str', required=True),
        data=dict(type='dict', required=True),
        condition=dict(type='str', required=True, choices=['key-exists']),
        key=dict(type='str', required=False),
        search=dict(type='str', required=False),
        description=dict(type='str', required=True),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Setup easy to reference variables
    fact_name = module.params['fact_name']
    test_name = module.params['test_name']
    data = module.params['data']
    condition = module.params['condition']
    key = module.params['key']
    search = module.params['search']
    description = module.params['description']

    # Run the unit test
    # currently supports single route-engine and no loops
	# more is planned to iterate and search recursively
    new_facts = {}
    for key, item in data.items():
        if condition == 'key-exists':
            for k, v in data.items():
                if key in k:
                    test_result = '[PASS]'
                else:
                    test_result = '[FAIL]'

    # Create facts object
    new_facts = {
        # prepend unit_test_ to all facts
        'unit_test_' + fact_name: {
            'test_name': test_name,
            'test_description': description,
            'test_result': test_result
        }
    }
    # Prep the ansible_facts
    results = {'ansible_facts': new_facts}

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        return results

    module.exit_json(**results)


if __name__ == '__main__':
    main()
