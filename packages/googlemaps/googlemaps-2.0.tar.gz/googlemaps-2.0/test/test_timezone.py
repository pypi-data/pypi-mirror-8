# This Python file uses the following encoding: utf-8
#
# Copyright 2014 Google Inc. All rights reserved.
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#

"""Tests for the timezone module."""

import test as _test
import datetime

import googlemaps

class TimezoneTest(_test.TestCase):

    def setUp(self):
        self.c = googlemaps.Client(
            key="AIzaSyDyZdCabN8GKh786tdj16gq80xalbbfqDM",
            timeout=5)

    def test_los_angeles(self):
        timezone = self.c.timezone((39.6034810,-119.6822510), 1331766000)
        self.assertIsNotNone(timezone)
        self.assertEqual(3600.0, timezone['dstOffset'])
        self.assertEqual('America/Los_Angeles', timezone['timeZoneId'])
        self.assertEqual('Pacific Daylight Time', timezone['timeZoneName'])

    def test_los_angeles_es(self):
        timezone = self.c.timezone((39.6034810,-119.6822510), 1331766000, language='es')
        self.assertIsNotNone(timezone)
        self.assertEqual(3600.0, timezone['dstOffset'])
        self.assertEqual('America/Los_Angeles', timezone['timeZoneId'])
        self.assertEqual(self.u('Hora de verano del Pac\\xedfico'), timezone['timeZoneName'])

    def test_los_angeles_with_no_timestamp(self):
        timezone = self.c.timezone((39.6034810,-119.6822510))
        self.assertIsNotNone(timezone)
        self.assertEqual('America/Los_Angeles', timezone['timeZoneId'])
