# encoding: utf-8

import os
import hashlib
import functools

import dill
import multiprocessing

from .std_logger import get_logger
from .serializer import serialize_tuple, unserialize_tuple


class CacheItem(object):

    def __init__(self, file_name, value, origin, loaded):
        self.file_name = file_name
        self.value = value
        self.origin = origin
        self.loaded = loaded

    def __str__(self):
        return str(self.value)


class CacheBuilder(object):

    def __init__(self, root_dir=None, keep_in_memory=True):
        self.root_dir = root_dir
        self.keep_in_memory = keep_in_memory
        self._manager = multiprocessing.Manager()
        self.reset_handlers()

    def reset_handlers(self):
        self._type_handlers = list()

    def register_handler(self, type_, hash_function, file_extension, load_function, save_function,
                         get_origin_function, set_origin_function):
        self._type_handlers.append((type_,
                                    dill.dumps(hash_function),
                                    file_extension,
                                    dill.dumps(load_function),
                                    dill.dumps(save_function),
                                    dill.dumps(get_origin_function),
                                    dill.dumps(set_origin_function),
                                    )
                                   )

    def __call__(self, function):
        folder = function.__name__
        if self.root_dir is not None:
            folder = os.path.join(self.root_dir, folder)

        cache = self._manager.dict()
        lock = self._manager.Lock()
        counter = self._manager.Value('d', 0)
        handlers = self._manager.list(self._type_handlers)

        c = _CachedFunction(function, folder, self.keep_in_memory, lock, cache, counter, handlers)
        return c


