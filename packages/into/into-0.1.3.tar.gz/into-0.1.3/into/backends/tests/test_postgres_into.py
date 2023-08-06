from __future__ import absolute_import, division, print_function

import pytest

psycopg2 = pytest.importorskip('psycopg2')
import subprocess
ps = subprocess.Popen("ps aux | grep postgres",shell=True, stdout=subprocess.PIPE)
output = ps.stdout.read()
num_processes = len(output.splitlines())
pytestmark = pytest.mark.skipif(num_processes < 6, reason="No Postgres Installation")


from datashape import dshape
from into.backends.csv import CSV
from into.backends.sql import create_from_datashape
from into import into, resource
from into.utils import assert_allclose
import sqlalchemy
import os
import csv as csv_module
import pandas as pd
import datetime as dt
import numpy as np

url = 'postgresql://localhost/postgres'
url = 'postgresql://postgres:postgres@localhost'
file_name = 'test.csv'


try:
    engine = sqlalchemy.create_engine(url)
    name = 'tmpschema'
    create = sqlalchemy.schema.CreateSchema(name)
    engine.execute(create)
    metadata = sqlalchemy.MetaData()
    metadata.reflect(engine, schema=name)
    drop = sqlalchemy.schema.DropSchema(name)
    engine.execute(drop)
except sqlalchemy.exc.OperationalError:
    pytestmark = pytest.mark.skipif(True, reason="Can not connect to postgres")


data = [(1, 2), (10, 20), (100, 200)]
ds = dshape('var * {a: int32, b: int32}')

def setup_function(function):
    with open(file_name, 'w') as f:
        csv_writer = csv_module.writer(f)
        for row in data:
            csv_writer.writerow(row)

def teardown_function(function):
    os.remove(file_name)
    engine = sqlalchemy.create_engine(url)
    metadata = sqlalchemy.MetaData()
    metadata.reflect(engine)

    for t in metadata.tables:
        if 'testtable' in t:
            metadata.tables[t].drop(engine)

def test_csv_postgres_load():
    csv = CSV(file_name)
    tbl = 'testtable'

    engine = sqlalchemy.create_engine(url)

    if engine.has_table(tbl):
        metadata = sqlalchemy.MetaData()
        metadata.reflect(engine)
        t = metadata.tables[tbl]
        t.drop(engine)

    create_from_datashape(engine, dshape('{testtable: %s}' % ds))
    metadata = sqlalchemy.MetaData()
    metadata.reflect(engine)
    sql = metadata.tables[tbl]
    conn = engine.raw_connection()

    cursor = conn.cursor()
    full_path = os.path.abspath(file_name)
    load = '''copy {0} from '{1}'(FORMAT CSV, DELIMITER ',', NULL '');'''.format(tbl, full_path)
    cursor.execute(load)
    conn.commit()


def test_simple_into():
    tbl = 'testtable_into_2'

    csv = CSV(file_name)
    sql = resource(url, tbl, dshape=ds)

    into(sql, csv, dshape=ds)

    assert into(list, sql) == data

def test_append():
    tbl = 'testtable_into_append'

    csv = CSV(file_name)
    sql = resource(url, tbl, dshape=ds)

    into(sql, csv)
    assert into(list, sql) == data

    into(sql, csv)
    assert into(list, sql) == data + data


def test_tryexcept_into():
    tbl = 'testtable_into_2'

    csv = CSV(file_name)
    sql = resource(url, tbl, dshape=ds)

    into(sql, csv, quotechar="alpha") # uses multi-byte character and
                                      # fails over to using sql.extend()

    assert into(list, sql) == data


@pytest.mark.xfail(raises=KeyError)
def test_failing_argument():
    tbl = 'testtable_into_2'

    csv = CSV(file_name)
    sql = resource(url, tbl, dshape=ds)

    into(sql, csv, skipinitialspace="alpha") # failing call


def test_no_header_no_columns():
    tbl = 'testtable_into_3'

    csv = CSV(file_name)
    sql = resource(url, tbl, dshape=ds)

    into(sql, csv, dshape=ds)

    assert into(list, sql) == data


def test_complex_into():
    # data from: http://dummydata.me/generate
    this_dir = os.path.dirname(__file__)
    file_name = os.path.join(this_dir, 'dummydata.csv')

    tbl = 'testtable_into_complex'
    ds = dshape('var * {Name: string, RegistrationDate: date, ZipCode: int32, Consts: float64}')

    csv = CSV(file_name, has_header=True)
    sql = resource(url, tbl, dshape=ds)

    into(sql, csv)

    assert_allclose(into(list, sql), into(list, csv))
