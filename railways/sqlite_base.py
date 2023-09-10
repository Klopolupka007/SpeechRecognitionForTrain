# Copyright 2017 Neural Networks and Deep Learning lab, MIPT
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sqlite3
from logging import getLogger

from deeppavlov.core.common.registry import register
from deeppavlov.core.models.component import Component

logger = getLogger(__name__)


@register('sqlite_vocab')
class SQLiteVocab(Component):
    def __init__(self, load_path, **kwargs):
        self.conn = sqlite3.connect(load_path)
        self.cursor = self.conn.cursor()

    def __call__(self, doc_ids_batch, *args, **kwargs):
        text_batch = []
        for doc_ids in doc_ids_batch:
            texts = []
            for doc_id in doc_ids:
                query = "SELECT * FROM documents WHERE id=?;"
                res = self.cursor.execute(query, (doc_id,))
                res = res.fetchall()
                texts.append(res[0])
            text_batch.append(texts)
        return text_batch
