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

import six
import testtools

from openstack.auth import service_filter as filt
from openstack import exceptions


class TestServiceFilter(testtools.TestCase):
    def test_minimum(self):
        sot = filt.ServiceFilter()
        self.assertEqual("service_type=any,visibility=public",
                         six.text_type(sot))

    def test_maximum(self):
        sot = filt.ServiceFilter(service_type='compute', visibility='admin',
                                 region='b', service_name='c')
        exp = "service_type=compute,visibility=admin,region=b,service_name=c"
        self.assertEqual(exp, six.text_type(sot))

    def test_visibility(self):
        sot = filt.ServiceFilter(service_type='identity', visibility='public')
        self.assertEqual("service_type=identity,visibility=public",
                         six.text_type(sot))
        sot = filt.ServiceFilter(service_type='identity',
                                 visibility='internal')
        self.assertEqual("service_type=identity,visibility=internal",
                         six.text_type(sot))
        sot = filt.ServiceFilter(service_type='identity', visibility='admin')
        self.assertEqual("service_type=identity,visibility=admin",
                         six.text_type(sot))
        sot = filt.ServiceFilter(service_type='identity',
                                 visibility='publicURL')
        self.assertEqual("service_type=identity,visibility=public",
                         six.text_type(sot))
        sot = filt.ServiceFilter(service_type='identity',
                                 visibility='internalURL')
        self.assertEqual("service_type=identity,visibility=internal",
                         six.text_type(sot))
        sot = filt.ServiceFilter(service_type='identity',
                                 visibility='adminURL')
        self.assertEqual("service_type=identity,visibility=admin",
                         six.text_type(sot))
        self.assertRaises(exceptions.SDKException, filt.ServiceFilter,
                          service_type='identity', visibility='b')
        self.assertRaises(exceptions.SDKException, filt.ServiceFilter,
                          service_type='identity', visibility=None)

    def test_match_service_type(self):
        sot = filt.ServiceFilter(service_type='identity')
        self.assertTrue(sot.match_service_type('identity'))
        self.assertFalse(sot.match_service_type('compute'))

    def test_match_service_type_any(self):
        sot = filt.ServiceFilter()
        self.assertTrue(sot.match_service_type('identity'))
        self.assertTrue(sot.match_service_type('compute'))

    def test_match_service_name(self):
        sot = filt.ServiceFilter(service_type='identity')
        self.assertTrue(sot.match_service_name('keystone'))
        self.assertTrue(sot.match_service_name('ldap'))
        self.assertTrue(sot.match_service_name(None))
        sot = filt.ServiceFilter(service_type='identity',
                                 service_name='keystone')
        self.assertTrue(sot.match_service_name('keystone'))
        self.assertFalse(sot.match_service_name('ldap'))
        self.assertFalse(sot.match_service_name(None))

    def test_match_region(self):
        sot = filt.ServiceFilter(service_type='identity')
        self.assertTrue(sot.match_region('East'))
        self.assertTrue(sot.match_region('West'))
        self.assertTrue(sot.match_region(None))
        sot = filt.ServiceFilter(service_type='identity', region='East')
        self.assertTrue(sot.match_region('East'))
        self.assertFalse(sot.match_region('West'))
        self.assertFalse(sot.match_region(None))

    def test_match_visibility(self):
        sot = filt.ServiceFilter(service_type='identity',
                                 visibility='internal')
        self.assertFalse(sot.match_visibility('admin'))
        self.assertTrue(sot.match_visibility('internal'))
        self.assertFalse(sot.match_visibility('public'))

    def test_join(self):
        a = filt.ServiceFilter(region='east')
        b = filt.ServiceFilter(service_type='identity')
        result = a.join(b)
        self.assertEqual("service_type=identity,visibility=public,region=east",
                         six.text_type(result))
        self.assertEqual("service_type=any,visibility=public,region=east",
                         six.text_type(a))
        self.assertEqual("service_type=identity,visibility=public",
                         six.text_type(b))
