import musicazoo.queue
import musicazoo.lib.service as service
from musicazoo.queue.module import Module
import os
import signal

cwd=os.path.dirname(__file__)

class Youtube(Module):
    TYPE_STRING='youtube'
    process = ['python',os.path.join(cwd,'modules/youtube.py')]

class Problem(Module):
    TYPE_STRING='problem'
    process = ['python',os.path.join(cwd,'modules/problem.py')]

class Text(Module):
    TYPE_STRING='text'
    process = ['python',os.path.join(cwd,'modules/text.py')]

modules = [Youtube, Problem, Text]
backgrounds = [Youtube, Problem, Text]

q=musicazoo.queue.Queue(modules, backgrounds)

def shutdown_handler(signum,frame):
    print
    print "Received signal, attempting graceful shutdown..."
    service.ioloop.add_callback_from_signal(q.shutdown)

signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

service.ioloop.start()
