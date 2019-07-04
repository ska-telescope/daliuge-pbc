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
import logging
import os

from celery import Celery
from sip_config_db.scheduling.processing_block import ProcessingBlock
from sip_config_db.scheduling.processing_block_list import ProcessingBlockList
from sip_config_db import __version__ as config_db_version
from sip_logging.sip_logging import init_logger

from . import __version__
from dlg_pbc import common


logger = logging.getLogger(__name__)

DIM_HOST = os.getenv('DIM_HOST', 'dim')
BROKER = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/1')
BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/2')
APP = Celery(broker=BROKER, backend=BACKEND)


@APP.task
def version():
    return __version__


@APP.task
def execute_processing_block(pb_id, log_level='DEBUG'):
    """Execute the given processing block under DALiuGE"""

    init_logger(__name__, show_log_origin=True, propagate=False,
                log_level=log_level)
    logger.info('+' * 40)
    logger.info('+ Executing Processing block: %s!', pb_id)
    logger.info('+' * 40)
    logger.info('Processing Block Controller version: %s', __version__)
    logger.info('Configuration database API version: %s', config_db_version)

    pb = ProcessingBlock(pb_id)

    logger.info('Starting workflow %s %s', pb.workflow_id, pb.workflow_version)

    pb.set_status('running')
    common.run_processing_block(pb, pb.set_status, host=DIM_HOST, zero_cost_run=True)

    pb_list = ProcessingBlockList()
    pb_list.set_complete(pb_id)
    pb.set_status('completed')
    logger.info('-' * 40)
    logger.info('- Destroying PBC for %s', pb_id)
    logger.info('-' * 40)
    return pb.status
