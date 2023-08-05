# vim: tabstop=4 shiftwidth=4 softtabstop=4
# Copyright 2009-2012 10gen, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test class of 3Par Client handling volume & snapshot."""

import os
import sys
sys.path.insert(0, os.path.realpath(os.path.abspath('../')))
from hp3parclient import exceptions
import HP3ParClient_base as hp3parbase

CPG_NAME1 = 'CPG1_UNIT_TEST' + hp3parbase.TIME
CPG_NAME2 = 'CPG2_UNIT_TEST' + hp3parbase.TIME
VOLUME_NAME1 = 'VOLUME1_UNIT_TEST' + hp3parbase.TIME
VOLUME_NAME2 = 'VOLUME2_UNIT_TEST' + hp3parbase.TIME
SNAP_NAME1 = 'SNAP_UNIT_TEST' + hp3parbase.TIME
DOMAIN = 'UNIT_TEST_DOMAIN'
VOLUME_SET_NAME1 = 'VOLUME_SET1_UNIT_TEST' + hp3parbase.TIME
VOLUME_SET_NAME2 = 'VOLUME_SET2_UNIT_TEST' + hp3parbase.TIME
SIZE = 512


class HP3ParClientVolumeTestCase(hp3parbase.HP3ParClientBaseTestCase):

    def setUp(self):
        super(HP3ParClientVolumeTestCase, self).setUp(withSSH=True)

        optional = self.CPG_OPTIONS
        try:
            self.cl.createCPG(CPG_NAME1, optional)
        except Exception:
            pass
        try:
            self.cl.createCPG(CPG_NAME2, optional)
        except Exception:
            pass

    def tearDown(self):

        try:
            self.cl.deleteVolumeSet(VOLUME_SET_NAME1)
        except Exception:
            pass
        try:
            self.cl.deleteVolumeSet(VOLUME_SET_NAME2)
        except Exception:
            pass
        try:
            self.cl.deleteVolume(VOLUME_NAME1)
        except Exception:
            pass
        try:
            self.cl.deleteVolume(VOLUME_NAME2)
        except Exception:
            pass
        try:
            self.cl.deleteCPG(CPG_NAME1)
        except Exception:
            pass
        try:
            self.cl.deleteCPG(CPG_NAME2)
        except Exception:
            pass

        super(HP3ParClientVolumeTestCase, self).tearDown()

    def test_1_create_volume(self):
        self.printHeader('create_volume')

        try:
            # add one
            optional = {'comment': 'test volume', 'tpvv': True}
            self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, SIZE, optional)
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume')
            return

        try:
            # check
            vol1 = self.cl.getVolume(VOLUME_NAME1)
            self.assertIsNotNone(vol1)
            volName = vol1['name']
            self.assertEqual(VOLUME_NAME1, volName)

        except Exception as ex:
            print(ex)
            self.fail('Failed to get volume')
            return

        try:
            # add another
            optional = {'comment': 'test volume2', 'tpvv': True}
            self.cl.createVolume(VOLUME_NAME2, CPG_NAME2, SIZE, optional)
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume')
            return

        try:
            # check
            vol2 = self.cl.getVolume(VOLUME_NAME2)
            self.assertIsNotNone(vol2)
            volName = vol2['name']
            comment = vol2['comment']
            self.assertEqual(VOLUME_NAME2, volName)
            self.assertEqual("test volume2", comment)
        except Exception as ex:
            print(ex)
            self.fail("Failed to get volume")

        self.printFooter('create_volume')

    def test_1_create_volume_badParams(self):
        self.printHeader('create_volume_badParams')
        try:
            name = VOLUME_NAME1
            cpgName = CPG_NAME1
            optional = {'id': 4, 'comment': 'test volume', 'badPram': True}
            self.cl.createVolume(name, cpgName, SIZE, optional)
        except exceptions.HTTPBadRequest:
            print("Expected exception")
            self.printFooter('create_volume_badParams')
            return
        except Exception as ex:
            print(ex)
            self.fail("Failed with unexpected exception")

        self.fail('No exception occurred.')

    def test_1_create_volume_duplicate_name(self):
        self.printHeader('create_volume_duplicate_name')

        # add one and check
        try:
            optional = {'comment': 'test volume', 'tpvv': True}
            self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, SIZE, optional)
        except Exception as ex:
            print(ex)
            self.fail("Failed to create volume")

        try:
            self.cl.createVolume(VOLUME_NAME1, CPG_NAME2, SIZE, optional)
        except exceptions.HTTPConflict:
            print("Expected exception")
            self.printFooter('create_volume_duplicate_name')
            return
        except Exception as ex:
            print(ex)
            self.fail("Failed with unexpected exception")
        self.fail('No exception occurred.')

    def test_1_create_volume_tooLarge(self):
        self.printHeader('create_volume_tooLarge')
        try:
            optional = {'id': 3, 'comment': 'test volume', 'tpvv': True}
            self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, 16777218, optional)
        except exceptions.HTTPBadRequest:
            print("Expected exception")
            self.printFooter('create_volume_tooLarge')
            return
        except Exception as ex:
            print(ex)
            self.fail("Failed with unexpected exception")

        self.fail('No exception occurred')

    def test_1_create_volume_duplicate_ID(self):
        self.printHeader('create_volume_duplicate_ID')
        try:
            optional = {'id': 10000, 'comment': 'first volume'}
            self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, SIZE, optional)
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume')

        try:
            optional2 = {'id': 10000, 'comment': 'volume with duplicate ID'}
            self.cl.createVolume(VOLUME_NAME2, CPG_NAME2, SIZE, optional2)
        except exceptions.HTTPConflict:
            print('Expected exception')
            self.printFooter('create_volume_duplicate_ID')
            return
        except Exception as ex:
            print(ex)
            self.fail('Failed with unexpected exception')

        self.fail('No exception occurred')

    def test_1_create_volume_longName(self):
        self.printHeader('create_volume_longName')
        try:
            optional = {'id': 5}
            LongName = ('ThisVolumeNameIsWayTooLongToMakeAnySenseAndIs'
                        'DeliberatelySo')
            self.cl.createVolume(LongName, CPG_NAME1, SIZE, optional)
        except exceptions.HTTPBadRequest:
            print('Expected exception')
            self.printFooter('create_volume_longName')
            return
        except Exception as ex:
            print(ex)
            self.fail('Failed with unexpected exception')

        self.fail('No exception occurred.')

    def test_2_get_volume_bad(self):
        self.printHeader('get_volume_bad')

        try:
            self.cl.getVolume('NoSuchVolume')
        except exceptions.HTTPNotFound:
            print("Expected exception")
            self.printFooter('get_volume_bad')
            return
        except Exception as ex:
            print(ex)
            self.fail("Failed with unexpected exception")

        self.fail("No exception occurred")

    def test_2_get_volumes(self):
        self.printHeader('get_volumes')

        self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, SIZE)
        self.cl.createVolume(VOLUME_NAME2, CPG_NAME1, SIZE)

        vol1 = self.cl.getVolume(VOLUME_NAME1)
        vol2 = self.cl.getVolume(VOLUME_NAME2)

        vols = self.cl.getVolumes()

        self.assertTrue(self.findInDict(vols['members'], 'name', vol1['name']))
        self.assertTrue(self.findInDict(vols['members'], 'name', vol2['name']))

        self.printFooter('get_volumes')

    def test_3_delete_volume_nonExist(self):
        self.printHeader('delete_volume_nonExist')
        try:
            self.cl.deleteVolume(VOLUME_NAME1)
        except exceptions.HTTPNotFound:
            print("Expected exception")
            self.printFooter('delete_volume_nonExist')
            return
        except Exception as ex:
            print(ex)
            self.fail("Failed with unexpected exception")

        self.fail('No exception occurred.')

    def test_3_delete_volumes(self):
        self.printHeader('delete_volumes')

        try:
            optional = {'comment': 'Made by flask.'}
            self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, SIZE, optional)
            self.cl.getVolume(VOLUME_NAME1)
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume')

        try:
            optional = {'comment': 'Made by flask.'}
            self.cl.createVolume(VOLUME_NAME2, CPG_NAME1, SIZE, optional)
            self.cl.getVolume(VOLUME_NAME2)
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume')

        try:
            self.cl.deleteVolume(VOLUME_NAME1)
        except Exception as ex:
            print(ex)
            self.fail('Failed to delete %s' % (VOLUME_NAME1))

        try:
            self.cl.getVolume(VOLUME_NAME1)
        except exceptions.HTTPNotFound:
            print('Expected exception')
        except Exception as ex:
            print(ex)
            self.fail('Failed with unexpected exception')

        try:
            self.cl.deleteVolume(VOLUME_NAME2)
        except Exception as ex:
            print(ex)
            self.fail('Failed to delete %s' % (VOLUME_NAME2))

        try:
            self.cl.getVolume(VOLUME_NAME2)
        except exceptions.HTTPNotFound:
            print('Expected exception')
            self.printFooter('delete_volumes')
            return
        except Exception as ex:
            print(ex)
            self.fail('Failed with unexpected exception')

    def test_4_create_snapshot_no_optional(self):
        self.printHeader('create_snapshot_no_optional')

        try:
            optional = {'snapCPG': CPG_NAME1}
            self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, SIZE, optional)
            # add one
            self.cl.createSnapshot(SNAP_NAME1, VOLUME_NAME1)
            # no API to get and check
        except Exception as ex:
            print(ex)
            self.fail("Failed with unexpected exception")

        self.cl.deleteVolume(SNAP_NAME1)
        self.printFooter('create_snapshot_no_optional')

    def test_4_create_snapshot(self):
        self.printHeader('create_snapshot')

        try:
            optional = {'snapCPG': CPG_NAME1}
            self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, SIZE, optional)
            # add one
            optional = {'expirationHours': 300}
            self.cl.createSnapshot(SNAP_NAME1, VOLUME_NAME1, optional)
            # no API to get and check
        except Exception as ex:
            print(ex)
            self.fail("Failed with unexpected exception")

        self.cl.deleteVolume(SNAP_NAME1)
        self.printFooter('create_snapshot')

    def test_4_create_snapshot_badParams(self):
        self.printHeader('create_snapshot_badParams')
        # add one
        optional = {'snapCPG': CPG_NAME1}
        self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, SIZE, optional)
        try:
            optional = {'Bad': True, 'expirationHours': 300}
            self.cl.createSnapshot(SNAP_NAME1, VOLUME_NAME1, optional)
        except exceptions.HTTPBadRequest:
            print("Expected exception")
            self.printFooter('create_snapshot_badParams')
            return
        except Exception as ex:
            print(ex)
            self.fail("Failed with unexpected exception")

        self.fail("No exception occurred.")

    def test_4_create_snapshot_nonExistVolume(self):
        self.printHeader('create_snapshot_nonExistVolume')

        # add one
        try:
            name = 'UnitTestSnapshot'
            volName = 'NonExistVolume'
            optional = {'id': 1, 'comment': 'test snapshot',
                        'readOnly': True, 'expirationHours': 300}
            self.cl.createSnapshot(name, volName, optional)
        except exceptions.HTTPNotFound:
            print("Expected exception")
            self.printFooter('create_snapshot_nonExistVolume')
            return
        except Exception as ex:
            print(ex)
            self.fail("Failed with unexpected exception")

        self.fail("No exception occurred.")

    def test_5_grow_volume(self):
        self.printHeader('grow_volume')
        try:
            # add one
            optional = {'comment': 'test volume', 'tpvv': True}
            self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, SIZE, optional)
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume')
            return

        try:
            # grow it
            result = self.cl.growVolume(VOLUME_NAME1, 1)
        except Exception as ex:
            print(ex)
            self.fail('Failed to grow volume')
            return

        try:
            result = self.cl.getVolume(VOLUME_NAME1)
            size_after = result['sizeMiB']
            self.assertGreater(size_after, SIZE)
        except Exception as ex:
            print(ex)
            self.fail('Failed to get volume after growth')
            return

        self.printFooter('grow_volume')

    def test_5_grow_volume_bad(self):
        self.printHeader('grow_volume_bad')

        try:
            # add one
            optional = {'comment': 'test volume', 'tpvv': True}
            self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, SIZE, optional)
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume')
            return

        try:
            # shrink it
            self.cl.growVolume(VOLUME_NAME1, -1)
        # 3par is returning 409 instead of 400
        except exceptions.HTTPBadRequest as ex:
            print("Expected exception")
            self.printFooter('grow_volume_bad')
            return
        except exceptions.HTTPConflict as ex:
            print("Expected exception")
            self.printFooter('grow_volume_bad')
            return
        except Exception as ex:
            print(ex)
            self.fail("Failed with unexpected exception")

        self.fail("No exception occurred.")

    def test_6_copy_volume(self):
        self.printHeader('copy_volume')

        # TODO: Add support for ssh/stopPhysical copy in mock mode
        if self.unitTest:
            self.printFooter('copy_volume')
            return

        try:
            # add one
            optional = {'comment': 'test volume', 'tpvv': True,
                        'snapCPG': CPG_NAME1}
            self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, SIZE, optional)
        except Exception as ex:
            print ex
            self.fail('Failed to create volume')
            return

        try:
            # copy it
            optional = {'online': True}
            self.cl.copyVolume(VOLUME_NAME1, VOLUME_NAME2, CPG_NAME1, optional)
        except Exception as ex:
            print ex
            self.fail('Failed to copy volume')
            return

        try:
            self.cl.getVolume(VOLUME_NAME2)
        except Exception as ex:
            print ex
            self.fail('Failed to get cloned volume')
            return

        try:
            self.cl.stopOnlinePhysicalCopy(VOLUME_NAME2)
        except Exception as ex:
            print ex
            self.fail('Failed to stop physical copy. ' +
                      'This may negatively impact other tests and require'
                      ' manual cleanup!')
            return

        try:
            self.cl.getVolume(VOLUME_NAME2)
            self.fail("Expecting exception, but found 'deleted' volume")
        except exceptions.HTTPNotFound as ex:
            self.printFooter('copy_volume')
            return
        except Exception as ex:
            print ex
            self.fail('Unexpected exception')

        self.fail('Expecting HTTPNotFound exception')

    def test_7_create_volume_set(self):
        self.printHeader('create_volume_set')
        try:
            self.cl.createVolumeSet(VOLUME_SET_NAME1, domain=self.DOMAIN,
                                    comment="Unit test volume set 1")
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume set')
            return

        try:
            resp = self.cl.getVolumeSet(VOLUME_SET_NAME1)
            print(resp)
        except Exception as ex:
            print(ex)
            self.fail('Failed to get volume set')
            return

        self.printFooter('create_volume_set')

    def test_7_create_volume_set_with_volumes(self):
        self.printHeader('create_volume_set')
        try:
            optional = {'comment': 'test volume 1', 'tpvv': True}
            self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, SIZE, optional)
            optional = {'comment': 'test volume 2', 'tpvv': True}
            self.cl.createVolume(VOLUME_NAME2, CPG_NAME1, SIZE, optional)
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volumes')
            return

        try:
            members = [VOLUME_NAME1, VOLUME_NAME2]
            self.cl.createVolumeSet(VOLUME_SET_NAME1, domain=self.DOMAIN,
                                    comment="Unit test volume set 1",
                                    setmembers=members)

        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume set with members')

        try:
            resp = self.cl.getVolumeSet(VOLUME_SET_NAME1)
            self.assertIsNotNone(resp)
            resp_members = resp['setmembers']
            self.assertIn(VOLUME_NAME1, resp_members)
            self.assertIn(VOLUME_NAME2, resp_members)
        except Exception as ex:
            print(ex)
            self.fail('Failed to get volume set')
            return

        self.printFooter('create_volume_set')

    def test_7_create_volume_set_dup(self):
        self.printHeader('create_volume_set_dup')

        try:
            self.cl.createVolumeSet(VOLUME_SET_NAME1, domain=self.DOMAIN,
                                    comment="Unit test volume set 1")
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume set')
            return

        try:
            # create it again
            self.cl.createVolumeSet(VOLUME_SET_NAME1, domain=self.DOMAIN,
                                    comment="Unit test volume set 1")
        except exceptions.HTTPConflict as ex:
            print("expected exception")
            self.printFooter('create_volume_set_dup')
            return
        except Exception as ex:
            print(ex)
            self.fail("Failed with unexpected exception")

        self.fail("No exception occured")

    def test_8_get_volume_sets(self):
        self.printHeader('get_volume_sets')

        try:
            self.cl.createVolumeSet(VOLUME_SET_NAME1, domain=self.DOMAIN,
                                    comment="Unit test volume set 1")
            self.cl.createVolumeSet(VOLUME_SET_NAME2, domain=self.DOMAIN)
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume set')
            return

        try:
            sets = self.cl.getVolumeSets()
            self.assertIsNotNone(sets)
            set_names = [vset['name'] for vset in sets['members']]

            self.assertIn(VOLUME_SET_NAME1, set_names)
            self.assertIn(VOLUME_SET_NAME2, set_names)

        except Exception as ex:
            print(ex)
            self.fail('Failed to get volume sets')
            return

        self.printFooter('get_volume_sets')

    def test_9_del_volume_set_empty(self):
        self.printHeader('del_volume_set_empty')
        try:
            self.cl.createVolumeSet(VOLUME_SET_NAME2, domain=self.DOMAIN)
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume set')
            return

        try:
            self.cl.deleteVolumeSet(VOLUME_SET_NAME2)
        except Exception as ex:
            print(ex)
            self.fail('Failed to delete volume set')
            return

        self.printFooter('del_volume_set_empty')

    def test_9_del_volume_set_with_volumes(self):
        self.printHeader('delete_volume_set_with_volumes')
        try:
            optional = {'comment': 'test volume 1', 'tpvv': True}
            self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, SIZE, optional)
            optional = {'comment': 'test volume 2', 'tpvv': True}
            self.cl.createVolume(VOLUME_NAME2, CPG_NAME1, SIZE, optional)
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volumes')
            return

        try:
            members = [VOLUME_NAME1, VOLUME_NAME2]
            self.cl.createVolumeSet(VOLUME_SET_NAME1, domain=self.DOMAIN,
                                    comment="Unit test volume set 1",
                                    setmembers=members)

        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume set with members')

        try:
            self.cl.deleteVolumeSet(VOLUME_SET_NAME1)
        except Exception as ex:
            print(ex)
            self.fail('Failed to delete volume set')
            return

        self.printFooter('delete_volume_set_with_volumes')

    def test_10_modify_volume_set_change_name(self):
        self.printHeader('modify_volume_set_change_name')
        try:
            self.cl.createVolumeSet(VOLUME_SET_NAME1, domain=self.DOMAIN,
                                    comment="First")
            self.cl.modifyVolumeSet(VOLUME_SET_NAME1,
                                    newName=VOLUME_SET_NAME2)
            vset = self.cl.getVolumeSet(VOLUME_SET_NAME2)
            self.assertEqual("First", vset['comment'])
        except Exception as ex:
            print(ex)
            self.fail('Failed to create or change name of volume set')

        self.printFooter('modify_volume_set_change_name')

    def test_10_modify_volume_set_change_comment(self):
        self.printHeader('modify_volume_set_change_comment')
        try:
            self.cl.createVolumeSet(VOLUME_SET_NAME1, domain=self.DOMAIN,
                                    comment="First")
            self.cl.modifyVolumeSet(VOLUME_SET_NAME1,
                                    comment="Second")
            vset = self.cl.getVolumeSet(VOLUME_SET_NAME1)
            self.assertEqual("Second", vset['comment'])
        except Exception as ex:
            print(ex)
            self.fail('Failed to create or change comment of volume set')

        self.printFooter('modify_volume_set_change_comment')
        pass

    def test_10_modify_volume_set_add_members_to_empty(self):
        self.printHeader('modify_volume_set_add_members_to_empty')

        try:
            optional = {'comment': 'test volume 1', 'tpvv': True}
            self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, SIZE, optional)
            optional = {'comment': 'test volume 2', 'tpvv': True}
            self.cl.createVolume(VOLUME_NAME2, CPG_NAME1, SIZE, optional)
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume set')
        try:
            self.cl.createVolumeSet(VOLUME_SET_NAME1, domain=self.DOMAIN,
                                    comment="Unit test volume set 1")
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume set')
            return

        try:
            members = [VOLUME_NAME1, VOLUME_NAME2]
            self.cl.modifyVolumeSet(VOLUME_SET_NAME1, self.cl.SET_MEM_ADD,
                                    setmembers=members)
        except Exception as ex:
            print(ex)
            self.fail('Failed to add volumes')
            return

        try:
            resp = self.cl.getVolumeSet(VOLUME_SET_NAME1)
            print(resp)
            self.assertTrue(VOLUME_NAME1 in resp['setmembers'])
            self.assertTrue(VOLUME_NAME2 in resp['setmembers'])
        except Exception as ex:
            print(ex)
            self.fail('Failed to add volumes to volume set')
            return

        self.printFooter('modify_volume_set_add_members_to_empty')

    def test_10_modify_volume_set_add_members(self):
        self.printHeader('modify_volume_set_add_members')

        try:
            optional = {'comment': 'test volume 1', 'tpvv': True}
            self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, SIZE, optional)
            optional = {'comment': 'test volume 2', 'tpvv': True}
            self.cl.createVolume(VOLUME_NAME2, CPG_NAME1, SIZE, optional)
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume set')
        try:
            members = [VOLUME_NAME1]
            self.cl.createVolumeSet(VOLUME_SET_NAME1, domain=self.DOMAIN,
                                    setmembers=members,
                                    comment="Unit test volume set 1")
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume set')
            return

        try:
            members = [VOLUME_NAME2]
            self.cl.modifyVolumeSet(VOLUME_SET_NAME1, self.cl.SET_MEM_ADD,
                                    setmembers=members)
        except Exception as ex:
            print(ex)
            self.fail('Failed to add volumes')
            return

        try:
            resp = self.cl.getVolumeSet(VOLUME_SET_NAME1)
            print(resp)
            self.assertTrue(VOLUME_NAME1 in resp['setmembers'])
            self.assertTrue(VOLUME_NAME2 in resp['setmembers'])
        except Exception as ex:
            print(ex)
            self.fail('Failed to add volumes to volume set')
            return

        self.printFooter('modify_volume_set_add_members')

    def test_10_modify_volume_set_del_members(self):
        self.printHeader('modify_volume_del_members')

        try:
            optional = {'comment': 'test volume 1', 'tpvv': True}
            self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, SIZE, optional)
            optional = {'comment': 'test volume 2', 'tpvv': True}
            self.cl.createVolume(VOLUME_NAME2, CPG_NAME1, SIZE, optional)
            members = [VOLUME_NAME1, VOLUME_NAME2]
            self.cl.createVolumeSet(VOLUME_SET_NAME1, domain=self.DOMAIN,
                                    comment="Unit test volume set 1",
                                    setmembers=members)
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume set')
            return

        try:

            members = [VOLUME_NAME1]
            self.cl.modifyVolumeSet(VOLUME_SET_NAME1,
                                    action=self.cl.SET_MEM_REMOVE,
                                    setmembers=members)
        except Exception as ex:
            print(ex)
            self.fail('Failed to remove volumes from set')
            return

        try:
            resp = self.cl.getVolumeSet(VOLUME_SET_NAME1)
            self.assertIsNotNone(resp)
            resp_members = resp['setmembers']
            self.assertNotIn(VOLUME_NAME1, resp_members)
            self.assertIn(VOLUME_NAME2, resp_members)
        except Exception as ex:
            print(ex)
            self.fail('Failed to get volume set')
            return

        self.printFooter('modify_volume_del_members')

    def _create_vv_sets(self):
        optional = {'comment': 'test volume 1', 'tpvv': True}
        self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, SIZE, optional)
        optional = {'comment': 'test volume 2', 'tpvv': True}
        self.cl.createVolume(VOLUME_NAME2, CPG_NAME1, SIZE, optional)
        members = [VOLUME_NAME1, VOLUME_NAME2]
        self.cl.createVolumeSet(VOLUME_SET_NAME1, domain=self.DOMAIN,
                                comment="Unit test volume set 1",
                                setmembers=members)

    def test_11_add_qos(self):
        self.printHeader('add_qos')

        self._create_vv_sets()
        qos = {'bwMinGoalKB': 1024,
               'bwMaxLimitKB': 1024}
        try:
            self.cl.createQoSRules(VOLUME_SET_NAME1, qos)
        except Exception as ex:
            print(ex)
            self.fail('Failed to add qos')
            return

        try:
            rule = self.cl.queryQoSRule(VOLUME_SET_NAME1)
        except Exception as ex:
            print(ex)
            self.fail('Failed to query qos')

        self.assertIsNotNone(rule)
        self.assertEquals(rule['bwMinGoalKB'], qos['bwMinGoalKB'])
        self.assertEquals(rule['bwMaxLimitKB'], qos['bwMaxLimitKB'])
        self.printFooter('add_qos')

    def test_12_modify_qos(self):
        self.printHeader('modify_qos')

        self._create_vv_sets()
        qos_before = {'bwMinGoalKB': 1024,
                      'bwMaxLimitKB': 1024}
        qos_after = {'bwMinGoalKB': 1024,
                     'bwMaxLimitKB': 2048}

        try:
            self.cl.createQoSRules(VOLUME_SET_NAME1, qos_before)
            self.cl.modifyQoSRules(VOLUME_SET_NAME1, qos_after)
        except Exception as ex:
            print(ex)
            self.fail('Failed to modify qos')
            return

        try:
            rule = self.cl.queryQoSRule(VOLUME_SET_NAME1)
        except Exception as ex:
            print(ex)
            self.fail('Failed to query qos')

        self.assertIsNotNone(rule)
        self.assertEquals(rule['bwMinGoalKB'], qos_after['bwMinGoalKB'])
        self.assertEquals(rule['bwMaxLimitKB'], qos_after['bwMaxLimitKB'])
        self.printFooter('modify_qos')

    def test_13_delete_qos(self):
        self.printHeader('delete_qos')

        self._create_vv_sets()
        self.cl.createVolumeSet(VOLUME_SET_NAME2)

        qos1 = {'bwMinGoalKB': 1024,
                'bwMaxLimitKB': 1024}
        qos2 = {'bwMinGoalKB': 512,
                'bwMaxLimitKB': 2048}
        try:
            self.cl.createQoSRules(VOLUME_SET_NAME1, qos1)
            self.cl.createQoSRules(VOLUME_SET_NAME2, qos2)
            all_qos = self.cl.queryQoSRules()
            self.assertGreaterEqual(all_qos['total'], 2)
            self.assertIn(VOLUME_SET_NAME1,
                          [qos['name'] for qos in all_qos['members']])
            self.assertIn(VOLUME_SET_NAME2,
                          [qos['name'] for qos in all_qos['members']])
        except Exception as ex:
            print(ex)
            self.fail('Failed to create/query qos')
            return

        try:
            self.cl.deleteQoSRules(VOLUME_SET_NAME1)
            all_qos = self.cl.queryQoSRules()
        except Exception as ex:
            print(ex)
            self.fail("Failed to delete/query qos")
            return

        self.assertIsNotNone(all_qos)
        self.assertNotIn(VOLUME_SET_NAME1,
                         [qos['name'] for qos in all_qos['members']])
        self.assertIn(VOLUME_SET_NAME2,
                      [qos['name'] for qos in all_qos['members']])
        self.printFooter('delete_qos')

    def test_14_modify_volume_rename(self):
        self.printHeader('modify volume')
        try:
            # add one
            optional = {'comment': 'test volume', 'tpvv': True}
            self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, SIZE, optional)
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume')
            return

        try:
            volumeMod = {'newName': VOLUME_NAME2}
            self.cl.modifyVolume(VOLUME_NAME1, volumeMod)
            vol2 = self.cl.getVolume(VOLUME_NAME2)
            self.assertIsNotNone(vol2)
            self.assertEqual(vol2['comment'], optional['comment'])
        except Exception as ex:
            print(ex)
            self.fail('Failed to modify volume')
            return

        self.printFooter('modify volume')

    def test_15_set_volume_metadata(self):
        self.printHeader('set volume metadata')

        optional = {'comment': 'test volume', 'tpvv': True}
        expected_value = 'test_val'
        self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, 1024, optional)
        self.cl.setVolumeMetaData(VOLUME_NAME1, 'test_key', expected_value)
        result = self.cl.getVolumeMetaData(VOLUME_NAME1, 'test_key')
        self.assertEqual(result['value'], expected_value)

        self.printFooter('set volume metadata')

    def test_15_set_bad_volume_metadata(self):
        self.printHeader('set bad volume metadata')

        self.assertRaises(exceptions.HTTPNotFound,
                          self.cl.setVolumeMetaData,
                          'Fake_Volume',
                          'test_key',
                          'test_val')

        self.printFooter('set bad volume metadata')

    def test_15_set_volume_metadata_existing_key(self):
        self.printHeader('set volume metadata existing key')

        optional = {'comment': 'test volume', 'tpvv': True}
        expected = 'new_test_val'
        self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, 1024, optional)
        self.cl.setVolumeMetaData(VOLUME_NAME1, 'test_key', 'test_val')
        self.cl.setVolumeMetaData(VOLUME_NAME1, 'test_key', 'new_test_val')
        contents = self.cl.getVolumeMetaData(VOLUME_NAME1, 'test_key')
        self.assertEqual(contents['value'], expected)

        self.printFooter('set volume metadata existing key')

    def test_15_set_volume_metadata_invalid_length(self):
        self.printHeader('set volume metadata invalid length')

        optional = {'comment': 'test volume', 'tpvv': True}
        self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, 1024, optional)
        self.assertRaises(exceptions.HTTPBadRequest,
                          self.cl.setVolumeMetaData,
                          VOLUME_NAME1,
                          'this_key_will_cause_an_exception',
                          'test_val')

        self.printFooter('set volume metadata invalid length')

    def test_15_set_volume_metadata_invalid_data(self):
        self.printHeader('set volume metadata invalid data')

        optional = {'comment': 'test volume', 'tpvv': True}
        self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, 1024, optional)
        self.assertRaises(exceptions.HTTPBadRequest,
                          self.cl.setVolumeMetaData,
                          VOLUME_NAME1,
                          None,
                          'test_val')

        self.printFooter('set volume metadata invalid data')

    def test_16_get_volume_metadata(self):
        self.printHeader('get volume metadata')

        optional = {'comment': 'test volume', 'tpvv': True}
        expected_value = 'test_val'
        self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, 1024, optional)
        self.cl.setVolumeMetaData(VOLUME_NAME1, 'test_key', expected_value)
        result = self.cl.getVolumeMetaData(VOLUME_NAME1, 'test_key')
        self.assertEqual(expected_value, result['value'])

        self.printFooter('get volume metadata')

    def test_16_get_volume_metadata_missing_volume(self):
        self.printHeader('get volume metadata missing volume')

        self.assertRaises(exceptions.HTTPNotFound,
                          self.cl.getVolumeMetaData,
                          'Fake_Volume',
                          'bad_key')

        self.printFooter('get volume metadata missing volume')

    def test_16_get_volume_metadata_missing_key(self):
        self.printHeader('get volume metadata missing key')

        optional = {'comment': 'test volume', 'tpvv': True}
        self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, 1024, optional)
        self.assertRaises(exceptions.HTTPNotFound,
                          self.cl.getVolumeMetaData,
                          VOLUME_NAME1,
                          'bad_key')

        self.printFooter('get volume metadata missing key')

    def test_16_get_volume_metadata_invalid_input(self):
        self.printHeader('get volume metadata invalid input')

        optional = {'comment': 'test volume', 'tpvv': True}
        self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, 1024, optional)
        self.assertRaises(exceptions.HTTPBadRequest,
                          self.cl.getVolumeMetaData,
                          VOLUME_NAME1,
                          '&')

        self.printFooter('get volume metadata invalid input')

    def test_17_get_all_volume_metadata(self):
        self.printHeader('get all volume metadata')

        # Keys present in metadata
        optional = {'comment': 'test volume', 'tpvv': True}
        expected_value_1 = 'test_val'
        expected_value_2 = 'test_val2'
        self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, 1024, optional)
        self.cl.setVolumeMetaData(VOLUME_NAME1,
                                  'test_key_1',
                                  expected_value_1)
        self.cl.setVolumeMetaData(VOLUME_NAME1,
                                  'test_key_2',
                                  expected_value_2)
        result = self.cl.getAllVolumeMetaData(VOLUME_NAME1)
        self.assertEqual(expected_value_1, result['members'][0]['value'])
        self.assertEqual(expected_value_2, result['members'][1]['value'])

        # No keys present in metadata
        optional = {'comment': 'test volume', 'tpvv': True}
        expected_value = {'total': 0, 'members': []}
        self.cl.createVolume(VOLUME_NAME2, CPG_NAME1, 1024, optional)
        result = self.cl.getAllVolumeMetaData(VOLUME_NAME2)
        self.assertEqual(expected_value, result)

        self.printFooter('get all volume metadata')

    def test_17_get_all_volume_metadata_missing_volume(self):
        self.printHeader('get all volume metadata missing volume')

        self.assertRaises(exceptions.HTTPNotFound,
                          self.cl.getAllVolumeMetaData,
                          'Fake_Volume')

        self.printFooter('get all volume metadata missing volume')

    def test_18_remove_volume_metadata(self):
        self.printHeader('remove volume metadata')

        optional = {'comment': 'test volume', 'tpvv': True}
        self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, 1024, optional)
        self.cl.setVolumeMetaData(VOLUME_NAME1, 'test_key', 'test_val')
        self.cl.removeVolumeMetaData(VOLUME_NAME1, 'test_key')
        self.assertRaises(exceptions.HTTPNotFound,
                          self.cl.getVolumeMetaData,
                          VOLUME_NAME1,
                          'test_key')

        self.printFooter('remove volume metadata')

    def test_18_remove_volume_metadata_missing_volume(self):
        self.printHeader('remove volume metadata missing volume')

        self.assertRaises(exceptions.HTTPNotFound,
                          self.cl.removeVolumeMetaData,
                          'Fake_Volume',
                          'test_key')

        self.printFooter('remove volume metadata missing volume')

    def test_18_remove_volume_metadata_missing_key(self):
        self.printHeader('remove volume metadata missing key')

        optional = {'comment': 'test volume', 'tpvv': True}
        self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, 1024, optional)
        self.assertRaises(exceptions.HTTPNotFound,
                          self.cl.removeVolumeMetaData,
                          VOLUME_NAME1,
                          'test_key')

        self.printFooter('remove volume metadata missing key')

    def test_18_remove_volume_metadata_invalid_input(self):
        self.printHeader('remove volume metadata invalid input')

        optional = {'comment': 'test volume', 'tpvv': True}
        self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, 1024, optional)
        self.assertRaises(exceptions.HTTPBadRequest,
                          self.cl.removeVolumeMetaData,
                          VOLUME_NAME1,
                          '&')

        self.printFooter('remove volume metadata invalid input')

    def test_19_find_volume_metadata(self):
        self.printHeader('find volume metadata')

        # Volume should be found
        optional = {'comment': 'test volume', 'tpvv': True}
        expected = True
        self.cl.createVolume(VOLUME_NAME1, CPG_NAME1, 1024, optional)
        self.cl.setVolumeMetaData(VOLUME_NAME1, 'test_key', 'test_val')
        result = self.cl.findVolumeMetaData(VOLUME_NAME1,
                                            'test_key',
                                            'test_val')
        self.assertEqual(result, expected)

        # Volume should not be found
        optional = {'comment': 'test volume', 'tpvv': True}
        expected = False
        result = self.cl.findVolumeMetaData(VOLUME_NAME1,
                                            'bad_key',
                                            'test_val')
        self.assertEqual(result, expected)

        self.printFooter('find volume metadata')

    def test_19_find_volume_metadata_missing_volume(self):
        self.printHeader('find volume metadata missing volume')

        expected = False
        result = self.cl.findVolumeMetaData('Fake_Volume',
                                            'test_key',
                                            'test_val')
        self.assertEqual(result, expected)

        self.printFooter('find volume metadata missing volume')

# testing
# suite = unittest.TestLoader().
#   loadTestsFromTestCase(HP3ParClientVolumeTestCase)
# unittest.TextTestRunner(verbosity=2).run(suite)
