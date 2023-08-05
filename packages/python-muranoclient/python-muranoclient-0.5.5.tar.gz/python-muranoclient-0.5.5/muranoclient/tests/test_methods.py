#    Copyright (c) 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

import mock
import testtools

from muranoclient import client
from muranoclient.v1 import actions
import muranoclient.v1.environments as environments
import muranoclient.v1.sessions as sessions


def my_mock(*a, **b):
    return [a, b]


LOG = logging.getLogger('Unit tests')
api = mock.MagicMock(json_request=my_mock)


class UnitTestsForClassesAndFunctions(testtools.TestCase):
    def test_create_client_instance(self):

        endpoint = 'http://no-resolved-host:8001'
        test_client = client.Client('1', endpoint=endpoint,
                                    token='1', timeout=10)

        self.assertIsNotNone(test_client.environments)
        self.assertIsNotNone(test_client.sessions)
        self.assertIsNotNone(test_client.services)

    def test_env_manager_list(self):
        manager = environments.EnvironmentManager(api)
        result = manager.list()

        self.assertEqual([], result)

    def test_env_manager_create(self):
        manager = environments.EnvironmentManager(api)
        result = manager.create({'name': 'test'})

        self.assertEqual({'name': 'test'}, result.data)

    def test_env_manager_create_with_named_parameters(self):
        manager = environments.EnvironmentManager(api)
        result = manager.create(data={'name': 'test'})

        self.assertEqual({'name': 'test'}, result.data)

    def test_env_manager_create_negative_without_parameters(self):

        manager = environments.EnvironmentManager(api)

        self.assertRaises(TypeError, manager.create)

    def test_env_manager_delete(self):
        manager = environments.EnvironmentManager(api)
        result = manager.delete('test')

        self.assertIsNone(result)

    def test_env_manager_delete_with_named_parameters(self):
        manager = environments.EnvironmentManager(api)
        result = manager.delete(environment_id='1')

        self.assertIsNone(result)

    def test_env_manager_delete_negative_without_parameters(self):

        manager = environments.EnvironmentManager(api)

        self.assertRaises(TypeError, manager.delete)

    def test_env_manager_update(self):
        manager = environments.EnvironmentManager(api)
        result = manager.update('1', 'test')

        self.assertEqual({'name': 'test'}, result.data)

    def test_env_manager_update_with_named_parameters(self):
        manager = environments.EnvironmentManager(api)
        result = manager.update(environment_id='1',
                                name='test')

        self.assertEqual({'name': 'test'}, result.data)

    def test_env_manager_update_negative_with_one_parameter(self):

        manager = environments.EnvironmentManager(api)

        self.assertRaises(TypeError, manager.update, 'test')

    def test_env_manager_update_negative_without_parameters(self):

        manager = environments.EnvironmentManager(api)

        self.assertRaises(TypeError, manager.update)

    def test_env_manager_get(self):
        manager = environments.EnvironmentManager(api)
        result = manager.get('test')

        self.assertIsNotNone(result.manager)

    def test_env(self):
        environment = environments.Environment(api, api)

        self.assertIsNotNone(environment.data())

    def test_session_manager_delete(self):
        manager = sessions.SessionManager(api)
        result = manager.delete('datacenter1', 'session1')

        self.assertIsNone(result)

    def test_session_manager_delete_with_named_parameters(self):
        manager = sessions.SessionManager(api)
        result = manager.delete(environment_id='datacenter1',
                                session_id='session1')

        self.assertIsNone(result)

    def test_session_manager_delete_negative_with_one_parameter(self):

        manager = sessions.SessionManager(api)

        self.assertRaises(TypeError, manager.delete, 'datacenter1')

    def test_session_manager_delete_negative_without_parameters(self):

        manager = sessions.SessionManager(api)

        self.assertRaises(TypeError, manager.delete)

    def test_session_manager_get(self):
        manager = sessions.SessionManager(api)
        result = manager.get('datacenter1', 'session1')
        # WTF?
        self.assertIsNotNone(result.manager)

    def test_session_manager_configure(self):
        manager = sessions.SessionManager(api)
        result = manager.configure('datacenter1')

        self.assertIsNotNone(result)

    def test_session_manager_configure_with_named_parameter(self):
        manager = sessions.SessionManager(api)
        result = manager.configure(environment_id='datacenter1')

        self.assertIsNotNone(result)

    def test_session_manager_configure_negative_without_parameters(self):

        manager = sessions.SessionManager(api)

        self.assertRaises(TypeError, manager.configure)

    def test_session_manager_deploy(self):
        manager = sessions.SessionManager(api)
        result = manager.deploy('datacenter1', '1')

        self.assertIsNone(result)

    def test_session_manager_deploy_with_named_parameters(self):
        manager = sessions.SessionManager(api)
        result = manager.deploy(environment_id='datacenter1',
                                session_id='1')

        self.assertIsNone(result)

    def test_session_manager_deploy_negative_with_one_parameter(self):

        manager = sessions.SessionManager(api)

        self.assertRaises(TypeError, manager.deploy, 'datacenter1')

    def test_session_manager_deploy_negative_without_parameters(self):

        manager = sessions.SessionManager(api)

        self.assertRaises(TypeError, manager.deploy)

    def test_action_manager_call(self):
        manager = actions.ActionManager(api)
        result = manager.call('testEnvId', 'testActionId', ['arg1', 'arg2'])
        self.assertEqual(('POST',
                          '/v1/environments/testEnvId/actions/testActionId'),
                         result)
