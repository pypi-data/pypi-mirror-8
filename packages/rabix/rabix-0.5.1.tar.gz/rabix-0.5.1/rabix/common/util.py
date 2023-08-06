import random
import itertools
import collections
import logging
import six

from rabix.common.errors import RabixError

log = logging.getLogger(__name__)


def wrap_in_list(val, *append_these):
    """
    >>> wrap_in_list(1, 2)
    [1, 2]
    >>> wrap_in_list([1, 2], 3, 4)
    [1, 2, 3, 4]
    >>> wrap_in_list([1, 2], [3, 4])
    [1, 2, [3, 4]]
    """
    wrapped = val if isinstance(val, list) else [val]
    return wrapped + list(append_these)


def import_name(name):
    name = str(name)
    if '.' not in name:
        return __import__(name)
    chunks = name.split('.')
    var_name = chunks[-1]
    module_name = '.'.join(chunks[:-1])
    fromlist = chunks[:-2] if len(chunks) > 2 else []
    module = __import__(module_name, fromlist=fromlist)
    if not hasattr(module, var_name):
        raise ImportError('%s not found in %s' % (var_name, module_name))
    return getattr(module, var_name)


def dot_update_dict(dst, src):
    for key, val in six.iteritems(src):
        t = dst
        if '.' in key:
            for k in key.split('.'):
                if k == key.split('.')[-1]:
                    if isinstance(val, collections.Mapping):
                        t = t.setdefault(k, {})
                        dot_update_dict(t, src[key])
                    else:
                        t[k] = val
                else:
                    if not isinstance(t.get(k), collections.Mapping):
                        t[k] = {}
                    t = t.setdefault(k, {})
        else:
            if isinstance(val, collections.Mapping):
                t = t.setdefault(key, {})
                dot_update_dict(t, src[key])
            else:
                t[key] = val
    return dst


def rnd_name(syllables=5):
    return ''.join(itertools.chain(*zip(
        (random.choice('bcdfghjklmnpqrstvwxz') for _ in range(syllables)),
        (random.choice('aeiouy') for _ in range(syllables)))))


def log_level(int_level):
    if int_level <= 0:
        level = logging.WARN
    elif int_level == 1:
        level = logging.INFO
    elif int_level >= 2:
        level = logging.DEBUG
    else:
        raise RabixError("Invalid log level: %s" % int_level)
    return level


def sec_files_naming_conv(path, ext):
    return ''.join([path, ext]) if ext.startswith('.') \
        else '.'.join(['.'.join(path.split('.')[:-1]), ext])
