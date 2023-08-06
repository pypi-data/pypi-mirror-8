#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
# Created on 2014-03-05 00:11:49


import os
import six
import time
import shutil
import logging
import logging.config
from six.moves import builtins

import click
from pyspider.database import connect_database
from pyspider.libs.utils import run_in_thread, run_in_subprocess, Get, ObjectDict

from pyspider.scheduler import Scheduler
from pyspider.fetcher.tornado_fetcher import Fetcher
from pyspider.processor import Processor
from pyspider.result import ResultWorker
from pyspider.webui.app import app


def read_config(ctx, param, value):
    if not value:
        return {}
    import json
    config = json.load(value)
    ctx.default_map = config
    return config


def connect_db(ctx, param, value):
    if not value:
        return
    return Get(lambda: connect_database(value))


def connect_rpc(ctx, param, value):
    if not value:
        return
    try:
        from six.moves import xmlrpc_client
    except ImportError:
        import xmlrpclib as xmlrpc_client
    return xmlrpc_client.ServerProxy(value, allow_none=True)


@click.group(invoke_without_command=True)
@click.option('-c', '--config', callback=read_config, type=click.File('r'),
              help='a json file with default values for subcommands. {"webui": {"port":5001}}')
@click.option('--debug', envvar='DEBUG', is_flag=True, help='debug mode')
@click.option('--queue-maxsize', envvar='QUEUE_MAXSIZE', default=100,
              help='maxsize of queue')
@click.option('--taskdb', envvar='TASKDB', callback=connect_db,
              help='database url for taskdb, default: sqlite')
@click.option('--projectdb', envvar='PROJECTDB', callback=connect_db,
              help='database url for projectdb, default: sqlite')
@click.option('--resultdb', envvar='RESULTDB', callback=connect_db,
              help='database url for resultdb, default: sqlite')
@click.option('--amqp-url', help='amqp url for rabbitmq, default: built-in Queue')
@click.option('--phantomjs-proxy', help="phantomjs proxy ip:port")
@click.option('--data-path', default='./data', help='data dir path')
@click.pass_context
def cli(ctx, **kwargs):
    """
    A powerful spider system in python.
    """
    logging.config.fileConfig(os.path.join(os.path.dirname(__file__), "logging.conf"))

    # get db from env
    for db in ('taskdb', 'projectdb', 'resultdb'):
        if kwargs[db] is not None:
            continue
        if os.environ.get('MYSQL_NAME'):
            kwargs[db] = Get(lambda db=db: connect_database('mysql+%s://%s:%s/%s' % (
                db, os.environ['MYSQL_PORT_3306_TCP_ADDR'],
                os.environ['MYSQL_PORT_3306_TCP_PORT'], db)))
        elif os.environ.get('MONGODB_NAME'):
            kwargs[db] = Get(lambda db=db: connect_database('mongodb+%s://%s:%s/%s' % (
                db, os.environ['MONGODB_PORT_27017_TCP_ADDR'],
                os.environ['MONGODB_PORT_27017_TCP_PORT'], db)))
        elif ctx.invoked_subcommand == 'bench':
            if kwargs['data_path'] == './data':
                kwargs['data_path'] += '/bench'
                shutil.rmtree(kwargs['data_path'], ignore_errors=True)
                os.mkdir(kwargs['data_path'])
            if db in ('taskdb', 'resultdb'):
                kwargs[db] = Get(lambda db=db: connect_database('sqlite+%s://' % (db)))
            else:
                kwargs[db] = Get(lambda db=db: connect_database('sqlite+%s:///%s/%s.db' % (
                    db, kwargs['data_path'], db[:-2])))
        else:
            if not os.path.exists(kwargs['data_path']):
                os.mkdir(kwargs['data_path'])
            kwargs[db] = Get(lambda db=db: connect_database('sqlite+%s:///%s/%s.db' % (
                db, kwargs['data_path'], db[:-2])))

    # queue
    if kwargs.get('amqp_url'):
        from pyspider.libs.rabbitmq import Queue
        for name in ('newtask_queue', 'status_queue', 'scheduler2fetcher',
                     'fetcher2processor', 'processor2result'):
            kwargs[name] = Get(lambda name=name: Queue(name, amqp_url=kwargs['amqp_url'],
                                                       maxsize=kwargs['queue_maxsize']))
    elif os.environ.get('RABBITMQ_NAME'):
        from pyspider.libs.rabbitmq import Queue
        amqp_url = ("amqp://guest:guest@%(RABBITMQ_PORT_5672_TCP_ADDR)s"
                    ":%(RABBITMQ_PORT_5672_TCP_PORT)s/%%2F" % os.environ)
        for name in ('newtask_queue', 'status_queue', 'scheduler2fetcher',
                     'fetcher2processor', 'processor2result'):
            kwargs[name] = Get(lambda name=name: Queue(name, amqp_url=amqp_url,
                                                       maxsize=kwargs['queue_maxsize']))
    else:
        from multiprocessing import Queue
        for name in ('newtask_queue', 'status_queue', 'scheduler2fetcher',
                     'fetcher2processor', 'processor2result'):
            kwargs[name] = Queue(kwargs['queue_maxsize'])

    # phantomjs-proxy
    if kwargs.get('phantomjs_proxy'):
        pass
    elif os.environ.get('PHANTOMJS_NAME'):
        kwargs['phantomjs_proxy'] = os.environ['PHANTOMJS_PORT'][len('tcp://'):]

    ctx.obj = ObjectDict(ctx.obj or {})
    ctx.obj['instances'] = []
    ctx.obj.update(kwargs)

    if ctx.invoked_subcommand is None and not ctx.obj.get('testing_mode'):
        ctx.invoke(all)
    return ctx


