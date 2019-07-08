# t1 -> t2 - t3
from taskbay.task import task


@task()
def t1():
    print('t1 executed')

@task()
def t2():
    print('t2 executed')

@task()
def t3():
    print('t3 executed')


# workflow defined by event processing
# Rules:
#  on event(t1, COMPLETED): schedule a new task(t2)
#  on event(t2, COMPLETED): schedule a new task(t3)
