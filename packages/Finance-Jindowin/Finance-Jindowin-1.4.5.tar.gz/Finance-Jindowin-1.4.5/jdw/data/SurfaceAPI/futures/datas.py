# -*- coding: utf-8 -*-
import pdb
import pandas as pd
import numpy as np
from sqlalchemy import select, and_, outerjoin, join
from collections import namedtuple
from jdw.data.SurfaceAPI.engine import FetchKDEngine



class ElementTuple(
    namedtuple('ElementTuple',
               ('alias_name','column_name','table_name'))):
    
    __slots__ = ()

    def __repr__(self) :
        return "alias name:{}\n column name:{}\n table_name:{}\n".format(
            self.alias_name,self.column_name,self.table_name
        )
    
class FutDatas(object):
    def __init__(self):
        self._engine = FetchKDEngine()
        self.datas_cols = {}
        self.mapping_cols = {}
        self.initialize()
    
    def initialize(self):
        def create_element(alias_name, column_name, table_name):
            self.datas_cols[alias_name] = ElementTuple(alias_name=alias_name,
                                                   column_name=column_name,
                                                   table_name=table_name)
            self.mapping_cols["{}.{}".format(column_name, table_name)] = alias_name
        
        create_element('presettle','preSettlePrice','market_post_fut')
        create_element('open','openPrice','market_post_fut')
        create_element('high','highestPrice','market_post_fut')
        create_element('low','lowestPrice','market_post_fut')
        create_element('close','closePrice','market_post_fut')
        create_element('settle','settlePrice','market_post_fut')
        create_element('volume','turnoverVol','market_post_fut')
        create_element('value','turnoverValue','market_post_fut')
        create_element('openint','openInt','market_post_fut')


        create_element('index_presettle','preSettlePrice','market_index_fut')
        create_element('index_open','openPrice','market_index_fut')
        create_element('index_high','highestPrice','market_index_fut')
        create_element('index_low','lowestPrice','market_index_fut')
        create_element('index_close','closePrice','market_index_fut')
        create_element('index_settle','settlePrice','market_index_fut')
        create_element('index_volume','turnoverVol','market_index_fut')
        create_element('index_value','turnoverValue','market_index_fut')
        create_element('index_openint','openInt','market_post_fut')
    
    def fetch_tables(self, columns):
        data_cols = {}
        columns = set(columns).difference({'trade_date', 'code'})
        for c in columns:
            n = self.datas_cols[c]
            t = self._engine._base.classes[n.table_name]
            if n.column_name in t.__table__.columns:
                data_cols[t.__table__.columns[n.column_name]] = t
        return data_cols
    
    def transfor(self, data_cols):
        return [col.label(
            self.mapping_cols["{}.{}".format(
                col.name,col.table.name)]) for col in data_cols.keys()]


    def fetch_data(self, start_date, end_date, columns, is_format=1):
        data_cols = self.fetch_tables(columns=columns)
        joined_tables = set()
        data_tables = list(set(data_cols.values()))
        if len(data_cols) <= 0:
            raise ValueError("data_tables len({0})".format(len(data_tables)))
        
        big_table = data_tables[0]
        joined_tables.add(big_table.__table__.name)
        for t in set(data_cols.values()):
            if t.__table__.name not in joined_tables:
                big_table = outerjoin(
                    big_table, t,
                    and_(big_table.trade_date == t.trade_date,
                         big_table.code == t.code, t.flag == 1))
                joined_tables.add(t.__table__.name)
        
        clause_list = and_(
            data_tables[0].flag == 1,
            data_tables[0].trade_date.between(start_date, end_date))
        cols = self.transfor(data_cols)
        query = select(
            [data_tables[0].trade_date, data_tables[0].code] + cols).select_from(
                big_table).where(clause_list)
        data =  pd.read_sql(query, self._engine.client()).drop_duplicates(
            subset=['trade_date', 'code']).replace(
                [-np.inf, np.inf],
                np.nan).sort_values(by=['trade_date', 'code'])
        
        if is_format == 0:
            res = {}
            data.set_index(['trade_date','code'],inplace=True)
            for col in columns:
                res[col] = data[col].unstack()
            return res
        else:
            return data