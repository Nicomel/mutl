import abc
import pickle

from ..config import mutl_config as config
from ..models.task import TasksListsRepo  

class TLRFile(object):
    """
    This class is used to load and persist a tasks list repository (TLR)
    """
    def __init__(self):
        self.filepath = config.mutl_file_path

    def load(self) -> TasksListsRepo:
        with open(self.filepath, 'rb') as mutl_file:
            tlr = pickle.load(mutl_file)
        mutl_file.close()
        return tlr

    def persist(self, tlr: TasksListsRepo) -> bool:
        with open(self.filepath, 'wb') as mutl_file:
            tlr = pickle.dump(mutl_file)
        mutl_file.close()
        return True