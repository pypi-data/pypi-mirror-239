# !/usr/bin/env python
# coding: utf-8
import json
import uuid

from JYTools.JYWorker import RedisQueue
from JYTools.JYWorker import RedisWorker
from JYTools.util import loader

from JYTools.util import constants


__author__ = 'zhouhenglc'


def get_func_name(func):
    if func is None:
        return
    if not callable(func):
        raise RuntimeError('function %s not callable' % func)
    func_name = '%s.%s' % (func.__module__, func.__name__)
    return func_name


def handle_one_failed_func(failed_func, **kwargs):
    status = kwargs['status']
    if status != TASK_STATUS_FAILED:
        return
    f_func = loader.load_function(failed_func)
    if not f_func:
        return
    f_func(kwargs)


def handle_completed_func(completed_func, success_func, failed_func,
                          *result, **kwargs):
    if completed_func:
        c_func = loader.load_function(completed_func)
        c_func(result)
    for r in result:
        if r['status'] != TASK_STATUS_SUCCESS:
            if not failed_func:
                return
            f_func = loader.load_function(failed_func)
            f_func(result)
            return
    s_func = loader.load_function(success_func)
    s_func(result)
    return


TASK_STATUS_SUCCESS = 'success'
TASK_STATUS_FAILED = 'failed'


class FuncTaskWorker(RedisWorker):
    expect_params_type = dict
    DEFAULT_WORK_TAG = constants.DEFAULT_FUN_TASK_TAG

    def handle_task(self, key, params):
        if 'func' not in params:
            self.set_current_task_invalid('Need func')
        exec_args = params.get('exec_args', [])
        exec_kwargs = params.get('exec_kwargs', {})
        reload = params.get('reload', False)
        exception = None
        _func_name = params['func']
        self.task_log('exec args is: ', *exec_args)
        try:
            _func = loader.load_function(_func_name, reload)
            r = _func(*exec_args, **exec_kwargs)
            status = TASK_STATUS_SUCCESS
        except Exception as e:
            status = TASK_STATUS_FAILED
            self.task_exception_log()
            exception = {'msg': str(e), 'type': e.__class__.__name__}
            r = None
        exec_result = {'status': status, 'exception': exception,
                       'func_return': r, 'exec_args': exec_args,
                       'exec_kwargs': exec_kwargs}
        self.set_output("exec_result", exec_result)


class FuncTaskGroup(object):

    def __init__(self, group_id, completed_func=None, failed_func=None,
                 success_func=None, any_failed_func=None, func_task_tag=None,
                 pipeline_tag=None, redis_host=None, redis_password=None,
                 redis_port=None, redis_db=None, redis_man=None):
        if group_id is None:
            group_id = 'atg-%s' % str(uuid.uuid4())
        self.group_id = group_id
        self.func_task_tag = func_task_tag or constants.DEFAULT_FUN_TASK_TAG
        self.pipeline_tag = pipeline_tag or constants.DEFAULT_PIPELINE_TAG
        self._internal_id = 'iatg-%s' % str(uuid.uuid4())
        self.completed_func = get_func_name(completed_func)
        self.failed_func = get_func_name(failed_func)
        self.success_func = get_func_name(success_func)
        self.any_failed_func = get_func_name(any_failed_func)
        self.tasks = []
        self.started = False
        queue_kwargs = {'redis_host': redis_host, 'redis_port': redis_port,
                        'redis_password': redis_password,
                        'redis_db': redis_db, 'redis_man': redis_man,
                        'work_tag': self.pipeline_tag}
        self.r_queue = RedisQueue(**queue_kwargs)

    def add_sync_task(self, func, *args, **kwargs):
        func_name = get_func_name(func)
        params = {'work_tag':  self.func_task_tag,
                  'input_exec_args': list(args),
                  'input_exec_kwargs': kwargs,
                  'input_func': func_name}

        self.tasks.append(params)

    def start(self):
        if self.started:
            return
        self.started = True
        task_list = self.tasks
        task_len = len(self.tasks)
        if self.any_failed_func:
            for i in range(task_len):
                task = {'work_tag':  self.func_task_tag,
                        'input_func': get_func_name(handle_one_failed_func),
                        'input_exec_args': [self.any_failed_func],
                        'input_exec_kwargs': '&%sexec_result' % (i+1)}
                task_list.append(task)
        c_task = {'work_tag':  self.func_task_tag,
                  'input_func': get_func_name(handle_completed_func),
                  'input_exec_args': [self.completed_func, self.success_func,
                                      self.failed_func],
                  'input_exec_kwargs': {}}
        c_task['input_exec_args'].extend(
            ['&%sexec_result' % (i+1) for i in range(task_len)])
        task_list.append(c_task)
        key = '%s-%s' % (self.group_id, self._internal_id)
        params = {'task_list': task_list}
        self.r_queue.push(key, params=params)


def run_fun_task(redis_queue, key, func, *args, **kwargs):
    work_tag = redis_queue.work_tag or constants.DEFAULT_FUN_TASK_TAG
    params = {'exec_args': list(args), 'exec_kwargs': kwargs,
              'func': get_func_name(func), 'reload': False}
    redis_queue.push(key, params, work_tag=work_tag)
