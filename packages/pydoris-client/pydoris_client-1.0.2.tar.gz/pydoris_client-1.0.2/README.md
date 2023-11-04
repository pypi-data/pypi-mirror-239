# Apache Doris Python Client
A Apache Doris client for the Python programming language.

Apache Doris is a high-performance, real-time analytical database based on MPP architecture, known for its extreme speed and ease of use. It only requires a sub-second response time to return query results under massive data and can support not only high-concurrent point query scenarios but also high-throughput complex analysis scenarios. All this makes Apache Doris an ideal tool for scenarios including report analysis, ad-hoc query, unified data warehouse, and data lake query acceleration. On Apache Doris, users can build various applications, such as user behavior analysis, AB test platform, log retrieval analysis, user portrait analysis, and order analysis.

## Installation
```
pip install pydoris
```


## DorisClient Usage
DorisClient supports DDL operations such as creating databases/tables, querying, and deleting pandas Dataframe, as well as automatically creating Pandas DataFrame into Doris, and reading doris data into Dataframe
 
```python

import pandas as pd
from pydoris.doris_client import *

client = DorisClient()
fe_host = "10.16.10.6"
fe_http_port = "8036"
fe_query_port = "9036"
username = 'root'
passwd = ""

doris_client = DorisClient()
doris_client.options.fe_host = fe_host
doris_client.options.fe_http_port = fe_http_port
doris_client.options.fe_query_port = fe_query_port
doris_client.options.username = username
doris_client.options.password = passwd
doris_client.options.db = "test"

"""
In addition to writing data to doris, if you need to operate on Doris,
you must call this function with the other parameters set
"""
doris_client.options.jar_path = '/Users/bingquanzhao/Desktop/mysql-connector-java-8.0.27.jar'
doris_client.options.create_doris_operator()

from decimal import Decimal
data = {
    'f_id': [int(1), int(2), int(3)],
    'f_decimal': [Decimal('10.5'), Decimal('20.75'), Decimal('30.25')],
    'f_timestamp': [time.time_ns(), time.time_ns(), time.time_ns()],
    'f_datetime': [datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now()],
    'f_str': [str('1'), str('2'), str('3')],
    'f_float': [float(1.222), float(2.333), float(3.4444)],
    'f_boolean': [True, True, False]
}


def create_db():
    db = 'pydoris_test'
    doris_client.execute(f"create database {db} ;")


def create_table():
    doris_client.execute("""create table if not exists pydoris_test.write_test(
                                   f_id int,
                                   f_decimal decimal(18,6),
                                   f_timestamp bigint,
                                   f_datetime datetime(6),
                                   f_str string,
                                   f_float float,
                                   f_boolean boolean

                                   )duplicate key(`f_id`)
                                   distributed by hash(`f_id`) buckets 1
                                   properties("replication_allocation" = "tag.location.default: 1");""")


def list_tables():
    tables = doris_client.list_tables("pydoris_test")
    print(tables)


def write_table():
    from decimal import Decimal

    df = pd.DataFrame(data)

    """
    write from csv
    """
    csv = df.to_csv(header=False, index=False)
    print(csv)
    doris_client.options.set_csv_format(",").set_auto_uuid_label().set_line_delimiter("\\n")
    doris_client.write("pydoris_test.write_test", csv)
    """write from json"""
    # j = df.to_json(orient="records", force_ascii=False, date_format='iso', date_unit='us')
    # print(j)
    # doris_client.options.set_json_format().set_auto_uuid_label()
    # doris_client.write("pydoris_test.write_test", j)


def write_from_df():
    df = pd.DataFrame(columns=["f_id", "f_decimal", "f_timestamp", "f_datetime", "f_str", "f_float", "f_boolean"],
                      data=data)
    # default replication_allocation = tag.location.default: 1, if you need individual setting，Please fill in configuration
    doris_client.write_from_df(df, "pydoris_test.df_write_test", "UNIQUE", ['f_id'],
                               distributed_hash_key=["f_id"], buckets=1,
                               field_mapping=[("f_decimal", "Decimal(20,8)")]
                               , table_properties={"replication_allocation": "tag.location.default: 1"})


def query():
    result = doris_client.query("select * from pydoris_test.write_test limit 100")
    print(result)


def query_to_df():
    result = doris_client.query_to_dataframe("select * from pydoris_test.df_write_test limit 100",
                                             ["f_id", "f_decimal", "f_timestamp", "f_datetime", "f_str", "f_float",
                                              "f_boolean"])
    print(result)

def drop_table():
    db = 'pydoris_test'
    table_name = 'df_write_test'
    doris_client.drop_table(db, table_name)

if __name__ == '__main__':
    # drop_table()
    # create_db()
    # create_table()
    # write_table()
    # write_from_df()
    query()
    query_to_df()
    # list_tables()

```
