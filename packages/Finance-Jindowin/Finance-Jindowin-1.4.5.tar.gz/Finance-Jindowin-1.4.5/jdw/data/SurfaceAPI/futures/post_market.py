# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import pdb
from sqlalchemy import select, and_, join
from jdw.data.SurfaceAPI.engine import FetchKDEngine
from jdw.data.SurfaceAPI.universe import BaseUniverse
from jdw.data.SurfaceAPI.universe import UniverseDummy


class PostMarket(object):

    def __init__(self):
        self._engine = FetchKDEngine()
        self._table_model = self._engine.table_model('market_post_fut')

    def market(self, universe, start_date, end_date, columns, is_format=2):
        cols = [self._table_model.trade_date, self._table_model.code]
        for col in columns:
            cols.append(self._table_model.__dict__[col])
        return self.query(universe=universe,
                          start_date=start_date,
                          end_date=end_date,
                          data_cols=cols)
            

    def query(self, universe, start_date, end_date, data_cols):
        universe_model = universe._table_model if isinstance(
            universe, BaseUniverse) else None
        if isinstance(universe, BaseUniverse):
            cond = universe._query_statements(start_date, end_date)
            big_table = join(
                self._table_model, universe_model,
                and_(
                    self._table_model.trade_date.between(start_date, end_date),
                    self._table_model.flag == 1,
                    self._table_model.trade_date == universe_model.trade_date,
                    self._table_model.code == universe_model.code, cond))
            query = select(data_cols).select_from(big_table)
        elif isinstance(universe, list):
            clause_list = and_(
                self._table_model.flag == 1,
                self._table_model.code.in_(universe),
                self._table_model.trade_date.between(start_date, end_date))

            query = select(data_cols).where(clause_list)
        else:
            clause_list = and_(
                self._table_model.flag == 1,
                self._table_model.trade_date.between(start_date, end_date))

            query = select(data_cols).where(clause_list)

        return pd.read_sql(query, self._engine.client())