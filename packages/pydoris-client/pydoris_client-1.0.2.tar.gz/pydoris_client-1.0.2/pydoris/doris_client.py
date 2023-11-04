#! /usr/bin/python3

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import requests
import uuid
from requests.auth import HTTPBasicAuth

from pydoris.selectdb.db_operator import *


class DorisClient:
    def __init__(self):
        self.options = Options()
        self._session = requests.sessions.Session()
        self.stream_load_url = self._build_url

    def _build_url(self, database, table):
        url = ("http://{host}:{port}/api/{database}/{table}/_stream_load"
               .format(host=self.options.fe_host,
                       port=self.options.fe_http_port,
                       database=database,
                       table=table)
               )
        return url

    def write(self, table_name, data):
        database = table_name.split('.')[0]
        table = table_name.split('.')[1]
        self._auth = HTTPBasicAuth(self.options.username, self.options.password)
        self._session.should_strip_auth = lambda old_url, new_url: False
        resp = self._session.request(
            'PUT', url=self._build_url(database, table),
            data=data,  # open('/path/to/your/data.csv', 'rb'),
            headers=self.options.get_options(),
            auth=self._auth
        )
        import json
        print(resp.text)
        load_status = json.loads(resp.text)['Status'] == 'Success'
        if resp.status_code == 200 and resp.reason == 'OK' and load_status:
            return True
        else:
            return False

    def query(self, sql):
        return self.options.db_operator.query(sql)

    def execute(self, sql):
        self.options.db_operator.execute(sql)

    def query_to_dataframe(self, sql, columns: list):
        return self.options.db_operator.read_to_df(sql, columns)

    def write_from_df(self, data_df: pd.DataFrame, table_name: str, table_model: str,
                      table_module_key=None,
                      distributed_hash_key=None,
                      buckets=None,
                      table_properties=None,
                      field_mapping: list[tuple] = None):
        self.options.db_operator.create_table_from_df(data_df, table_name, table_model,
                                                      table_module_key,
                                                      distributed_hash_key,
                                                      buckets,
                                                      table_properties,
                                                      field_mapping
                                                      )
        csv = data_df.to_csv(header=False, index=False)
        self.write(table_name, csv)

    def list_tables(self, database):
        list_tuple = self.options.db_operator.get_tables(database)
        return [t[0] for t in list_tuple]

    def drop_table(self, db, table_name):
        return self.options.db_operator.drop_table(f"{db}.{table_name}")

    def create_database(self, database):
        return self.options.db_operator.create_database(database)

    def get_table_columns(self, db, table_name):
        return self.options.db_operator.get_table_columns(f"{db}.{table_name}")


class Options:
    def __init__(self):
        self.db_operator: SelectDBBase
        self.fe_host = None
        self.fe_http_port = None
        self.fe_query_port = None
        self.username = None
        self.password = None
        self.jar_path = None
        self.db = None
        self._headers = {
            'Content-Type': 'text/plain; charset=UTF-8',
            "Content-Length": None,
            "Transfer-Encoding": None,
            "Expect": "100-continue",
            'format': 'csv',
            "column_separator": ',',
        }

    def set_csv_format(self, column_separator):
        self._headers['format'] = 'csv'
        self._headers['column_separator'] = column_separator
        return self

    def set_json_format(self):
        self._headers['format'] = 'json'
        self._headers['read_json_by_line'] = 'true'
        return self

    def set_auto_uuid_label(self):
        self._headers['label'] = str(uuid.uuid4())
        return self

    def set_label(self, label):
        self._headers['label'] = label
        return self

    def set_format(self, data_format: str):
        if data_format.lower() in ['csv', 'json']:
            self._headers['format'] = data_format
        return self

    def set_line_delimiter(self, line_delimiter):
        self._headers['line_delimiter'] = line_delimiter
        return self

    def set_enable_profile(self):
        self._headers['enable_profile'] = 'true'
        return self

    def set_option(self, k, v):
        self._headers[k] = v
        return self

    def get_options(self):
        return self._headers

    def create_doris_operator(self):
        if self.jar_path is not None:
            self.db_operator = SelectDBBase(f"{self.fe_host}:{self.fe_query_port}", self.db, self.username,
                                            self.password,
                                            self.jar_path)

