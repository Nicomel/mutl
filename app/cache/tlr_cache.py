from ..models.task import Task, TasksList, TasksListsRepo, TaskStatus
from ..persistence.tlr_file import TLRFile

class TLRCache(object):
    def __init__(self, tlrFile: TLRFile):
        self.tlr = tlrFile.load()

