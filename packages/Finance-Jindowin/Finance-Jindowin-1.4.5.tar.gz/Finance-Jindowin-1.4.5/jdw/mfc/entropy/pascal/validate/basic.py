# -*- coding: utf-8 -*-
import datetime, pdb, math
import pandas as pd
import numpy as np
from ultron.factor.dimension import DimensionBinaryCorrcoef, DimensionCorrcoef
from ultron.factor.dimension.corrcoef import FCorrType
from ultron.ump.similar.corrcoef import ECoreCorrType
from ultron.ump.core.process import add_process_env_sig, EnvProcess
from ultron.kdutils.parallel import delayed, Parallel
from ultron.kdutils.progress import Progress
from ultron.factor.fitness.score import ScoreTuple
from ultron.factor.fitness.validate import Validate
from ultron.tradingday import *
from jdw.mfc.entropy.pascal.validate.tuple import DetailTuple

def split_k(k_split, columns):
    if len(columns) < k_split:
        return [[col] for col in columns]
    sub_column_cnt = int(len(columns) / k_split)
    group_adjacent = lambda a, k: zip(*([iter(a)] * k))
    cols = list(group_adjacent(columns, sub_column_cnt))
    residue_ind = -(len(columns) %
                        sub_column_cnt) if sub_column_cnt > 0 else 0
    if residue_ind < 0:
        cols.append(columns[residue_ind:])
    return cols

@add_process_env_sig
def do_correlation(target_columns, factors_data, factros_diff, corr_array):
    res = []
    rfeatures = list(factros_diff.keys())
    diff_dt = [factros_diff[f].unstack() for f in rfeatures]
    diff_dt = pd.concat(diff_dt,axis=1)
    diff_dt.columns = rfeatures
    for target in target_columns:
        ft_data = factors_data[target[0]]
        lfeatures = [target[0]]
        ft_data = pd.concat([diff_dt,ft_data.unstack()],axis=1)
        ft_data.rename(columns={0:target[0]},inplace=True)
        ft_data = ft_data.reset_index()[['trade_date','code'] + rfeatures + lfeatures]

        corr = DimensionBinaryCorrcoef(lfeatures=lfeatures, rfeatures=rfeatures, thresh=corr_array[target[1]], method=FCorrType.F_TS_CORR)
        _ = corr.run(factors_data=ft_data, similar_type=ECoreCorrType.E_CORE_TYPE_SPERM)

        res.append(
            {'factor_name':target[0],
            'id':target[1],'dummy':target[2],
            'universe':target[3],'horizon':target[4],'filter':1 if len(corr._filter) == 0 else -1,'corr':corr._corrcoef})
    return pd.DataFrame(res)
        

@add_process_env_sig
def do_metrics(dummy_data, universe_data, yields_data, factors_data, params):
    score_tuple_array = []
    factors_columns = list(factors_data.keys())
    with Progress(len(factors_columns), 0, label='factors metrics') as pg:
        i = 0
        for f in factors_columns:
            i += 1
            st = ScoreTuple(name=f,
                            factors=factors_data[f],
                            returns=yields_data,
                            hold=params.horizon,
                            dummy=dummy_data * universe_data)
            score_tuple_array.append(st)
            pg.show(i)
    columns_name = [col['name'] for col in params.score.obj]
    columns_score = [col['value'] for col in params.score.obj]
    validate = Validate(score_tuple_array,
                        columns_name=columns_name,
                        columns_score=columns_score)
    score_pd = validate.score_pd
    ### validate_data 因子之间相关性比较 收益率倒序排
    filter_pd = score_pd[score_pd['filter']==1].sort_values(by=['returns_mean'],ascending=False)
    if filter_pd.empty:
        return score_pd
    features = filter_pd.index.tolist()
    dt = [factors_data[f].unstack() for f in features]
    dt = pd.concat(dt,axis=1) if len(dt) > 0 else pd.DataFrame()
    
    dt.columns = features
    dt = dt.reset_index()[['trade_date','code'] + features]

    corr = DimensionCorrcoef(features=features,thresh=params.corr_limit, method=FCorrType.F_TS_CORR)
    outfactor = corr.run(factors_data=dt[['trade_date','code'] + features],similar_type=ECoreCorrType.E_CORE_TYPE_SPERM)
    new_features = [col for col in outfactor.columns if col not in ['trade_date','code']] 

    score_pd['filter'] = -1
    score_pd.loc[score_pd.index.isin(new_features), 'filter'] = 1


    score_pd['id'] = params.id
    score_pd['dummy'] = params.dummy_name
    score_pd['universe'] = params.universe_name
    score_pd['corr_limit'] = params.corr_limit
    score_pd['horizon'] = params.horizon

    return score_pd


