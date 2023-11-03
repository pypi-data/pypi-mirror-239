import dataclasses
import enum
import functools
import inspect


class _AdviceType(enum.Enum):
    BEFORE = 0
    AROUND = 1
    AFTER = 2
    ERROR = 3


def _create_advices_dict():
    return {advice_type: [] for advice_type in _AdviceType}


@dataclasses.dataclass
class _Aspect():
    _advices : dict = dataclasses.field(default_factory=_create_advices_dict)

    def add(self, advice, advice_type, id):
        self._advices[advice_type].append((id, advice))

    def remove(self, id):
        for lst in self._advices.values():
            if id is None:
                lst.clear()
            else:
                lst[:] = list(filter(lambda v: v[0] != id, lst))

    def get(self, advice_type):
        return self._advices[advice_type]


def _has_aspect(func):
    return hasattr(func, '_aspect')


def _woven(func, aspect, args, kwargs):

    #before
    for id, advice in aspect.get(_AdviceType.BEFORE):
        returned = advice(args, kwargs)
        if returned is None:
            return None
        else:
            args, kwargs = returned

    #around
    funcs = [advice for id, advice in aspect.get(_AdviceType.AROUND)]
    funcs.append(lambda args, kwargs: func(*args, **kwargs))
    for i in range(len(funcs) -2, -1, -1):
        funcs[i] = functools.partial(funcs[i], funcs[i+1])
    try:
        result = funcs[0](args, kwargs)

    #error
    except Exception as e:
        for id, advice in aspect.get(_AdviceType.ERROR):
            e = advice(e)
        if aspect.get(_AdviceType.ERROR):
            return e
        else:
            raise e

    #after
    for id, advice in aspect.get(_AdviceType.AFTER):
        result = advice(result)

    return result


def _add_aspect(container, func, func_name):
    if _has_aspect(func):
        return func

    aspect = _Aspect()

    woven = functools.wraps(func)(lambda *args, **kwargs: _woven(func, aspect, args, kwargs))
    woven._aspect = aspect

    setattr(container, func_name, woven)

    return woven


def _add_advice(container, func, advice, advice_type, id):
    func = _add_aspect(container, func, func.__name__)
    func._aspect.add(advice, advice_type, id)


_global_id_counter = 0
def _next_id():
    global _global_id_counter
    id = _global_id_counter
    _global_id_counter += 1
    return id


def _is_function_or_method(obj):
    return inspect.isfunction(obj) or inspect.ismethod(obj)


def _get_funcs(container):
    for name, func in inspect.getmembers(container, _is_function_or_method):
        yield func


def _weave(joinpoint, advice, advice_type):
    id = _next_id()
    
    if inspect.ismethod(joinpoint):
        _add_advice(joinpoint.__self__, joinpoint, advice, advice_type, id)

    elif inspect.isfunction(joinpoint) or inspect.isbuiltin(joinpoint):
        if joinpoint.__name__ == joinpoint.__qualname__:
            container = inspect.getmodule(joinpoint)
        else:
            container =  inspect.getmodule(joinpoint).__dict__[joinpoint.__qualname__.split('.')[0]]
        _add_advice(container, joinpoint, advice, advice_type, id)

    else:
        for attribute in _get_funcs(joinpoint):
            _add_advice(joinpoint, attribute, advice, advice_type, id)

    return id


def before(joinpoint, advice):
    return _weave(joinpoint, advice, _AdviceType.BEFORE)


def around(joinpoint, advice):
    return _weave(joinpoint, advice, _AdviceType.AROUND)


def after(joinpoint, advice):
    return _weave(joinpoint, advice, _AdviceType.AFTER)


def error(joinpoint, advice):
    return _weave(joinpoint, advice, _AdviceType.ERROR)


def remove(func, id=None):
    if _has_aspect(func):
        func._aspect.remove(id)
