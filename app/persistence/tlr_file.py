import abc
import os
import pickle
import uuid
from ..config import mutl_config as config
from ..models.task import TasksListsRepo  

class TLRFile(object):
    """
    This class is used to load and persist a tasks list repository (TLR)
    """
    def __init__(self):
        self.filepath = config.mutl_file_path

    def load(self) -> TasksListsRepo:
        if os.path.isfile(self.filepath):
            #TODO add try/raise
            with open(self.filepath, 'rb') as mutl_file:
                tlr = pickle.load(mutl_file)
            mutl_file.close()
            return tlr
        else:
            return TasksListsRepo(
                uuid=uuid.uuid1(),
                version=0
                )

    def persist(self, tlr: TasksListsRepo) -> bool:
        #TODO add try/raise
        with open(self.filepath, 'ab') as mutl_file:
            pickle.dump(tlr, mutl_file)
        mutl_file.close()
        return True