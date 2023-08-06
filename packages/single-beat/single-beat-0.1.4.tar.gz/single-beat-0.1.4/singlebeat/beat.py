import os
import sys
import pyuv
import time
import socket
import redis
import logging
import signal

REDIS_SERVER = os.environ.get('SINGLE_BEAT_REDIS_SERVER',
                              'redis://localhost:6379')
IDENTIFIER = os.environ.get('SINGLE_BEAT_IDENTIFIER', None)
LOCK_TIME = int(os.environ.get('SINGLE_BEAT_LOCK_TIME', 5))
INITIAL_LOCK_TIME = int(os.environ.get('SINGLE_BEAT_INITIAL_LOCK_TIME',
                                       LOCK_TIME * 2))
HEARTBEAT_INTERVAL = int(os.environ.get('SINGLE_BEAT_HEARTBEAT_INTERVAL', 1))
HOST_IDENTIFIER = os.environ.get('SINGLE_BEAT_HOST_IDENTIFIER',
                                 socket.gethostname())
LOG_LEVEL = os.environ.get('SINGLE_BEAT_LOG_LEVEL', 'warn')

# wait_mode can be, supervisored or heartbeat
WAIT_MODE = os.environ.get('SINGLE_BEAT_WAIT_MODE', 'heartbeat')
assert WAIT_MODE in ('supervised', 'heartbeat')
WAIT_BEFORE_DIE = int(os.environ.get('SINGLE_BEAT_WAIT_BEFORE_DIE', 60))

numeric_log_level = getattr(logging, LOG_LEVEL.upper(), None)
logging.basicConfig(level=numeric_log_level)
logger = logging.getLogger(__name__)

rds = redis.Redis.from_url(REDIS_SERVER)
rds.ping()


class Process(object):
    def __init__(self, args):
        self.args = args
        self.state = None
        self.t1 = time.time()

        self.identifier = IDENTIFIER or self.args[0]

        signal.signal(signal.SIGTERM, self.sigterm_handler)
        signal.signal(signal.SIGINT, self.sigterm_handler)

        self.loop = pyuv.Loop.default_loop()
        self.timer = pyuv.Timer(self.loop)
        self.state = 'WAITING'

    def proc_exit_cb(self, proc, exit_status, term_signal):
        sys.exit(exit_status)

    def stdout_read_cb(self, handle, data, error):
        if data:
            sys.stdout.write(data)

    def stderr_read_cb(self, handle, data, error):
        if data:
            sys.stdout.write(data)

    def timer_cb(self, timer):
        logger.debug("timer called %s state=%s",
                     time.time() - self.t1, self.state)
        self.t1 = time.time()
        if self.state == 'WAITING':
            if self.acquire_lock(self.identifier):
                self.spawn_process()
            else:
                if WAIT_MODE == 'supervised':
                    logging.debug("already running, will exit after %s seconds"
                                  % WAIT_BEFORE_DIE)
                    time.sleep(WAIT_BEFORE_DIE)
                    sys.exit()
        elif self.state == "RUNNING":
            rds.set("SINGLE_BEAT_%s" % self.identifier,
                    "%s:%s" % (HOST_IDENTIFIER, self.proc.pid), ex=LOCK_TIME)

    def acquire_lock(self, identifier):
        return rds.execute_command('SET', 'SINGLE_BEAT_%s' % self.identifier,
                                   "%s:%s" % (HOST_IDENTIFIER, '0'),
                                   'NX', 'EX', INITIAL_LOCK_TIME)

    def sigterm_handler(self, signum, frame):
        logging.debug("our state %s", self.state)
        if self.state == 'WAITING':
            sys.exit(signum)
        elif self.state == 'RUNNING':
            logger.debug('already running sending signal to child - %s',
                         self.proc.pid)
            os.kill(self.proc.pid, signum)

    def run(self):
        # runs every 1 second
        self.timer.start(self.timer_cb, 0.1, HEARTBEAT_INTERVAL)
        self.loop.run()

    def spawn_process(self):
        args = sys.argv[1:]
        self.proc = pyuv.Process(self.loop)

        stdout_pipe = pyuv.Pipe(self.loop)
        stderr_pipe = pyuv.Pipe(self.loop)

        stdio = []
        stdio.append(pyuv.StdIO(flags=pyuv.UV_IGNORE))
        stdio.append(pyuv.StdIO(
            stream=stdout_pipe,
            flags=pyuv.UV_CREATE_PIPE | pyuv.UV_WRITABLE_PIPE))
        stdio.append(pyuv.StdIO(
            stream=stderr_pipe,
            flags=pyuv.UV_CREATE_PIPE | pyuv.UV_WRITABLE_PIPE))

        self.state = "RUNNING"

        self.proc.spawn(file=args[0],
                        args=args[1:],
                        cwd=os.getcwd(),
                        exit_callback=self.proc_exit_cb,
                        stdio=stdio)

        stdout_pipe.start_read(self.stdout_read_cb)
        stderr_pipe.start_read(self.stderr_read_cb)


def run_process():
    process = Process(sys.argv[1:])
    process.run()

if __name__ == "__main__":
    run_process()
