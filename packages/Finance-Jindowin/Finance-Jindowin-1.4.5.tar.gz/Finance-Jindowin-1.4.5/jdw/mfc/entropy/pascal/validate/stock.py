from ultron.tradingday import *
from jdw.mfc.entropy.pascal.validate.basic import FactorsValidate
from jdwdata.RetrievalAPI import get_data_by_map, get_factors, get_factor_info
import pandas as pd
import pdb, inspect


class StockValidate(FactorsValidate):
    def __init__(self,
                 factors_class,
                 params_array,
                 yields_name,
                 factors_columns=None):
        super(StockValidate, self).__init__(factors_class=factors_class,
                                              params_array=params_array,
                                              yields_name=yields_name,
                                              factors_columns=factors_columns)
    
    
    def create_factors(self, begin_date, end_date):
        inst_module = self.factors_class(
            begin_date=begin_date.strftime('%Y-%m-%d'), 
            end_date=end_date.strftime('%Y-%m-%d'), data_format=0)
        factors_columns = inst_module.factors_list()
        res = {}
        for func in factors_columns:
            func_module = getattr(inst_module, func)
            fun_param = inspect.signature(func_module).parameters
            if 'dependencies' not in fun_param:
                continue
            result = func_module()
            if isinstance(result, dict):
                for r in result.values():
                    res[r.id] = r
            else:
                res[result.id] = result
        return res



    def prepare_data(self, begin_date, end_date):
        
        factors_data = self.create_factors(begin_date=begin_date, end_date=end_date)
        dummy_array = [params.dummy_name for params in self.params_array]
        universe_array = [params.universe_name for params in self.params_array]

        data = get_data_by_map(columns=dummy_array + universe_array + [self.yields_name],
                               begin_date=begin_date.strftime('%Y-%m-%d'),
                               end_date=end_date.strftime('%Y-%m-%d'),
                               method='ddb')
        
        factor_info = get_factor_info(category=None, freq='daily',universe='dummy120_fst')
        #factor_info = factor_info.loc[0:10]
        factors_diff = None
        if factor_info is not None:
            ## 提取因子
            factors_diff = get_factors(begin_date=begin_date.strftime('%Y-%m-%d'),
                              end_date=end_date.strftime('%Y-%m-%d'),
                              ids=factor_info['id'].unique().tolist(),
                              freq='D',
                              format_data=1)
        dummy_data = {key: data[key] for key in dummy_array if key in data}
        universe_data = {key: data[key] for key in universe_array if key in data}
        yields_data = data[self.yields_name]
        return dummy_data, universe_data ,yields_data, factors_data, factors_diff

        
        
        