# This file was automatically generated by SWIG (http://www.swig.org).
# Version 2.0.7
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.



from sys import version_info
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_Mistral', [dirname(__file__)])
        except ImportError:
            import _Mistral
            return _Mistral
        if fp is not None:
            try:
                _mod = imp.load_module('_Mistral', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _Mistral = swig_import_helper()
    del swig_import_helper
else:
    import _Mistral
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


def _swig_setattr_nondynamic_method(set):
    def set_attr(self,name,value):
        if (name == "thisown"): return self.this.own(value)
        if hasattr(self,name) or (name == "this"):
            set(self,name,value)
        else:
            raise AttributeError("You cannot add attributes to %s" % self)
    return set_attr


class VarValuation(object):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    value = _swig_property(_Mistral.VarValuation_value_get, _Mistral.VarValuation_value_set)
    type = _swig_property(_Mistral.VarValuation_type_get, _Mistral.VarValuation_type_set)
    def __init__(self, *args): 
        this = _Mistral.new_VarValuation(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_VarValuation
    __del__ = lambda self : None;
VarValuation_swigregister = _Mistral.VarValuation_swigregister
VarValuation_swigregister(VarValuation)

class Mistral_Expression(object):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    nbj_ident = _swig_property(_Mistral.Mistral_Expression_nbj_ident_get, _Mistral.Mistral_Expression_nbj_ident_set)
    _solver = _swig_property(_Mistral.Mistral_Expression__solver_get, _Mistral.Mistral_Expression__solver_set)
    _self = _swig_property(_Mistral.Mistral_Expression__self_get, _Mistral.Mistral_Expression__self_set)
    def has_been_added(self): return _Mistral.Mistral_Expression_has_been_added(self)
    def initialise(self): return _Mistral.Mistral_Expression_initialise(self)
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_Expression(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_Expression
    __del__ = lambda self : None;
    def get_type(self): return _Mistral.Mistral_Expression_get_type(self)
    def get_arity(self): return _Mistral.Mistral_Expression_get_arity(self)
    def get_child(self, *args): return _Mistral.Mistral_Expression_get_child(self, *args)
    def get_id(self): return _Mistral.Mistral_Expression_get_id(self)
    def next(self, *args): return _Mistral.Mistral_Expression_next(self, *args)
    def getVariableId(self): return _Mistral.Mistral_Expression_getVariableId(self)
    def get_value(self): return _Mistral.Mistral_Expression_get_value(self)
    def get_size(self): return _Mistral.Mistral_Expression_get_size(self)
    def get_min(self): return _Mistral.Mistral_Expression_get_min(self)
    def get_max(self): return _Mistral.Mistral_Expression_get_max(self)
    def contain(self, *args): return _Mistral.Mistral_Expression_contain(self, *args)
    def add(self, *args): return _Mistral.Mistral_Expression_add(self, *args)
    def print_python(self): return _Mistral.Mistral_Expression_print_python(self)
Mistral_Expression_swigregister = _Mistral.Mistral_Expression_swigregister
Mistral_Expression_swigregister(Mistral_Expression)

class Mistral_IntVar(Mistral_Expression):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_IntVar(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_IntVar
    __del__ = lambda self : None;
Mistral_IntVar_swigregister = _Mistral.Mistral_IntVar_swigregister
Mistral_IntVar_swigregister(Mistral_IntVar)

class Mistral_Neg(Mistral_Expression):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_Neg(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_Neg
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_Neg_add(self, *args)
Mistral_Neg_swigregister = _Mistral.Mistral_Neg_swigregister
Mistral_Neg_swigregister(Mistral_Neg)

class Mistral_Min(Mistral_Expression):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_Min(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_Min
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_Min_add(self, *args)
Mistral_Min_swigregister = _Mistral.Mistral_Min_swigregister
Mistral_Min_swigregister(Mistral_Min)

class Mistral_Max(Mistral_Expression):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_Max(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_Max
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_Max_add(self, *args)
Mistral_Max_swigregister = _Mistral.Mistral_Max_swigregister
Mistral_Max_swigregister(Mistral_Max)

class Mistral_AllDiff(Mistral_Expression):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_AllDiff(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_AllDiff
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_AllDiff_add(self, *args)
Mistral_AllDiff_swigregister = _Mistral.Mistral_AllDiff_swigregister
Mistral_AllDiff_swigregister(Mistral_AllDiff)

class Mistral_Table(Mistral_Expression):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_Table(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_Table
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_Table_add(self, *args)
Mistral_Table_swigregister = _Mistral.Mistral_Table_swigregister
Mistral_Table_swigregister(Mistral_Table)

class Mistral_Gcc(Mistral_Expression):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_Gcc(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_Gcc
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_Gcc_add(self, *args)
Mistral_Gcc_swigregister = _Mistral.Mistral_Gcc_swigregister
Mistral_Gcc_swigregister(Mistral_Gcc)

class Mistral_Element(Mistral_Expression):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_Element(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_Element
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_Element_add(self, *args)
Mistral_Element_swigregister = _Mistral.Mistral_Element_swigregister
Mistral_Element_swigregister(Mistral_Element)

class Mistral_LeqLex(Mistral_Expression):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_LeqLex(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_LeqLex
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_LeqLex_add(self, *args)
Mistral_LeqLex_swigregister = _Mistral.Mistral_LeqLex_swigregister
Mistral_LeqLex_swigregister(Mistral_LeqLex)

class Mistral_LessLex(Mistral_Expression):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_LessLex(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_LessLex
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_LessLex_add(self, *args)
Mistral_LessLex_swigregister = _Mistral.Mistral_LessLex_swigregister
Mistral_LessLex_swigregister(Mistral_LessLex)

class Mistral_Sum(Mistral_Expression):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_Sum(*args)
        try: self.this.append(this)
        except: self.this = this
    def addVar(self, *args): return _Mistral.Mistral_Sum_addVar(self, *args)
    def addWeight(self, *args): return _Mistral.Mistral_Sum_addWeight(self, *args)
    __swig_destroy__ = _Mistral.delete_Mistral_Sum
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_Sum_add(self, *args)
Mistral_Sum_swigregister = _Mistral.Mistral_Sum_swigregister
Mistral_Sum_swigregister(Mistral_Sum)

class Mistral_binop(Mistral_Expression):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    def __init__(self, *args, **kwargs): raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    def arity(self): return _Mistral.Mistral_binop_arity(self)
    __swig_destroy__ = _Mistral.delete_Mistral_binop
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_binop_add(self, *args)
Mistral_binop_swigregister = _Mistral.Mistral_binop_swigregister
Mistral_binop_swigregister(Mistral_binop)

class Mistral_mul(Mistral_binop):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_mul(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_mul
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_mul_add(self, *args)
Mistral_mul_swigregister = _Mistral.Mistral_mul_swigregister
Mistral_mul_swigregister(Mistral_mul)

class Mistral_div(Mistral_binop):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_div(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_div
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_div_add(self, *args)
Mistral_div_swigregister = _Mistral.Mistral_div_swigregister
Mistral_div_swigregister(Mistral_div)

class Mistral_mod(Mistral_binop):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_mod(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_mod
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_mod_add(self, *args)
Mistral_mod_swigregister = _Mistral.Mistral_mod_swigregister
Mistral_mod_swigregister(Mistral_mod)

class Mistral_and(Mistral_binop):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_and(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_and
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_and_add(self, *args)
Mistral_and_swigregister = _Mistral.Mistral_and_swigregister
Mistral_and_swigregister(Mistral_and)

class Mistral_or(Mistral_binop):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_or(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_or
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_or_add(self, *args)
Mistral_or_swigregister = _Mistral.Mistral_or_swigregister
Mistral_or_swigregister(Mistral_or)

class Mistral_eq(Mistral_binop):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_eq(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_eq
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_eq_add(self, *args)
Mistral_eq_swigregister = _Mistral.Mistral_eq_swigregister
Mistral_eq_swigregister(Mistral_eq)

class Mistral_ne(Mistral_binop):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_ne(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_ne
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_ne_add(self, *args)
Mistral_ne_swigregister = _Mistral.Mistral_ne_swigregister
Mistral_ne_swigregister(Mistral_ne)

class Mistral_NoOverlap(Mistral_binop):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_NoOverlap(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_NoOverlap
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_NoOverlap_add(self, *args)
Mistral_NoOverlap_swigregister = _Mistral.Mistral_NoOverlap_swigregister
Mistral_NoOverlap_swigregister(Mistral_NoOverlap)

class Mistral_Precedence(Mistral_binop):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_Precedence(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_Precedence
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_Precedence_add(self, *args)
Mistral_Precedence_swigregister = _Mistral.Mistral_Precedence_swigregister
Mistral_Precedence_swigregister(Mistral_Precedence)

class Mistral_le(Mistral_binop):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_le(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_le
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_le_add(self, *args)
Mistral_le_swigregister = _Mistral.Mistral_le_swigregister
Mistral_le_swigregister(Mistral_le)

class Mistral_ge(Mistral_binop):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_ge(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_ge
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_ge_add(self, *args)
Mistral_ge_swigregister = _Mistral.Mistral_ge_swigregister
Mistral_ge_swigregister(Mistral_ge)

class Mistral_lt(Mistral_binop):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_lt(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_lt
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_lt_add(self, *args)
Mistral_lt_swigregister = _Mistral.Mistral_lt_swigregister
Mistral_lt_swigregister(Mistral_lt)

class Mistral_gt(Mistral_binop):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_gt(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_gt
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_gt_add(self, *args)
Mistral_gt_swigregister = _Mistral.Mistral_gt_swigregister
Mistral_gt_swigregister(Mistral_gt)

class Mistral_Minimise(Mistral_Expression):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_Minimise(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_Minimise
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_Minimise_add(self, *args)
Mistral_Minimise_swigregister = _Mistral.Mistral_Minimise_swigregister
Mistral_Minimise_swigregister(Mistral_Minimise)

class Mistral_Maximise(Mistral_Expression):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _Mistral.new_Mistral_Maximise(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_Mistral_Maximise
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.Mistral_Maximise_add(self, *args)
Mistral_Maximise_swigregister = _Mistral.Mistral_Maximise_swigregister
Mistral_Maximise_swigregister(Mistral_Maximise)

class MistralSolver(object):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    solver = _swig_property(_Mistral.MistralSolver_solver_get, _Mistral.MistralSolver_solver_set)
    model = _swig_property(_Mistral.MistralSolver_model_get, _Mistral.MistralSolver_model_set)
    feature_ready = _swig_property(_Mistral.MistralSolver_feature_ready_get, _Mistral.MistralSolver_feature_ready_set)
    is_copy = _swig_property(_Mistral.MistralSolver_is_copy_get, _Mistral.MistralSolver_is_copy_set)
    nogood_base = _swig_property(_Mistral.MistralSolver_nogood_base_get, _Mistral.MistralSolver_nogood_base_set)
    valuation = _swig_property(_Mistral.MistralSolver_valuation_get, _Mistral.MistralSolver_valuation_set)
    valuation_size = _swig_property(_Mistral.MistralSolver_valuation_size_get, _Mistral.MistralSolver_valuation_size_set)
    decisions = _swig_property(_Mistral.MistralSolver_decisions_get, _Mistral.MistralSolver_decisions_set)
    graph = _swig_property(_Mistral.MistralSolver_graph_get, _Mistral.MistralSolver_graph_set)
    first_decision_level = _swig_property(_Mistral.MistralSolver_first_decision_level_get, _Mistral.MistralSolver_first_decision_level_set)
    saved_level = _swig_property(_Mistral.MistralSolver_saved_level_get, _Mistral.MistralSolver_saved_level_set)
    def __init__(self): 
        this = _Mistral.new_MistralSolver()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_MistralSolver
    __del__ = lambda self : None;
    def add(self, *args): return _Mistral.MistralSolver_add(self, *args)
    def get_expression(self, *args): return _Mistral.MistralSolver_get_expression(self, *args)
    def num_expression(self): return _Mistral.MistralSolver_num_expression(self)
    def max_expression_id(self): return _Mistral.MistralSolver_max_expression_id(self)
    def initialise(self, *args): return _Mistral.MistralSolver_initialise(self, *args)
    def solve(self): return _Mistral.MistralSolver_solve(self)
    def solveAndRestart(self, *args): return _Mistral.MistralSolver_solveAndRestart(self, *args)
    def startNewSearch(self): return _Mistral.MistralSolver_startNewSearch(self)
    def getNextSolution(self): return _Mistral.MistralSolver_getNextSolution(self)
    def sacPreprocess(self, *args): return _Mistral.MistralSolver_sacPreprocess(self, *args)
    def get_level(self): return _Mistral.MistralSolver_get_level(self)
    def get_decision_id(self): return _Mistral.MistralSolver_get_decision_id(self)
    def propagate(self): return _Mistral.MistralSolver_propagate(self)
    def save(self): return _Mistral.MistralSolver_save(self)
    def post(self, *args): return _Mistral.MistralSolver_post(self, *args)
    def undo(self, *args): return _Mistral.MistralSolver_undo(self, *args)
    def deduce(self, *args): return _Mistral.MistralSolver_deduce(self, *args)
    def branch_right(self): return _Mistral.MistralSolver_branch_right(self)
    def store_solution(self): return _Mistral.MistralSolver_store_solution(self)
    def setHeuristic(self, *args): return _Mistral.MistralSolver_setHeuristic(self, *args)
    def setAntiLex(self, *args): return _Mistral.MistralSolver_setAntiLex(self, *args)
    def setFailureLimit(self, *args): return _Mistral.MistralSolver_setFailureLimit(self, *args)
    def setNodeLimit(self, *args): return _Mistral.MistralSolver_setNodeLimit(self, *args)
    def setTimeLimit(self, *args): return _Mistral.MistralSolver_setTimeLimit(self, *args)
    def setVerbosity(self, *args): return _Mistral.MistralSolver_setVerbosity(self, *args)
    def setRandomized(self, *args): return _Mistral.MistralSolver_setRandomized(self, *args)
    def setRandomSeed(self, *args): return _Mistral.MistralSolver_setRandomSeed(self, *args)
    def forceFiniteDomain(self, *args): return _Mistral.MistralSolver_forceFiniteDomain(self, *args)
    def addNogood(self, *args): return _Mistral.MistralSolver_addNogood(self, *args)
    def guide(self, *args): return _Mistral.MistralSolver_guide(self, *args)
    def backtrackTo(self, *args): return _Mistral.MistralSolver_backtrackTo(self, *args)
    def upOneLevel(self): return _Mistral.MistralSolver_upOneLevel(self)
    def presolve(self): return _Mistral.MistralSolver_presolve(self)
    def assign(self, *args): return _Mistral.MistralSolver_assign(self, *args)
    def increase_init_level(self, *args): return _Mistral.MistralSolver_increase_init_level(self, *args)
    def decrease_init_level(self, *args): return _Mistral.MistralSolver_decrease_init_level(self, *args)
    def reset(self, *args): return _Mistral.MistralSolver_reset(self, *args)
    def setLowerBounds(self, *args): return _Mistral.MistralSolver_setLowerBounds(self, *args)
    def setUpperBounds(self, *args): return _Mistral.MistralSolver_setUpperBounds(self, *args)
    def setRestartNogood(self): return _Mistral.MistralSolver_setRestartNogood(self)
    def is_opt(self): return _Mistral.MistralSolver_is_opt(self)
    def is_sat(self): return _Mistral.MistralSolver_is_sat(self)
    def is_unsat(self): return _Mistral.MistralSolver_is_unsat(self)
    def printStatistics(self): return _Mistral.MistralSolver_printStatistics(self)
    def getBacktracks(self): return _Mistral.MistralSolver_getBacktracks(self)
    def getNodes(self): return _Mistral.MistralSolver_getNodes(self)
    def getFailures(self): return _Mistral.MistralSolver_getFailures(self)
    def getChecks(self): return _Mistral.MistralSolver_getChecks(self)
    def getPropags(self): return _Mistral.MistralSolver_getPropags(self)
    def getTime(self): return _Mistral.MistralSolver_getTime(self)
    def getRandomNumber(self): return _Mistral.MistralSolver_getRandomNumber(self)
    def getNumVariables(self): return _Mistral.MistralSolver_getNumVariables(self)
    def getNumConstraints(self): return _Mistral.MistralSolver_getNumConstraints(self)
    def test_x60(self): return _Mistral.MistralSolver_test_x60(self)
    def printPython(self): return _Mistral.MistralSolver_printPython(self)
    def load_xml(self, *args): return _Mistral.MistralSolver_load_xml(self, *args)
    def get_feature_name(self, *args): return _Mistral.MistralSolver_get_feature_name(self, *args)
    def get_feature(self, *args): return _Mistral.MistralSolver_get_feature(self, *args)
    def get_features(self, *args): return _Mistral.MistralSolver_get_features(self, *args)
    def num_vars(self): return _Mistral.MistralSolver_num_vars(self)
    def get_degree(self, *args): return _Mistral.MistralSolver_get_degree(self, *args)
    def extract_graph(self): return _Mistral.MistralSolver_extract_graph(self)
    def numNodes(self): return _Mistral.MistralSolver_numNodes(self)
    def degree(self, *args): return _Mistral.MistralSolver_degree(self, *args)
    def get_neighbor(self, *args): return _Mistral.MistralSolver_get_neighbor(self, *args)
MistralSolver_swigregister = _Mistral.MistralSolver_swigregister
MistralSolver_swigregister(MistralSolver)

class MistralExpArray(object):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self): 
        this = _Mistral.new_MistralExpArray()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_MistralExpArray
    __del__ = lambda self : None;
    def size(self): return _Mistral.MistralExpArray_size(self)
    def add(self, *args): return _Mistral.MistralExpArray_add(self, *args)
    def get_item(self, *args): return _Mistral.MistralExpArray_get_item(self, *args)
    def set_item(self, *args): return _Mistral.MistralExpArray_set_item(self, *args)
MistralExpArray_swigregister = _Mistral.MistralExpArray_swigregister
MistralExpArray_swigregister(MistralExpArray)

class MistralIntArray(object):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self): 
        this = _Mistral.new_MistralIntArray()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_MistralIntArray
    __del__ = lambda self : None;
    def size(self): return _Mistral.MistralIntArray_size(self)
    def add(self, *args): return _Mistral.MistralIntArray_add(self, *args)
    def get_item(self, *args): return _Mistral.MistralIntArray_get_item(self, *args)
    def set_item(self, *args): return _Mistral.MistralIntArray_set_item(self, *args)
MistralIntArray_swigregister = _Mistral.MistralIntArray_swigregister
MistralIntArray_swigregister(MistralIntArray)

class MistralDoubleArray(object):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self): 
        this = _Mistral.new_MistralDoubleArray()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _Mistral.delete_MistralDoubleArray
    __del__ = lambda self : None;
    def size(self): return _Mistral.MistralDoubleArray_size(self)
    def add(self, *args): return _Mistral.MistralDoubleArray_add(self, *args)
    def get_item(self, *args): return _Mistral.MistralDoubleArray_get_item(self, *args)
    def set_item(self, *args): return _Mistral.MistralDoubleArray_set_item(self, *args)
MistralDoubleArray_swigregister = _Mistral.MistralDoubleArray_swigregister
MistralDoubleArray_swigregister(MistralDoubleArray)

import Numberjack

class Solver(Numberjack.NBJ_STD_Solver):
    def __init__(self, model=None, X=None, FD=False, clause_limit=-1, encoding=None):
        Numberjack.NBJ_STD_Solver.__init__(self, "Mistral", "Mistral", model, X, FD, clause_limit, encoding)



