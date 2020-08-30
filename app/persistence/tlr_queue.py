import abc
import os
import pickle
from typing import OrderedDict
from uuid import UUID
from ..models.datachange import DataChangesList

class TLRQueue(object):
    """
    This class is used to push and persist a changes list events
    """
    def __init__(self, mutl_queue_path):
        self.filepath = mutl_queue_path
        self.queue = OrderedDict[UUID, DataChangesList]()
        #TODO add try/raise
        if os.path.isfile(self.filepath):
            with open(self.filepath, 'rb') as mutl_queue:
                self.queue = pickle.load(mutl_queue)
            mutl_queue.close()

    def push(self, changesList: DataChangesList) -> bool:
        self.queue[changesList.uuid] = changesList
        self.persist()
        return True

    def removeItemIfexist(self, uuid: UUID) -> bool:
        if uuid in self.queue:
            self.queue.pop(uuid)
            self.persist()
            return True
        return False

    def pop(self, doPersist: bool = True) -> DataChangesList:
        changesList = self.queue.popitem(last=False)
        if doPersist:
            self.persist()
        return changesList[1]

    def isNotEmpty(self) -> bool:
        if len(self.queue) > 0:
            return True
        else:
            return False

    def persist(self) -> bool:
        #TODO add try/raise
        with open(self.filepath, 'ab') as mutl_queue:
            pickle.dump(self.queue, mutl_queue)
        mutl_queue.close()
        return True