@cli.command()
@click.option('--xmlrpc/--no-xmlrpc', default=True)
@click.option('--xmlrpc-host', default='0.0.0.0')
@click.option('--xmlrpc-port', envvar='SCHEDULER_XMLRPC_PORT', default=23333)
@click.option('--inqueue-limit', default=0,
              help='size limit of task queue for each project, '
              'tasks will been ignored when overflow')
@click.option('--delete-time', default=24 * 60 * 60,
              help='delete time before marked as delete')
@click.option('--active-tasks', default=100, help='active log size')
@click.option('--loop-limit', default=1000, help='maximum number of tasks due with in a loop')
@click.pass_context
def scheduler(ctx, xmlrpc, xmlrpc_host, xmlrpc_port,
              inqueue_limit, delete_time, active_tasks, loop_limit, Scheduler=Scheduler):
    g = ctx.obj
    scheduler = Scheduler(taskdb=g.taskdb, projectdb=g.projectdb, resultdb=g.resultdb,
                          newtask_queue=g.newtask_queue, status_queue=g.status_queue,
                          out_queue=g.scheduler2fetcher, data_path=g.get('data_path', 'data'))
    scheduler.INQUEUE_LIMIT = inqueue_limit
    scheduler.DELETE_TIME = delete_time
    scheduler.ACTIVE_TASKS = active_tasks
    scheduler.LOOP_LIMIT = loop_limit

    g.instances.append(scheduler)
    if g.get('testing_mode'):
        return scheduler

    if xmlrpc:
        run_in_thread(scheduler.xmlrpc_run, port=xmlrpc_port, bind=xmlrpc_host)
    scheduler.run()


@cli.command()
@click.option('--xmlrpc/--no-xmlrpc', default=False)
@click.option('--xmlrpc-host', default='0.0.0.0')
@click.option('--xmlrpc-port', envvar='FETCHER_XMLRPC_PORT', default=24444)
@click.option('--poolsize', default=100, help="max simultaneous fetches")
@click.option('--proxy', help="proxy host:port")
@click.option('--user-agent', help='user agent')
@click.option('--timeout', help='default fetch timeout')
@click.pass_context
def fetcher(ctx, xmlrpc, xmlrpc_host, xmlrpc_port, poolsize, proxy, user_agent,
            timeout, Fetcher=Fetcher):
    g = ctx.obj
    fetcher = Fetcher(inqueue=g.scheduler2fetcher, outqueue=g.fetcher2processor,
                      poolsize=poolsize, proxy=proxy)
    fetcher.phantomjs_proxy = g.phantomjs_proxy
    if user_agent:
        fetcher.user_agent = user_agent
    if timeout:
        fetcher.default_options = dict(fetcher.default_options)
        fetcher.default_options['timeout'] = timeout

    g.instances.append(fetcher)
    if g.get('testing_mode'):
        return fetcher

    if xmlrpc:
        run_in_thread(fetcher.xmlrpc_run, port=xmlrpc_port, bind=xmlrpc_host)
    fetcher.run()


@cli.command()
@click.pass_context
def processor(ctx, Processor=Processor):
    g = ctx.obj
    processor = Processor(projectdb=g.projectdb,
                          inqueue=g.fetcher2processor, status_queue=g.status_queue,
                          newtask_queue=g.newtask_queue, result_queue=g.processor2result)

    g.instances.append(processor)
    if g.get('testing_mode'):
        return processor

    processor.run()


