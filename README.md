# Remote Docker

*Run a docker command, tracking progress, sync results and manage, all of these in one simple cli.*

## Installation

### Requirements
1. Unix based OS (I suspect that some portion of the code is not os independent)
2. rsync, which should be ubiquitous among that kind of OSes.
3. Python 3, I just didn't test on Python 2 and even it works it's not gonna be without a glitch.

If you're quilified ...

```
pip install remote-docker
```

## Usage

It's easier to give a realistic use case, let's say we have arranged our project  (python) as follows:

```
project_root
- src
	- __init__.py
	- __main__.py
	- lib
		- ...
- Dockerfile
```


1. Declare the *running environment* in a `Dockerfile` (in the same directory at which the `cli` will be run, basically, the same as your source directory).

e.g. `Dockerfile`

```
FROM python:3
```

2. Run using `run` command in the form `rdocker run --tag=<jobname> --host=<user@host> --path=<host_path> <command> <args...>`. In this very case, we will use `rdocker run --tag=test --host=some@host --path=/tmp/myproject python -u -m src`. What it really does is:
	1. **Sync** (using `rsync`) the source code to the remote host, in this case, whole directory of `project_root` will be copied to the directory `/tmp/myproject` of the host, well there is some exceptions though you can define it using `.remotedignore`, which automatically initiated during the invocation of `rdocker`.
	2. **Build**, the `Dockerfile` will be built under `docker build -t <jobname>`. By the way, you can have a docker executable of your choice! e.g. `nvidia-docker` all you need do is to state `--docker=nvidia-docker` in the `run` command.
	3. **Run**, the designated command will be run inside a newly hatched container under the detach mode i.e. you don't have to be there and wait the process to finish.
	4. **Log**, all the output from that container will be live fed to your console, closing now won't budge the running container a bit.
	5. **Sync Back**, after the process in done, all the changes on the remote dirtory will be synced back to your computer's `project_root`, don't fear it will destroy your new changes, it will only make change to old files. (`rsync -u`)

3. Close your laptop and go to sleep, next day morning run `rdocker run` or `rdocker run --tag=test` you will see the progress, and if it's done you will get your results right back to your laptop.

Note: please see `--help` for the deeper use of the cli.