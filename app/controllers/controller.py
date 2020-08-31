from typing import Deque

import logging

from ..config import mutl_config as config
from ..models.task import Task, TasksList, TasksListsRepo
from ..models.datachange import *
from ..models.user import User
from ..persistence.tlr_file import TLRFile
from ..persistence.tlr_queue import TLRQueue
from ..cache.tlr_cache import TLRCache

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging._nameToLevel[config.mutl_log_level])
logger = logging.getLogger(__name__)

tlrFile = TLRFile()
tlrLocalQueue = TLRQueue(config.mutl_local_queue_path)
tlrServerQueue = TLRQueue(config.mutl_server_queue_path)
tlrCache = TLRCache(tlrFile)

def getLocalRepoVersion():
    return tlrCache.getCachedRepoVersion()

def getCachedTlr() -> TasksListsRepo:
    return tlrCache.tlr

def pushChanges(changesList: DataChangesList) -> bool:
    """
    This function is used to push event / data change into a local buffer
    and to the server when online. 
    Cache is updated with the change once received from the server when online
    """
    if config.mutl_online_default_status:
        #TODO: implement online functions to push change logs to server
        # Call server
        logger.info("Call MUTL server API")
    else:
        # Publish changes log on local queue/buffer
        tlrLocalQueue.push(changesList)
        # Apply changes log on cache (not persisted)
        tlrCache.update(changesList)
    return True

def consumeServerChanges(changesList: DataChangesList) -> bool:
    """
    This function is used to consume event / data change from the server
    Remote change from server are applied if we are online and if there is no remaining local change logs in the local queue
    It triggers a cache refresh if needed and persist the new version
    """
    # Push server changeslist into server queue
    tlrServerQueue.push(changesList)
    
    # Local buffered changeslist are removed from the local queue once received from the server
    tlrLocalQueue.removeItemIfexist(changesList.uuid)

    return True

def synchronize_changes():
    # We do not integrate server changeslist as long as local changeslist have not been committed on server side
    if tlrLocalQueue.isNotEmpty():
        # Push local changeslist buffered to the server
        for uuid, localChangesList in tlrLocalQueue.queue.items():
            #TODO add try/raise
            #TODO Call server API
            logger.info("Push local changes to server")
            # localChangesList
        return True

    # Integrate changeslist from server
    while tlrServerQueue.queue:
        serverChangesList = tlrServerQueue.pop()
        # For changes from server, check if the repo version in the changes list matches the current version of the repo, otherwise refresh
        if changesList.fromRepoVersion != tlrCache.tlr.version:
            # Get last version from the server
            #TODO: Call server API
            logger.info("Refresh local TL repo from MUTL server API")
            # tlrCache.refresh(serverTlr)
        # When repo up to date, update
        tlrCache.update(changesList, doPersist=True)
    
    return True