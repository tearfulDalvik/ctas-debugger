from threading import Thread

def wait_remote_command(queue):
    while(True):
        print(queue.get())