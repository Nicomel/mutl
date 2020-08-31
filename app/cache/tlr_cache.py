import logging
import pickle
from uuid import UUID
from typing import OrderedDict
from ..config import mutl_config as config
from ..models.task import Task, TasksList, TasksListsRepo, TaskStatus
from ..models.datachange import *
from ..persistence.tlr_file import TLRFile

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging._nameToLevel[config.mutl_log_level])
logger = logging.getLogger(__name__)

class TLRCache(object):
    def __init__(self, tlrFile: TLRFile):
        self.tlr = tlrFile.load()
        self.tlrFile = tlrFile

    def update(self, changesList: DataChangesList, doPersist: bool = False) -> bool:
        """
        This class is used to update the cache when a change is received from local/server
        """
        for changeLog in changesList.changeLogsList:
            if changeLog.operation == Operation.CREATE:
                item = pickle.loads(changeLog.serializedObject)
                if changeLog.objectType == ObjectType.TASKSLIST:
                    self.tlr.tasksListsDict[item.uuid] = item
                elif changeLog.objectType == ObjectType.TASK:
                    self.insertTask_atPos(item.tluuid, item, item.pos)
                else:
                    logger.error("Wrong object type used for creation")
                    return False

            elif changeLog.operation == Operation.UPDATE:
                if changeLog.objectType == ObjectType.TASKSLIST:
                    if ((changeLog.fieldName == "title") 
                    and (changeLog.tluuid in self.tlr.tasksListsDict)):
                        setattr(self.tlr.tasksListsDict[changeLog.tluuid], changeLog.fieldName, changeLog.fieldChange)
                    else:
                        logger.error("Wrong field name or uuid used for update")

                elif changeLog.objectType == ObjectType.TASK:
                    if (((changeLog.fieldName == "title") or (changeLog.fieldName == "description")) 
                    and (changeLog.tluuid in self.tlr.tasksListsDict) 
                    and (changeLog.tuuid in self.tlr.tasksListsDict[changeLog.tluuid].tasks)):
                        setattr(self.tlr.tasksListsDict[changeLog.tluuid].tasks[changeLog.tuuid], changeLog.fieldName, changeLog.fieldChange)
                    elif (changeLog.fieldName == "priority"):
                        self.moveTask_atPos(changeLog.tluuid, changeLog.tuuid, int(changeLog.fieldChange))
                    else:
                        logger.error("Wrong field name or uuid used for update")
                else:
                    logger.error("Wrong object type used for creation")
                    return False

            elif changeLog.operation == Operation.PATCH:
                if changeLog.objectType == ObjectType.TASKSLIST:
                    if ((changeLog.fieldName == "title") 
                    and (changeLog.tluuid in self.tlr.tasksListsDict)):
                        current = getattr(self.tlr.tasksListsDict[changeLog.tluuid], changeLog.fieldName)
                        setattr(
                            self.tlr.tasksListsDict[changeLog.tluuid], 
                            changeLog.fieldName, 
                            current + changeLog.fieldChange
                            )
                    else:
                        logger.error("Wrong field name or uuid used for update")

                elif changeLog.objectType == ObjectType.TASK:
                    if (((changeLog.fieldName == "title") or (changeLog.fieldName == "description")) 
                    and (changeLog.tluuid in self.tlr.tasksListsDict) 
                    and (changeLog.tuuid in self.tlr.tasksListsDict[changeLog.tluuid].tasks)):
                        current = getattr(self.tlr.tasksListsDict[changeLog.tluuid].tasks[changeLog.tuuid], changeLog.fieldName)
                        setattr(
                            self.tlr.tasksListsDict[changeLog.tluuid].tasks[changeLog.tuuid], 
                            changeLog.fieldName, 
                            current + changeLog.fieldChange)
                    else:
                        logger.error("Wrong field name or uuid used for update")
                else:
                    logger.error("Wrong object type used for creation")
                    return False

            elif changeLog.operation == Operation.DELETE:
                if changeLog.objectType == ObjectType.TASKSLIST:
                    if (changeLog.tluuid in self.tlr.tasksListsDict):
                        del self.tlr.tasksListsDict[changeLog.tluuid]
                    else:
                        logger.error("Wrong uuid used for deletion")

                elif changeLog.objectType == ObjectType.TASK:
                    if ((changeLog.tluuid in self.tlr.tasksListsDict) 
                    and (changeLog.tuuid in self.tlr.tasksListsDict[changeLog.tluuid].tasks)):
                        del self.tlr.tasksListsDict[changeLog.tluuid].tasks[changeLog.tuuid]
                    else:
                        logger.error("Wrong uuid used for deletion")
                else:
                    logger.error("Wrong object type used for creation")
                    return False
                print("delete")

            else:
                return False
        
        # Persist cache if required
        if doPersist:
            self.tlrFile.persist(self.tlr)

        return True
    
    def getCachedRepoVersion(self) -> int:
        if self.tlr is not None:
            return self.tlr.version
        else:
            return 0

    def refresh(self, serverTlr) -> bool:
        """
        This function is used to refresh the cache when a change is received from the server
        """
        self.tlr = serverTlr

        return True

    def moveTask_atPos(self, tluuid: UUID, tuuid: UUID, pos_key: int) -> bool:
        task = self.tlr.tasksListsDict[tluuid].tasks.pop(tuuid)
        self.insertTask_atPos(tluuid, task, pos_key)
        return True

    def insertTask_atPos(self, tluuid: UUID, task: Task, pos_key: int) -> bool:
        new_dict = OrderedDict()
        if pos_key == len(self.tlr.tasksListsDict[tluuid].tasks)+1:
            self.tlr.tasksListsDict[tluuid].tasks[task.uuid]=task
        else:
            i = 1
            for k, v in self.tlr.tasksListsDict[tluuid].tasks.items():
                if i==pos_key:
                    new_dict[task.uuid] = task  # insert task
                new_dict[k] = v
                i += 1
            self.tlr.tasksListsDict[tluuid].tasks = new_dict
        return True
