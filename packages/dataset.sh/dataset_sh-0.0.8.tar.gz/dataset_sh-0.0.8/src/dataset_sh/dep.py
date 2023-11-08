import json
import os
from typing import List, Optional
from pydantic import BaseModel, Field
from urllib.parse import urljoin


class DatasetDependencyItem(BaseModel):
    name: str
    comment: Optional[str] = None

    def to_str(self):
        if self.comment:
            cl = "\n".join([f"  # {c}" for c in self.comment.split('\n')])
            return f"{cl}\n  {self.name}"
        else:
            return f"  {self.name}"


class DatasetDependencyGroup(BaseModel):
    host: str
    items: List[DatasetDependencyItem] = Field(default_factory=list)

    def to_url_list(self):
        for item in self.items:
            yield item.name, get_dataset_url_for_remote_host(self.host, item.name)


class DatasetDependencies(BaseModel):
    groups: List[DatasetDependencyGroup] = Field(default_factory=list)

    def write_to_file(self, fp):
        with open(fp, 'w') as out:
            json.dump(
                self.model_dump(mode='json'),
                out,
                indent=4,
            )

    @staticmethod
    def read_from_file(fp):
        dep = DatasetDependencies()
        with open(fp) as f:
            return DatasetDependencies(**json.load(f))


def locate_dep_file(current_directory, max_it=30):
    file_name = 'dataset.list'
    it = 0
    while True:
        if file_name in os.listdir(current_directory):
            return os.path.abspath(os.path.join(current_directory, file_name))
        if current_directory == '/':
            return None
        current_directory = os.path.dirname(current_directory)
        it += 1
        if it >= max_it:
            return None


def get_dataset_url_for_remote_host(host, dataset):
    h = host
    if not h.endswith('/'):
        h = h + '/'
    absolute_url = urljoin(h, f'api/{dataset}/file')
    return absolute_url
