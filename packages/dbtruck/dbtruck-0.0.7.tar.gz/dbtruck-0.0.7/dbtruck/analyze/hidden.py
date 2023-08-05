import csv
import os
import sys
import pdb
import traceback
sys.path.extend(['..', '.', '../exporters'])

from geopy import geocoders
from collections import defaultdict

from load_data import *
from dbtruck.exporters.db import *
import dbtruck.settings as settings



def create_hidden_table(db, table):
    loctable = '_%s_loc_' % table
    try:
        db.execute('select count(*) from %s' % loctable).fetchone()[0]
        return loctable
    except:
        try:


            # create if it doesn't exist
            q = """create table %s (
                 id int references %s(id),
                 latitude float null,
                 longitude float null,
                 address text null,
                 city varchar(128) null,
                 state varchar(128) null,
                 country varchar(128) null,
                 query text null,
                 description text null,
                 zoom float null,
                 shape polygon null        
            )""" % (loctable, table)
            db.execute(q, bexit=False)

            q = 'create index %s_id on %s (id);' % (loctable, loctable)
            db.execute(q, bexit=False)
            return loctable
        except:
            traceback.print_exc()
            return None

def get_table_cols(db, table):
    cols = db.execute("""select column_name from
    information_schema.columns where table_name = '%s' order by
    ordinal_position asc""" % table).fetchall()
    return [c[0] for c in cols]
    

def get_all_table_names(db):
    try:
        tables = db.execute("""select table_name from
        information_schema.tables where table_schema = 'public' and
        table_type = 'BASE TABLE';""").fetchall()
        return [row[0] for row in tables]
    except:
        return []

def get_hidden_table_names(db):
    for regtable, loctable in get_table_name_pairs(db):
        if regtable and loctable:
            yield loctable

def get_regular_table_names(db):
    for regtable, loctable in get_table_name_pairs(db):
        yield regtable

def get_table_name_pairs(db):
    tables = get_all_table_names(db)
    loctables, regtables = [], []
    for table in tables:
        if table.startswith('_') and table.endswith('_loc_'):
            loctables.append(table)
        else:
            regtables.append(table)

    pairs = []
    for regtable in regtables:
        if ('_%s_loc_' % regtable) in loctables:
            pairs.append((regtable, '_%s_loc_' % regtable))
        else:
            pairs.append((regtable, None))
    return pairs


if __name__ == '__main__':
    from sqlalchemy import *
    from sqlalchemy.orm import scoped_session, sessionmaker
    from sqlalchemy.ext.declarative import declarative_base

    db = create_engine('postgresql://sirrice@localhost:5432/test')

    for pair in get_table_name_pairs(db):
        print pair