@cli.command()
@click.pass_context
def result_worker(ctx, ResultWorker=ResultWorker):
    g = ctx.obj
    result_worker = ResultWorker(resultdb=g.resultdb, inqueue=g.processor2result)

    g.instances.append(result_worker)
    if g.get('testing_mode'):
        return result_worker

    result_worker.run()


@cli.command()
@click.option('--host', default='0.0.0.0', envvar='WEBUI_HOST',
              help='webui bind to host')
@click.option('--port', default=5000, envvar='WEBUI_PORT',
              help='webui bind to host')
@click.option('--cdn', default='//cdnjscn.b0.upaiyun.com/libs/',
              help='js/css cdn server')
@click.option('--scheduler-rpc', callback=connect_rpc, help='xmlrpc path of scheduler')
@click.option('--fetcher-rpc', callback=connect_rpc, help='xmlrpc path of fetcher')
@click.option('--max-rate', type=float, help='max rate for each project')
@click.option('--max-burst', type=float, help='max burst for each project')
@click.option('--username', envvar='WEBUI_USERNAME',
              help='username of lock -ed projects')
@click.option('--password', envvar='WEBUI_PASSWORD',
              help='password of lock -ed projects')
@click.option('--need-auth', default=False, help='need username and password')
@click.pass_context
def webui(ctx, host, port, cdn, scheduler_rpc, fetcher_rpc,
          max_rate, max_burst, username, password, need_auth, app=app):
    g = ctx.obj
    app.config['taskdb'] = g.taskdb
    app.config['projectdb'] = g.projectdb
    app.config['resultdb'] = g.resultdb
    app.config['cdn'] = cdn

    if max_rate:
        app.config['max_rate'] = max_rate
    if max_burst:
        app.config['max_burst'] = max_burst
    if username:
        app.config['webui_username'] = username
    if password:
        app.config['webui_password'] = password

    # fetcher rpc
    if isinstance(fetcher_rpc, six.string_types):
        fetcher_rpc = connect_rpc(ctx, None, fetcher_rpc)
    if fetcher_rpc is None:
        fetcher = Fetcher(inqueue=None, outqueue=None, async=False)
        fetcher.phantomjs_proxy = g.phantomjs_proxy
        app.config['fetch'] = lambda x: fetcher.fetch(x)[1]
    else:
        import umsgpack
        app.config['fetch'] = lambda x: umsgpack.unpackb(fetcher_rpc.fetch(x).data)

    if isinstance(scheduler_rpc, six.string_types):
        scheduler_rpc = connect_rpc(ctx, None, scheduler_rpc)
    if scheduler_rpc is None and os.environ.get('SCHEDULER_NAME'):
        app.config['scheduler_rpc'] = connect_rpc(ctx, None, 'http://%s/' % (
            os.environ['SCHEDULER_PORT_23333_TCP'][len('tcp://'):]))
    elif scheduler_rpc is None:
        app.config['scheduler_rpc'] = connect_rpc(ctx, None, 'http://localhost:23333/')
    else:
        app.config['scheduler_rpc'] = scheduler_rpc

    app.debug = g.debug
    g.instances.append(app)
    if g.get('testing_mode'):
        return app

    app.run(host=host, port=port)


@cli.command()
@click.option('--fetcher-num', default=1, help='instance num of fetcher')
@click.option('--processor-num', default=1, help='instance num of processor')
@click.option('--result-worker-num', default=1,
              help='instance num of result worker')
@click.option('--run-in', default='subprocess', type=click.Choice(['subprocess', 'thread']),
              help='run each components in thread or subprocess. '
              'always using thread for windows.')
@click.pass_context
def all(ctx, fetcher_num, processor_num, result_worker_num, run_in):
    ctx.obj['debug'] = False
    g = ctx.obj

    if run_in == 'subprocess' and os.name != 'nt':
        run_in = run_in_subprocess
    else:
        run_in = run_in_thread

    threads = []

    # result worker
    result_worker_config = g.config.get('result_worker', {})
    for i in range(result_worker_num):
        threads.append(run_in(ctx.invoke, result_worker, **result_worker_config))

    # processor
    processor_config = g.config.get('processor', {})
    for i in range(processor_num):
        threads.append(run_in(ctx.invoke, processor, **processor_config))

    # fetcher
    fetcher_config = g.config.get('fetcher', {})
    fetcher_config.setdefault('xmlrpc_host', '127.0.0.1')
    for i in range(fetcher_num):
        threads.append(run_in(ctx.invoke, fetcher, **fetcher_config))

    # scheduler
    scheduler_config = g.config.get('scheduler', {})
    scheduler_config.setdefault('xmlrpc_host', '127.0.0.1')
    threads.append(run_in(ctx.invoke, scheduler, **scheduler_config))

    # running webui in main thread to make it exitable
    webui_config = g.config.get('webui', {})
    webui_config.setdefault('scheduler_rpc', 'http://localhost:%s/'
                            % g.config.get('scheduler', {}).get('xmlrpc_port', 23333))
    ctx.invoke(webui, **webui_config)

    # exit components run in threading
    for each in g.instances:
        each.quit()

    # exit components run in subprocess
    for each in threads:
        if hasattr(each, 'terminate'):
            each.terminate()
        each.join()


