#from jdw.mfc.entropy.pascal.validate.base import FactorsValidate
from jdw.mfc.entropy.pascal.validate.basic import FactorsValidate
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
        data = market_data.sort_values(by=['trade_date', 'code']).set_index(
            ['trade_date', 'code']).unstack()
        return data


    def create_dummy(self, begin_date, end_date, universe_name, dummy_name):
        dummy = UniverseDummy(universe_name) & UniverseDummy(dummy_name)
        return dummy.query(start_date=begin_date, end_date=end_date)
    
    def fetch_dummy(self, begin_date, end_date, name):
        l_dummy = UniverseDummy(u_name=name).query(
            start_date=begin_date,end_date=end_date)
        r_dummy = UniverseDummy(u_name='full').query(
            start_date=begin_date,end_date=end_date)
        l_dummy['value'] = 1
        r_dummy['value'] = 1
        return l_dummy.set_index(['trade_date','code'])['value'].unstack() * r_dummy.set_index(['trade_date','code'])['value'].unstack()


    def batch_dummy(self, begin_date, end_date, dummy_array):
        dummy_res = {}
        for dummy in dummy_array:
            dummy_data = self.fetch_dummy(
                begin_date=begin_date,
                end_date=end_date,
                name=dummy)
            dummy_res[dummy] = dummy_data
        return dummy_res
    


    def create_yields(self, begin_date, end_date, horizon, yields_name):
        yields_data = FutYields().fetch_returns(
            universe=None,
            name=yields_name,
            start_date=begin_date,
            offset=0,
            horizon=horizon - 1,  #默认 +1
            end_date=end_date).sort_values(by=['trade_date', 'code'])
        return yields_data.set_index(['trade_date','code']).unstack()

    def fetch_factors(self, begin_date, end_date):
        factors_data = FutFactors().category(
            universe=None,
            category='fut_factor_volume',
            start_date=begin_date,
            end_date=end_date)
        return factors_data

    def create_factors(self, begin_date, end_date):
        inst_module = self.factors_class(begin_date=begin_date,
                                         end_date=end_date,
                                         data_format=0)
        #window = inst_module.get_window()
        #market_data = self.fetch_data(begin_date=begin_date,
        #                              end_date=end_date,
        #                              window=window)
        factors_columns = inst_module.factors_list()
        res = {}
        for func in factors_columns:
            print(func)
            func_module = getattr(inst_module, func)
            fun_param = inspect.signature(func_module).parameters
            if 'dependencies' not in fun_param:
                continue
            #dependencies = fun_param['dependencies'].default
            #result = func_module(data=market_data[dependencies].copy())
            result = func_module()
            if isinstance(result, dict):
                for r in result.values():
                    res[r.id] = r
            elif isinstance(result, tuple):
                for r in result:
                    res[r.id] = r
            else:
                res[result.id] = result
        return res

    def prepare_data(self, begin_date, end_date):
        #horizon_array = [params.horizon for params in self.params_array]
        dummy_array = [params.dummy_name for params in self.params_array]
        universe_array = [params.universe_name for params in self.params_array]

        
        dummy_data = self.batch_dummy(begin_date=begin_date,
                                      end_date=end_date,
                                      dummy_array=dummy_array)

        universe_data = self.batch_dummy(begin_date=begin_date,
                                      end_date=end_date,
                                      dummy_array=universe_array)
        
        yields_data = self.create_yields(begin_date=begin_date,
                                             end_date=end_date,
                                             horizon=1,
                                             yields_name=self.yields_name)
        
        factors_data = self.create_factors(begin_date=begin_date,
                                           end_date=end_date)

        #factros_diff = self.fetch_factors(begin_date=begin_date, end_date=end_date)
        
        return dummy_data, universe_data, yields_data, factors_data, None