from spruce.task import task, App
from spruce.worker import Worker

if __name__ == '__main__':

    # Sender
    # 1. create the app which defines how to route the task message to
    app = App()
    # 2. send the task with all information
    app_id = app.send(name='my_task', params={'first_name': 'Fang', 'last_name': 'Nan'}, )


    # Worker
    # 1. define the execution code of the task, make it findable in the execution path
    @task()
    def my_task(first_name, last_name):
        return 'hello %s %s' % (first_name, last_name)

    # 2. run worker to listen the task
    worker = Worker(listen=['my_task'])
    worker.run()
