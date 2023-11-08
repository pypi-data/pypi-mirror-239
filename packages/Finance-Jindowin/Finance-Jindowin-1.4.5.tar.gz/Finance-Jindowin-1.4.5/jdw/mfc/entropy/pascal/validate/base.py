# -*- coding: utf-8 -*-
import datetime, pdb
import pandas as pd
from ultron.factor.dimension import DimensionBinaryCorrcoef, DimensionCorrcoef
from ultron.factor.dimension.corrcoef import FCorrType
from ultron.ump.similar.corrcoef import ECoreCorrType
from ultron.ump.core.process import add_process_env_sig, EnvProcess
from ultron.kdutils.parallel import delayed, Parallel
from ultron.kdutils.progress import Progress
from ultron.factor.fitness.score import ScoreTuple
from ultron.factor.fitness.validate import Validate
from ultron.tradingday import *



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
    for target in target_columns:
        ft_data = factors_data[target[0]]
        #dy_data = dummy_array["{0}_{1}".format(target[3],target[2])]
        lfeatures = [target[0]]
        ## 1. 需要绩效过滤 factros_diff 保留绩效大于指定的 2.根据绩效倒序排序 --> return 
        rfeatures = [col for col in factros_diff.columns if col not in ['trade_date','code']]
        dt = ft_data.reset_index().merge(factros_diff, on=['trade_date','code']).sort_values(by=['trade_date','code'])
        dc = DimensionBinaryCorrcoef(lfeatures=lfeatures, rfeatures=rfeatures, thresh=corr_array[target[1]], method=FCorrType.F_TS_CORR)
        _ = dc.run(factors_data=dt, similar_type=ECoreCorrType.E_CORE_TYPE_SPERM)
        res.append(
            {'factor_name':target[0],
            'id':target[1],'dummy':target[2],
            'universe':target[3],'horizon':target[4],'filter':1 if len(dc._filter) == 0 else -1,'corr':dc._corrcoef})
    return pd.DataFrame(res)


# 每个params 为独立进程
@add_process_env_sig
def do_metrics(dummy_data, yields_data, factors_data, params):
    score_tuple_array = []
    pdb.set_trace()
    factors_columns = factors_data.columns
    total_data = factors_data.reset_index().merge(
        yields_data, on=['trade_date',
                         'code']).merge(dummy_data,
                                        on=['trade_date', 'code'],
                                        how='outer')
    total_data = total_data.sort_values(by=['trade_date', 'code']).set_index(
        ['trade_date', 'code'])
    yields_data = total_data[['nxt1_ret']]
    factors_data = factors_data[factors_columns]
    dummy_data = pd.crosstab(total_data.index.get_level_values('trade_date'),
                             total_data.index.get_level_values('code'),
                             values=1,
                             aggfunc='sum')
    with Progress(len(factors_columns), 0, label='factors metrics') as pg:
        i = 0
        for f in factors_columns:
            i += 1
            st = ScoreTuple(name=f,
                            factors=factors_data[f].unstack(),
                            returns=yields_data['nxt1_ret'].unstack(),
                            hold=params.horizon,
                            dummy=dummy_data)
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
    features = filter_pd.index.tolist()
    corr = DimensionCorrcoef(features=features,thresh=params.corr_limit, method=FCorrType.F_TS_CORR)
    outfactor = corr.run(factors_data=factors_data[features].reset_index(),similar_type=ECoreCorrType.E_CORE_TYPE_SPERM)
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
                 yields_name=None,
                 factors_columns=None):
        self.factors_class = factors_class
        self.params_array = params_array
        self.factors_columns = factors_columns
        self.yields_name = yields_name

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

    def calculate(self, begin_date=None, end_date=None):
        pdb.set_trace()
        begin_date, end_date = self.conver_date(begin_date, end_date)
        dummy_array, yields_array, factors_data, factros_diff = self.prepare_data(
            begin_date, end_date)
        parallel = Parallel(1, verbose=0, pre_dispatch='2*n_jobs')
        validate_array = parallel(
            delayed(do_metrics)(dummy_array["{0}_{1}".format(
                params.universe_name, params.dummy_name)],
                                yields_array[params.horizon],
                                factors_data=factors_data,
                                params=params,
                                env=EnvProcess())
            for params in self.params_array)

        pdb.set_trace()
        ### 筛选出来因子 
        validate_data = pd.concat(validate_array,axis=0)
        ###
        forward_validate = validate_data[validate_data['filter'] == 1] 

        ### 
        corr_array = dict(zip([col.id for col in self.params_array],[col.corr_limit for col in self.params_array]))
        validate_data.index.name = 'factor_name'
        factors_list = forward_validate[['id','dummy','universe','horizon','corr_limit']].reset_index().values.tolist()
        process_list = split_k(4, factors_list)
        parallel = Parallel(4, verbose=0, pre_dispatch='2*n_jobs')
        res = parallel(
            delayed(do_correlation)(target_columns=target_columns,
            factors_data=factors_data,factros_diff=factros_diff,corr_array=corr_array,
                                env=EnvProcess())
            for target_columns in process_list)
        df2 = validate_data.reset_index()
        df1 = pd.concat(res,axis=0)
        dt = df1.merge(df2.drop(['filter'],axis=1), on=['factor_name', 'id', 'dummy', 'universe','horizon'], how='outer')
        return dt


