import multiprocessing
import os

workers=2*multiprocessing.cpu_count()+1
worker_class='sync'
worker_connection=1000

timeout=30
graceful_timeout=30

max_request=1000
max_request_jitter=50

accesslog='-'
errorlog='-'
loglevel='info'

bind = f"0.0.0.0:{os.environ.get('PORT', 10000)}"