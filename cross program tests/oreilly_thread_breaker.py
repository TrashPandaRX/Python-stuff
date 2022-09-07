import threading

class TestThread(threading.Thread):

    def __init__(self, name='TestThread'):
        """ constructor, setting initial variables """
        self._stopevent = threading.Event()
        self._sleepperiod = 1.0

        threading.Thread.__init__(self, name=name)

    def run(self):
        """ main control loop """
        print("inside run")
        print("{} starts".format(self.name))

        count = 0
        while not self._stopevent.is_set():
            count += 1
            print("loop {}".format(count))
            self._stopevent.wait(self._sleepperiod)

        print ("{} ends".format(self.name))

    def join(self, timeout=None):
        """ Stop the thread. """
        print("inside join")

        self._stopevent.set()
        threading.Thread.join(self, timeout)

if __name__ == "__main__":
    testthread = TestThread()
    testthread.start()

    import time
    time.sleep(15.0)

    testthread.join()

'''
OKAY so this is how this works.

one of the most important variable assignments is self._stopevent = threading.Event()

once this gets set the rest of the run(self)'s loop is listening for _stopevent to be set...which occurs
inside of the modified join (which btw behaves like the normal after you added the
extra _stopevent.set() command join because threading.Thread.join(self, timeout) calls upon the UNmodified regular version)

and finally the modified constructer function testthread.join() is called after X amount of time. which closes shop on the thread

'''