class _CachedFunction(object):

    """ Instances of this class can be used to decorate function calls for caching their
    results, even if the functions are executed across different processes started by Python
    multiprocessing modules Pool class.

    The cache is backed up on disk, so that cache entries are persisted over different
    runs.
    """

    def __init__(self, function, folder, _keep_in_memory, _lock, _cache, _counter, _handlers):

        self.function = function
        self.__name__ = function.__name__
        self.folder = folder
        self._keep_in_memory = _keep_in_memory

        self._cache = _cache
        self._lock = _lock
        self._hit_counter = _counter
        self._type_handlers = _handlers
        self._logger = get_logger(self)
        self._setup_cache()

    def reset_handlers(self):
        del self._type_handlers[:]

    def register_handler(self, type_, hash_function, file_extension, load_function, save_function,
                         get_origin_function, set_origin_function):
        self._type_handlers.append((type_,
                                    dill.dumps(hash_function),
                                    file_extension,
                                    dill.dumps(load_function),
                                    dill.dumps(save_function),
                                    dill.dumps(get_origin_function),
                                    dill.dumps(set_origin_function),
                                    )
                                   )

    def _lookup_for_type_of(self, obj):
        for row in self._type_handlers:
            if isinstance(obj, row[0]):
                return row
        nonf = dill.dumps(None)
        return [None, nonf, None, nonf, nonf, nonf, nonf]

    def _lookup_hash_function_for(self, key):
        return dill.loads(self._lookup_for_type_of(key)[1])

    def _lookup_load_function_for(self, ext):
        for (__, __, ext_i, load_function, __, __, __) in self._type_handlers:
            if ext == ext_i:
                return dill.loads(load_function)
        return None

    def _lookup_ext_and_save_function_for(self, what):
        row = self._lookup_for_type_of(what)
        return row[2], dill.loads(row[4])

    def _lookup_get_origin_function(self, what):
        return dill.loads(self._lookup_for_type_of(what)[5])

    def _lookup_set_origin_function(self, what):
        return dill.loads(self._lookup_for_type_of(what)[6])

    def get_number_of_hits(self):
        return self._hit_counter.value

    def _setup_cache(self):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        for file_name in os.listdir(self.folder):
            stem, ext = os.path.splitext(file_name)
            hash_code, __, origin_str = stem.partition("--")
            origin = unserialize_tuple(origin_str)
            self._cache[hash_code] = CacheItem(file_name, None, origin, False)

    def clear(self):
        self._cache.clear()

    def _compute_hash(self, key):
        hash_fun = self._lookup_hash_function_for(key)
        if hash_fun is not None:
            return hash_fun(key)
        if isinstance(key, (tuple, list)):
            data = "".join(self._compute_hash(item) for item in key)
        elif isinstance(key, set):
            data = "".join(self._compute_hash(item) for item in sorted(key))
        elif isinstance(key, dict):
            data = "".join(self._compute_hash(item) for item in key.items())
        elif isinstance(key, basestring):
            data = key
        elif hasattr(key, "__dict__"):
            data = dill.dumps(key.__dict__)
        elif isinstance(key, (bool, int, long, float,)):
            data = dill.dumps(key)
        else:
            raise Exception("can not compute hash for %r" % (key,))
        muncher = hashlib.sha1()
        muncher.update(data)
        return muncher.hexdigest()

    def _contains(self, hash_code):
        return hash_code in self._cache.keys()

    def _get(self, hash_code):
        item = self._cache[hash_code]
        if not item.loaded:
            value = self._load(item.file_name)
            item.value = self._set_origin(value, item.origin)
            item.loaded = True
            self._cache[hash_code] = item
        return item.value

    def _put(self, hash_code_args, args, result, origin):
        try:
            origin_str = serialize_tuple(origin).replace("/", "%")
        except Exception, e:
            raise Exception("can not pickle %r beause of:\n%s" % (e.message,))

        if len(origin_str) > 100:
            origin_str = "[TOO_LONG]"
        path = self._store(result, hash_code_args + "--" + origin_str)
        if self._keep_in_memory:
            self._cache[hash_code_args] = CacheItem(None, result, origin, True)
        else:
            self._cache[hash_code_args] = CacheItem(path, None, origin, False)

    def _load(self, file_name):
        path = os.path.join(self.folder, file_name)
        stem, f_ext = os.path.splitext(file_name)
        load_function = self._lookup_load_function_for(f_ext)
        if load_function is not None:
            obj = load_function(path)
        else:
            obj = dill.load(open(path, "rb"))
        self._logger.info("loaded %s" % path)
        return obj

    def _store(self, what, stem):
        ext, save_function = self._lookup_ext_and_save_function_for(what)
        if ext is not None and save_function is not None:
            path = os.path.join(self.folder, stem + ext)
            save_function(what, path)
        else:
            path = os.path.join(self.folder, stem + ".pickled")
            with open(path, "wb") as fp:
                dill.dump(what, fp)
        self._logger.info("stored %s" % path)
        return path

    def _get_origin(self, arg):
        get_origin = self._lookup_get_origin_function(arg)
        if get_origin is not None:
            return get_origin(arg)
        if isinstance(arg, (tuple, list)):
            return tuple(self._get_origin(item) for item in arg)
        elif isinstance(arg, basestring):
            return arg
        elif isinstance(arg, (int, bool, float)):
            return str(arg)
        elif isinstance(arg, dict):
            return "dict(%d)" % len(arg)
        elif isinstance(arg, set):
            return "set(%d)" % len(arg)
        else:
            return "XXX"

    def _set_origin(self, obj, origin):
        set_origin = self._lookup_set_origin_function(obj)
        if set_origin is not None:
            return set_origin(obj, origin)
        return obj

    def __call__(self, *args):
        hash_code = self._compute_hash(args)
        if self._contains(hash_code):
            with self._lock:
                self._hit_counter.value += 1
            self._logger.info("cache hit for %s" % hash_code)
            return self._get(hash_code)
        result = self.function(*args)
        origin = self._get_origin(args)
        result = self._set_origin(result, origin)
        self._logger.info("new result for %s" % hash_code)
        self._put(hash_code, args, result, origin)
        return result
