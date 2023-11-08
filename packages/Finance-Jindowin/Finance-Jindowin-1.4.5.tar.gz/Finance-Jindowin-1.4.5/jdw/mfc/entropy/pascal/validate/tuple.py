import abc, pdb, itertools,hashlib,json
from collections import namedtuple
from ultron.kdutils.create_id import create_id


class ParamsTuple(
        namedtuple(
            'ParamsTuple',
            ('dummy_name', 'universe_name', 'corr_limit', 'score', 'horizon'))
):
    __slots__ = ()

    def __repr__(self):
        return "dummy_name:{}\nuniverse_name:{}\ncorr_limit:{}\nhorizon:{}\n".format(
            self.dummy_name, self.universe_name, self.corr_limit, self.horizon)
    
    def encryption(self, feature):
        s = hashlib.md5(
            json.dumps(feature).encode(encoding="utf-8")).hexdigest()
        return create_id(original=s, digit=15)

    @property
    def id(self):
        return self.encryption({'dummy_name':self.dummy_name,
                        'universe_name':self.universe_name,'corr_limit':self.corr_limit,
                        'horizon':self.horizon})


class DetailTuple(
    namedtuple(
        'DetailTuple',('category','name','class_name','id','func','status','begin_date',
                       'owner','freq', 'universe','horizon','author',
                       'derive','derive_universe'))
                       ):

    __slots__ = ()

    def __repr__(self):
        return "id:{}\ncategory:{}\nname:{}\nclass{}:\nfunc:{}\nstatus:{}\nuniverse:{}\nhorizon:{},author:{}\nfreq:{}\n,owner:{}\nderive:{}\nderive_universe:{}".format(
            self.id, self.category, self.name, self.class_name, self.func, self.status,
            self.universe, self.horizon,self.author,self.freq,self.owner,
            self.derive, self.derive_universe)

class BaseIndicScore(metaclass=abc.ABCMeta):

    @property
    def name(self):
        pass

    @property
    def value(self):
        pass

    def __and__(self, rhs):
        return AndIndic(self, rhs)
    
    def encryption(self, feature):
        s = hashlib.md5(
            json.dumps(feature).encode(encoding="utf-8")).hexdigest()
        return create_id(original=s, digit=15)
        
    @property
    def id(self):
        i_obj = self.obj
        i_obj = sorted(i_obj, key=lambda x: x['name'])
        return self.encryption(i_obj)


class IndicScore(BaseIndicScore):

    def __init__(self, name, value):
        self.i_name = name
        self.i_value = value

    @property
    def name(self):
        return self.i_name

    @property
    def value(self):
        return self.i_value

    @property
    def obj(self):
        return [{'name': self.name, 'value': self.value}]



class AndIndic(BaseIndicScore):

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    @property
    def obj(self):
        unique_dict = {}
        nested_list = [self.lhs.obj, self.rhs.obj]
        nested_list = list(
            itertools.chain.from_iterable(
                sublist if isinstance(sublist, list) else [sublist]
                for sublist in nested_list))
        return [
            unique_dict.setdefault(d['name'], d) for d in nested_list
            if d['name'] not in unique_dict
        ]
