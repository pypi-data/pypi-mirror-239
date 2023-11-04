import datetime
import functools
import logging
import multiprocessing
import multiprocessing.pool
import time
from _collections_abc import dict_keys, dict_values, Iterable
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import product
from multiprocessing import get_context
from tqdm import tqdm
from typing import Dict, List, Set, Tuple, Optional, Union, Callable, Type


class ProcessPoolExecutorZx(object):
    """"""

    @classmethod
    def as_completed(cls, fs, timeout=None):
        """"""
        fs = set(fs)

        while fs:
            lines: list = []

            for rslt in fs:
                rslt: ProcessPoolExecutorZx._Result = rslt
                if rslt._apply_result.ready():
                    lines.append(rslt)

            for rslt in lines:
                yield rslt
                fs.discard(rslt)

            if not lines:
                time.sleep(0.001)

    class _Result(object):
        """"""

        def __init__(self, apply_result: multiprocessing.pool.ApplyResult) -> None:
            """"""
            self._apply_result: multiprocessing.pool.ApplyResult = apply_result

        def result(self):
            """"""
            self._apply_result.get()

    class _Item(object):
        """"""

        def __init__(self, fn, args, kwargs, rslt, exc):
            """"""
            self.fn = fn
            self.args = args
            self.kwargs = kwargs
            self.rslt = rslt  # _callback 返回过来的数据,
            self.exc = exc  # _error_callback 返回过来的数据,

    def __enter__(self):
        """"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """"""
        self.shutdown()
        return False

    def __init__(self, max_workers=None, *args, **kwargs):
        """"""
        assert isinstance(max_workers, (type(None), int))
        self._pool = multiprocessing.Pool(processes=max_workers)

    def _callback(self, fn, args, kwargs, rslt):
        """"""
        item = self._Item(fn=fn, args=args, kwargs=kwargs, rslt=rslt, exc=None)

    def _error_callback(self, fn, args, kwargs, exc):
        """"""
        item = self._Item(fn=fn, args=args, kwargs=kwargs, rslt=None, exc=exc)

    def map(self, fn, *iterables, timeout=None, chunksize=1):
        """"""
        fs = [self.submit(fn, *args) for args in zip(*iterables)]
        for future in self.as_completed(fs=fs, timeout=timeout):
            yield future

    def submit(self, fn, /, *args, **kwargs):
        """"""
        apply_result: multiprocessing.pool.ApplyResult = self._pool.apply_async(
            func=fn,
            args=args,
            kwds=kwargs,
            callback=functools.partial(self._callback, fn, args, kwargs),
            error_callback=functools.partial(
                self._error_callback, fn, args, kwargs),
        )
        result = self._Result(apply_result=apply_result)
        return result

    def shutdown(self, wait=True, *, cancel_futures=False):
        """"""
        self._pool.close()
        self._pool.join()


def __main_function():
    """"""

    def evaluate_func(setting: dict):
        """"""
        if 0:
            print(datetime.datetime.now(), setting)
        return setting

    def generate_settings() -> List[dict]:
        """"""
        params: Dict[str, list] = {}
        params["field_1"] = [*range(2, 241, 1)]
        params["field_2"] = [*range(2, 241, 1)]
        params["field_3"] = [*range(1, 241, 1)]

        keys: dict_keys = params.keys()
        values: dict_values = params.values()
        products: list = list(product(*values))

        settings: list = []
        for p in products:
            setting: dict = dict(zip(keys, p))
            settings.append(setting)

        return settings

    settings: List[dict] = generate_settings()

    logging.info(f"len_settings={len(settings)}")

    with ProcessPoolExecutorZx(
        max_workers=None,
        mp_context=get_context("spawn")
    ) as executor:
        logging.info(f"type_executor={type(executor)}")

        if 1:
            it: Iterable = tqdm(
                executor.map(evaluate_func, settings),
                total=len(settings)
            )
            results: List[Tuple] = list(it)

        else:
            # 使用concurrent.futures的一些经验
            # https://www.dongwm.com/post/use-concurrent-futures/
            fs = {executor.submit(evaluate_func, setting): setting for setting in settings}

            results: List[Tuple] = []
            for future in as_completed(fs):
                del fs[future]
                results.append(future.result())

                len_finished: int = len(settings) - len(fs)
                if len_finished % 1000 == 0:
                    logging.info(f"progress: {len_finished}/{len(settings)}")

        logging.info(f"len_results={len(results)}, len_settings={len(settings)},")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(message)s")

    __main_function()
