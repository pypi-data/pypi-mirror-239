import sys

from invoke import task

from src.edwh import task_for_namespace, get_task


@task
def setup(c):
    print('example local setup')
    if previous_setup := get_task("setup"):
        # don't execute because that would cause a loop!
        print(previous_setup)
    else:
        print("No global setup found", file=sys.stderr)

    if whitelabel_setup := get_task("whitelabel.setup"):
        whitelabel_setup(c)
    else:
        print("No whitelabel setup found", file=sys.stderr)

    if platform_setup := task_for_namespace("platform", "setup"):
        platform_setup(c)
    else:
        print("No platform setup found", file=sys.stderr)
