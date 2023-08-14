from typing import Any, List, Dict
from uuid import UUID
from KoPrivateGPT.DB.base import BaseDB
from KoPrivateGPT.schema import Passage
import os
import pickle

from KoPrivateGPT.utils import FileChecker


class PickleDB(BaseDB):
    def __init__(self, save_path: str, *args, **kwargs):
        FileChecker(save_path).check_type(file_types=['.pickle', '.pkl'])
        self.save_path = save_path
        self.db = list()

    @property
    def db_type(self) -> str:
        return 'local'

    def create(self):
        if os.path.exists(self.save_path):
            raise FileExistsError(f'{self.save_path} already exists')
        if not os.path.exists(os.path.dirname(self.save_path)):
            os.makedirs(os.path.dirname(self.save_path))
        self.save_path = self.save_path

    def load(self):
        if not FileChecker(self.save_path).check_type(file_types=['.pickle', '.pkl']).is_exist():
            raise FileNotFoundError(f'{self.save_path} does not exist')
        with open(self.save_path, 'rb') as f:
            self.db = pickle.load(f)

    def create_or_load(self):
        if os.path.exists(self.save_path):
            self.load()
        else:
            self.create()

    def save(self, passages: List[Passage]):
        self.db.extend(passages)
        self._write_pickle()

    def fetch(self, ids: List[UUID]) -> List[Passage]:
        result = list(filter(lambda x: x.id in ids, self.db))
        return result

    def search(self, filter: Dict[str, str]) -> List[Passage]:
        raise NotImplementedError("PickleDB does not support search method")

    def _write_pickle(self):
        with open(self.save_path, 'wb') as w:
            pickle.dump(self.db, w)
