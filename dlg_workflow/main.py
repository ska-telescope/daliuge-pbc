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
import time

import ska_sdp_config
from dlg_workflow import common


DLG_DIM_HOST = os.environ.get('DLG_DIM_HOST', '127.0.0.1')
DLG_DIM_PORT = int(os.environ.get('DLG_DIM_PORT', 8001))

logger = logging.getLogger(__name__)

def get_pb(config):
    workflow = {
        'id': 'testdlg',
        'version': '0.0.1',
        'type': 'dlg-realtime'
    }
    logger.info("Waiting for processing block...")
    for txn in config.txn():
        pb = txn.take_processing_block_by_workflow(
                workflow, config.client_lease)
        if pb is not None:
            continue
        txn.loop(wait=True)
    logger.info("Claimed processing block %s", pb)
    return pb


def create_deployment(config, pb):
    logger.info("Deploying DALiuGE...")
    deploy_id = pb.pb_id + "-dlg"
    deployment = ska_sdp_config.Deployment(
        deploy_id, "helm", {
            'chart': 'daliuge',
        })
    for txn in config.txn():
        txn.create_deployment(deployment)
    return deployment


def idle_for_some_obscure_reason(config, pb):
    logger.info("Done, now idling...")
    for txn in config.txn():
        if not txn.is_processing_block_owner(pb.pb_id):
            break
        txn.loop(True)


def cleanup(config, deployment):
    for txn in config.txn():
        txn.delete_deployment(deployment)
    config.close()


def main():
    logging.basicConfig(level=logging.INFO)
    config = ska_sdp_config.Config()
    pb = get_pb(config)
    deployment = create_deployment(config, pb)
    try:
        logger.info("Contacting DIM at %s", DLG_DIM_HOST)
        tries = 1
        max_tries = 200
        for _ in range(max_tries):
            try:
                common.run_processing_block(pb, lambda _: None,
                        host=DLG_DIM_HOST, port=DLG_DIM_PORT)
                break
            except:
                logger.exception("Error while running, trying again (%d/%d)",
                        tries, max_tries)
                tries += 1
                time.sleep(1)
        idle_for_some_obscure_reason(config, pb)
    finally:
        cleanup(config, deployment)

if __name__ == '__main__':
    main()