class FactorsValidate(object):
    def __init__(self,
                 factors_class,
                 params_array,
                 k_split=4,
                 yields_name=None,
                 factors_columns=None):
        
        self.factors_class = factors_class
        self.params_array = params_array
        self.factors_columns = factors_columns
        self.yields_name = yields_name
        self.k_split = k_split

    def conver_date(self, begin_date, end_date):
        end_date = datetime.datetime.now().date(
        ) if end_date is None else end_date
        start_date = advanceDateByCalendar('china.sse', end_date,
                                           "-{}b".format(120 * 12),
                                           BizDayConventions.Following)

        dates = carveSchedule(start_date,
                              end_date,
                              '-5ys',
                              calendar='china.sse',
                              dateRule=BizDayConventions.Following,
                              dateGenerationRule=DateGeneration.Backward)
        end_date = dates[-1]
        begin_date = dates[-11]
        return begin_date, end_date
    
    def create_detail(self, category, factors_detail, is_format=1):
        def to_horizon(l):
            res = []
            for i in  l:
                if isinstance(i, list):
                    res.append(i[0])
                else:
                    res.append(i)
            return list(set(res))

                

        details = {}
        for row in factors_detail.itertuples():
            status = 1 if not hasattr(row, 'status') else row.status
            derive = 1 if not hasattr(row, 'derive') else row.derive
            derive_universe = '' if not hasattr(row, 'derive_universe') else row.derive_universe
            author = 'ultron' if not hasattr(row, 'author') else row.author
            owner = 'hermes' if not hasattr(row,'owner') else row.owner
            freq = 'daily' if not hasattr(row,'freq') else row.freq
            begin_date = '2015-01-01' if not hasattr(row,'begin_date') else row.begin_date
            
            dt = {
                'category':category,
                'name':self.factors_class.__module__,
                'class_name':self.factors_class.__name__,
                'owner':owner,'freq':freq,
                'begin_date':begin_date,
                'id':row.id,
                'func':row.name,
                'status':status,
                'author':author,
                'horizon':row.horizon,
                'universe':row.universe,
                'derive':derive,
                'derive_universe':derive_universe}
            #if row.id in details:
            #    detail = details[row.id]
            #    dt['universe'] = [detail['universe'], dt['universe']] if not isinstance(detail['universe'], list) else detail['universe'] + [dt['universe']]
            #    dt['horizon'] = [detail['horizon'], dt['horizon']] if not isinstance(detail['horizon'], list) else detail['horizon'] + [dt['horizon']]
            #    dt['derive_universe'] = [detail['derive_universe'], dt['derive_universe']] if not isinstance(detail['derive_universe'], list) else detail['derive_universe'] + [dt['derive_universe']]
            details[row.id] = dt

        detail_array = [
            DetailTuple(category=v['category'], 
                        name=v['name'],
                        class_name=v['class_name'],
                        id=v['id'],
                        func=v['func'],
                        status=v['status'],
                        #universe=",".join(set(v['universe'])) if isinstance(v['universe'], list) else v['universe'],
                        #horizon= ','.join(map(str, to_horizon(v['horizon']))),
                        universe = v['universe'],
                        horizon = v['horizon'],
                        author=v['author'],
                        owner=v['owner'],
                        freq=v['freq'],
                        begin_date=v['begin_date'],
                        derive=v['derive'],
                        derive_universe=v['derive_universe']
                    #derive_universe=",".join(item for item in set(v['derive_universe']) if not isinstance(item, float) or not math.isnan(item)) if isinstance(v['derive_universe'], list) else v['derive_universe']
                    )  for k, v in details.items()]
        return detail_array if is_format == 0 else [d._asdict() for d in detail_array]

    def metrics(self, dummy_data, universe_data, yields_data, factors_data):
        parallel = Parallel(4, verbose=0, pre_dispatch='2*n_jobs')

        validate_array = parallel(
            delayed(do_metrics)(dummy_data=dummy_data[params.dummy_name],
                                universe_data = universe_data[params.universe_name],
                                yields_data = yields_data,
                                factors_data=factors_data,
                                params=params,
                                env=EnvProcess())
            for params in self.params_array)
        
        validate_data = pd.concat(validate_array,axis=0)
        validate_data.index.name = 'factor_name'
        return validate_data.reset_index()
    
    def correlation(self, validate_data, factors_data, factros_diff):
        forward_validate = validate_data[validate_data['filter'] == 1]
        corr_array = dict(zip([col.id for col in self.params_array],[col.corr_limit for col in self.params_array]))
        factors_list = forward_validate[['factor_name','id','dummy','universe','horizon','corr_limit']].values.tolist()
        process_list = split_k(self.k_split, factors_list)
        parallel = Parallel(len(process_list), verbose=0, pre_dispatch='2*n_jobs')
        res = parallel(
            delayed(do_correlation)(target_columns=target_columns,
            factors_data=factors_data,factros_diff=factros_diff,corr_array=corr_array,
                                env=EnvProcess())
            for target_columns in process_list)
        return pd.concat(res,axis=0)

    def calculate(self, begin_date=None, end_date=None):
        begin_date, end_date = self.conver_date(begin_date, end_date)
        dummy_data,universe_data,yields_data,factors_data,factors_diff = self.prepare_data(
            begin_date, end_date)
        
        validate_data = self.metrics(
            dummy_data=dummy_data, 
            universe_data=universe_data,
            yields_data=yields_data, 
            factors_data=factors_data)
        if factors_diff is not None:
            corr_data = self.correlation(validate_data=validate_data, 
                         factors_data=factors_data, 
                         factros_diff=factors_diff)
            dt = corr_data.merge(validate_data.drop(['filter'],axis=1), on=['factor_name', 'id', 'dummy', 'universe','horizon'], how='outer')
            dt['filter'] = dt['filter'].fillna(0)
        else:
            dt = validate_data
        factor_link = self.factors_class(data_format=2).factor_link()
        return dt.drop(['id'],axis=1).rename(
            columns={'factor_name':'id'}).merge(
                pd.DataFrame(factor_link), on=['id'])