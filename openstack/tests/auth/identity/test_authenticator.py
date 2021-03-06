# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from openstack.auth.identity import authenticator
from openstack import exceptions
from openstack.tests import base


class TestAuthenticatorCreate(base.TestCase):
    def test_create_3_password(self):
        auth = authenticator.create(
            username='1',
            password='2',
            token=None,
            auth_url='4',
            version='3',
            project_name='6',
            domain_name='7',
            project_domain_name='8',
            user_domain_name='9',
        )
        self.assertEqual('1', auth.auth_methods[0].username)
        self.assertEqual('2', auth.auth_methods[0].password)
        self.assertEqual('4', auth.auth_url)
        self.assertEqual('6', auth.project_name)
        self.assertEqual('7', auth.domain_name)
        self.assertEqual('8', auth.project_domain_name)
        self.assertEqual('9', auth.auth_methods[0].user_domain_name)

    def test_create_3_token(self):
        auth = authenticator.create(
            username='1',
            password='2',
            token='3',
            auth_url='4',
            version='3',
            project_name='6',
        )
        self.assertEqual('3', auth.auth_methods[0].token)
        self.assertEqual('4', auth.auth_url)

    def test_create_2_password(self):
        auth = authenticator.create(
            username='1',
            password='2',
            token=None,
            auth_url='4',
            version='2',
            project_name='6',
        )
        self.assertEqual('1', auth.username)
        self.assertEqual('2', auth.password)
        self.assertEqual('4', auth.auth_url)
        self.assertEqual('6', auth.tenant_name)

    def test_create_2_token(self):
        auth = authenticator.create(
            username='1',
            password='2',
            token='3',
            auth_url='4',
            version='2',
            project_name='6',
        )
        self.assertEqual('3', auth.token)
        self.assertEqual('4', auth.auth_url)

    def test_create_bogus(self):
        self.assertRaises(
            exceptions.NoMatchingPlugin,
            authenticator.create,
            username='1',
            password='2',
            token='3',
            auth_url='4',
            version='99',
            project_name='6',
        )
