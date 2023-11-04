from invoke import task


@task
def foo(c):
    ...


@task
def setup(c):
    print('example platform setup')