@cli.command()
@click.option('--fetcher-num', default=1, help='instance num of fetcher')
@click.option('--processor-num', default=2, help='instance num of processor')
@click.option('--result-worker-num', default=1, help='instance num of result worker')
@click.option('--run-in', default='subprocess', type=click.Choice(['subprocess', 'thread']),
              help='run each components in thread or subprocess. '
              'always using thread for windows.')
@click.option('--total', default=10000, help="total url in test page")
@click.option('--show', default=20, help="show how many urls in a page")
@click.pass_context
def bench(ctx, fetcher_num, processor_num, result_worker_num, run_in, total, show):
    from pyspider.libs import bench
    from pyspider.webui import bench_test
    bench_test  # make pyflake happy

    ctx.obj['debug'] = False
    g = ctx.obj
    if result_worker_num == 0:
        g['processor2result'] = None

    if run_in == 'subprocess' and os.name != 'nt':
        run_in = run_in_subprocess
    else:
        run_in = run_in_thread

    g.projectdb.insert('bench', {
        'name': 'bench',
        'status': 'RUNNING',
        'script': bench.bench_script % {'total': total, 'show': show},
        'rate': total,
        'burst': total,
        'updatetime': time.time()
    })

    # disable log
    logging.getLogger().setLevel(logging.ERROR)
    logging.getLogger('scheduler').setLevel(logging.ERROR)
    logging.getLogger('fetcher').setLevel(logging.ERROR)
    logging.getLogger('processor').setLevel(logging.ERROR)
    logging.getLogger('result').setLevel(logging.ERROR)
    logging.getLogger('webui').setLevel(logging.ERROR)

    threads = []

    # result worker
    result_worker_config = g.config.get('result_worker', {})
    for i in range(result_worker_num):
        threads.append(run_in(ctx.invoke, result_worker,
                              ResultWorker=bench.BenchResultWorker, **result_worker_config))

    # processor
    processor_config = g.config.get('processor', {})
    for i in range(processor_num):
        threads.append(run_in(ctx.invoke, processor,
                              Processor=bench.BenchProcessor, **processor_config))

    # fetcher
    fetcher_config = g.config.get('fetcher', {})
    fetcher_config.setdefault('xmlrpc_host', '127.0.0.1')
    for i in range(fetcher_num):
        threads.append(run_in(ctx.invoke, fetcher,
                              Fetcher=bench.BenchFetcher, **fetcher_config))

    # scheduler
    scheduler_config = g.config.get('scheduler', {})
    scheduler_config.setdefault('xmlrpc_host', '127.0.0.1')
    threads.append(run_in(ctx.invoke, scheduler,
                          Scheduler=bench.BenchScheduler, **scheduler_config))

    # webui
    webui_config = g.config.get('webui', {})
    webui_config.setdefault('scheduler_rpc', 'http://localhost:%s/'
                            % g.config.get('scheduler', {}).get('xmlrpc_port', 23333))
    threads.append(run_in(ctx.invoke, webui, **webui_config))

    # run project
    time.sleep(1)
    import requests
    rv = requests.post('http://localhost:5000/run', data={
        'project': 'bench',
    })
    assert rv.status_code == 200, 'run project error'

    # wait bench test finished
    while True:
        time.sleep(1)
        if builtins.all(getattr(g, x) is None or getattr(g, x).empty() for x in (
                'newtask_queue', 'status_queue', 'scheduler2fetcher',
                'fetcher2processor', 'processor2result')):
            break

    # exit components run in threading
    for each in g.instances:
        each.quit()

    # exit components run in subprocess
    for each in threads:
        if hasattr(each, 'terminate'):
            each.terminate()
        each.join(1)


def main():
    cli()

if __name__ == '__main__':
    main()
