#
#    ICRAR - International Centre for Radio Astronomy Research
#    (c) UWA - The University of Western Australia, 2019
#    Copyright by UWA (in the framework of the ICRAR)
#    All rights reserved
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston,
#    MA 02111-1307  USA
#
import unittest

from dlg import testutils
import dlg_workflow


class ProcessingBlock(object):
    pass


class SimpleTest(unittest.TestCase, testutils.ManagerStarter):
    def test_run_processing_block(self):

        processing_block = ProcessingBlock()
        processing_block.pb_id = 'abc'
        processing_block.workflow = {
            'id': 'workflow_id',
            'version': '0.1',
        }
        processing_block.parameters = {}

        statuses = []

        def callback(status):
            statuses.append(status)

        with self.start_nm_in_thread(), self.start_dim_in_thread():
            dlg_workflow.run_processing_block(processing_block, callback, zero_cost_run=True)
        self.assertListEqual(['preparing', 'running', 'finished'], statuses)
