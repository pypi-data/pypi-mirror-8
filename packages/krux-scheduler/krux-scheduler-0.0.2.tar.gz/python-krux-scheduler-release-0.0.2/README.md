python-krux-scheduler
=====================

Krux Python class built on top of [Krux Stdlib](https://staticfiles.krxd.net/foss/docs/pypi/krux-stdlib/) for interacting with [APScheduler](http://pythonhosted.org//APScheduler/)

Application quick start
-----------------------

The most common use case for this library is to run a job periodically from a script.
To do that, do the following:

```python

import time
from krux_scheduler import Application

def main():
    ### The name must be unique to the organization. The object  
    ### returned inherits from krux.cli.Application, so it provides
    ### all that functionality as well.
    app = Application( name = 'krux-my-periodic-job' )
    
    ### This is the scheduler object, which behaves exactly 
    ### like an APScheduler object, but with logging, stats 
    ### and CLI support added.
    scheduler = app.scheduler

    ### define the job you want to run periodically
    def periodic_job():
        print 'Called %s at %s' % (app.name, time.asctime())

    ### add the periodic job to the scheduler. This follows 
    ### APSchedulers arguments & functionality exactly.
    scheduler.add_cron_job(
        func   = periodic_job,
        hour   = '0,8,16'
        minute = '0',
    )

    ### start the scheduler
    scheduler.start()

    ### always call app.exit(), so any clean up that needs to
    ### happen can be done at the end of your program. It also
    ### sets the exit code for you appropriately.
    app.exit()

### Run the application stand alone
if __name__ == '__main__':
    main()

```

Seeing it in action
-------------------

This library comes with a CLI tool bundled that shows you how the code works.
If you run this, it'll alternate between throwing an exception (which is caught)
and a simple printed message. 

These are the options and how you can invoke it:

```
$ krux-scheduler-test  -h
usage: krux-scheduler-test [-h]
                           [--log-level {info,debug,critical,warning,error}]
                           [--stats] [--stats-host STATS_HOST]
                           [--stats-port STATS_PORT]
                           [--stats-environment STATS_ENVIRONMENT]
                           [--scheduler-minute SCHEDULER_MINUTE]
                           [--scheduler-hour SCHEDULER_HOUR]
                           [--scheduler-daemonize]
                           [--scheduler-exit-after-job]

krux-scheduler-test

optional arguments:
  -h, --help            show this help message and exit

logging:
  --log-level {info,debug,critical,warning,error}
                        Verbosity of logging. (default: warning)

stats:
  --stats               Enable sending statistics to statsd. (default: False)
  --stats-host STATS_HOST
                        Statsd host to send statistics to. (default:
                        localhost)
  --stats-port STATS_PORT
                        Statsd port to send statistics to. (default: 8125)
  --stats-environment STATS_ENVIRONMENT
                        Statsd environment. (default: dev)

scheduler:
  --scheduler-minute SCHEDULER_MINUTE
                        Comma separated list of minute mark(s) to run on. This
                        overrides any hardcoded arguments (default: None)
  --scheduler-hour SCHEDULER_HOUR
                        Comma separated list of hour mark(s) to run on. This
                        overrides any hardcoded arguments (default: None)
  --scheduler-daemonize
                        Run scheduled jobs in separate threads (default:
                        False)
  --scheduler-exit-after-job
                        Exit the application after a job has completed. Very
                        useful for RAM hungry applications whose only purpose
                        is to run a single job but not otherwise. Requires a
                        process monitor to restart if it exits (default:
                        False)
```
