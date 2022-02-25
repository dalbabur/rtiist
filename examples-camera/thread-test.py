import threading

class MyThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.sleep_event = threading.Event()
        self.damon = True

    def run(self):
        while True:
            self.sleep_event.clear()
            threading.Thread(target=self._run).start()

    def _run(self):
        print("run")

my_thread = MyThread()
my_thread.start()

while True:
    input("Hit ENTER to force execution\n")
    my_thread.sleep_event.set()