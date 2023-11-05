from jdw.mfc.entropy.pascal.validate.base import FactorsValidate
from jdw.data.SurfaceAPI.futures.post_market import PostMarket
from jdw.data.SurfaceAPI.futures.yields import FutYields
from jdw.data.SurfaceAPI.futures.factors import FutFactors
from jdw.data.SurfaceAPI.universe import UniverseDummy
from ultron.tradingday import *
import pandas as pd
import pdb, inspect


class FuturesValidate(FactorsValidate):

    def __init__(self,
                 factors_class,
                 params_array,
                 yields_name,
                 factors_columns=None):
        super(FuturesValidate, self).__init__(factors_class=factors_class,
                                              params_array=params_array,
                                              yields_name=yields_name,
                                              factors_columns=factors_columns)

    def fetch_data(self, begin_date, end_date, window):
        start_date = advanceDateByCalendar('china.sse', begin_date,
                                           "-{}b".format(window),
                                           BizDayConventions.Following)
        market_data = PostMarket().market(universe=None,
                                          start_date=start_date,
                                          end_date=end_date,
                                          columns=[
                                              'openPrice', 'highestPrice',
                                              'lowestPrice', 'closePrice',
                                              'turnoverVol', 'turnoverValue'
                                          ]).rename(
                                              columns={
                                                  'openPrice': 'open',
                                                  'highestPrice': 'high',
                                                  'lowestPrice': 'low',
                                                  'closePrice': 'close',
                                                  'turnoverVol': 'volume',
                                                  'turnoverValue': 'value'
                                              })
        market_data['vwap'] = market_data['close']
        return market_data

    def batch_yields(self, begin_date, end_date, horizon_array, yields_name):
        yields_res = {}
        for horizon in horizon_array:
            yields_data = self.create_yields(begin_date=begin_date,
                                             end_date=end_date,
                                             horizon=horizon,
                                             yields_name=yields_name)
            yields_res[horizon] = yields_data
        return yields_res

    def batch_dummy(self, begin_date, end_date, dummy_array):
        dummy_res = {}
        for dummy in dummy_array:
            dummy_data = self.create_dummy(
                begin_date=begin_date,
                end_date=end_date,
                universe_name=dummy['universe_name'],
                dummy_name=dummy['dummy_name'])
            ## universe + dummy
            name = "{0}_{1}".format(dummy['universe_name'],
                                    dummy['dummy_name'])
            dummy_res[name] = dummy_data
        return dummy_res

    def create_dummy(self, begin_date, end_date, universe_name, dummy_name):
        dummy = UniverseDummy(universe_name) & UniverseDummy(dummy_name)
        return dummy.query(start_date=begin_date, end_date=end_date)

    def create_yields(self, begin_date, end_date, horizon, yields_name):
        yields_data = FutYields().fetch_returns(
            universe=None,
            name=yields_name,
            start_date=begin_date,
            offset=0,
            horizon=horizon - 1,  #默认 +1
            end_date=end_date).sort_values(by=['trade_date', 'code'])
        return yields_data

    def fetch_factors(self, begin_date, end_date):
        factors_data = FutFactors().category(
            universe=None,
            category='fut_factor_volume',
            start_date=begin_date,
            end_date=end_date)
        return factors_data

    def create_factors(self, begin_date, end_date):
        factors_engine = self.factors_class()
        window = factors_engine.get_window()
        market_data = self.fetch_data(begin_date=begin_date,
                                      end_date=end_date,
                                      window=window)
        data = market_data.sort_values(by=['trade_date', 'code']).set_index(
            ['trade_date', 'code']).unstack()
        inst_module = self.factors_class(begin_date=begin_date,
                                         end_date=end_date,
                                         data_format=0)
        factors_columns = inst_module.factors_list()
        res = []
        for func in factors_columns:
            func_module = getattr(inst_module, func)
            fun_param = inspect.signature(func_module).parameters
            if 'dependencies' not in fun_param:
                continue
            dependencies = fun_param['dependencies'].default
            result = func_module(data=data[dependencies].copy())
            if isinstance(result, dict):
                for r in result.values():
                    r['id'] = r.id
                    res.append(r)
            elif isinstance(result, tuple):
                for r in result:
                    res.append(r)
            else:
                res.append(result)

        return pd.concat(res, axis=1)

    def prepare_data(self, begin_date, end_date):
        horizon_array = [params.horizon for params in self.params_array]
        dummy_array = [{
            'dummy_name': params.dummy_name,
            'universe_name': params.universe_name
        } for params in self.params_array]

        ##
        dummy_array = self.batch_dummy(begin_date=begin_date,
                                       end_date=end_date,
                                       dummy_array=dummy_array)

        yields_array = self.batch_yields(begin_date=begin_date,
                                         end_date=end_date,
                                         horizon_array=horizon_array,
                                         yields_name=self.yields_name)

        factors_data = self.create_factors(begin_date=begin_date,
                                           end_date=end_date)

        factros_diff = self.fetch_factors(begin_date=begin_date, end_date=end_date)
        
        return dummy_array, yields_array, factors_data,factros_diff