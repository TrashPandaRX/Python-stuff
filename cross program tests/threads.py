import threading
import random
from time import sleep

'''
def print_cube(num):
    print("Cube: {}".format(num * num * num))

def print_square(num):
    print("Square: {}".format(num * num))

def print_notes(note):
    sleep(2)
    print("Singing: {} - {}".format(note, sum([1,2,3,4,5,6,7,8,9,10])))

if __name__ == '__main__':
    t1 = threading.Thread(target = print_square, args = (10,))  # for some reason this only works when you plop a comma behind the value
    t2 = threading.Thread(target = print_cube, args = (10,))

    t1.start()
    t2.start()

    print(threading.active_count(), " is the current # of threads") 
    # should be 2, but eversince adding the code below the print()
    # geometry line, its returning just 1
    
    t1.join()
    t2.join()

    print("Done with geometry!")


    print(threading.active_count())


    # Dont' 100% get threads, the below is SUPER ugly

    # t1-t8 originally outside of scales list
    # scales not containing threads unfortunately
    
    #scales = []

    t1 = threading.Thread(target = print_notes, args = ("Do - #1",))   # originally didnt have  here
    t2 = threading.Thread(target = print_notes, args = ("re - #2",))
    t3 = threading.Thread(target = print_notes, args = ("me - #3",))
    t4 = threading.Thread(target = print_notes, args = ("fa - #4",))
    t5 = threading.Thread(target = print_notes, args = ("so - #5",))
    t6 = threading.Thread(target = print_notes, args = ("la - #6",))
    t7 = threading.Thread(target = print_notes, args = ("ti - #7",))
    t8 = threading.Thread(target = print_notes, args = ("dO - #8",))
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    print("enumerate() of threading : ", len(threading.enumerate()))

    # thought of this little bit, hope it works...
    # intended to look at all ALIVE threads in threading and activate them one at a time (including daemon and dummy threads)
    # NOTE dont forget the main thread also counts as a thread!
    for thread in threading.enumerate()[1:]:    # [1:] skips the mainthread
        print(thread.name," initialized!")

    # randomly end some threads early
    for thread in threading.enumerate()[1:]:
        if random.randint(0,1) == 0:
            thread.join()
            print("snagged ", thread.name)

    print("----------------")


    
    # this threw an error when i didnt have [1:] because you cant .join() the MainThread normally
    for thread in threading.enumerate()[1:]:
        thread.join()
        print("Done with ", thread.name)

    
    print("All musical threads completed!")
'''
notes = ["Do", "Re","Me", "Fa","So", "La", "Ti", "dO"]
letters = ["a", "b","c", "d","e", "f","g", "h","i", "j","k", "l","m", "n","o", "p","q", "r","s", "t","u", "v","w", "x","y", "z"]


def singing():
    print()


class experiment(threading.Thread):
    def __init__(self, name = "experiment"):
        self._StopEvent = threading.Event()
        self._Sleeper = 0.5
        threading.Thread.__init__(self, name=name)

    def run(self):
        print ("number of running threads: ", len(threading.enumerate()))
        if len(threading.enumerate()) < 3:
            count = 0.0

            # while the stop event hasnt been set to true (its false by default)
            while not self._StopEvent.is_set():
                count += .5
                print("{} up".format(count))
                self._StopEvent.wait(self._Sleeper)
            print("{} ending".format(self.name))
        else:
            count = 20.0
            while not self._StopEvent.is_set():
                count -= .5
                print("{} down".format(count))
                self._StopEvent.wait(self._Sleeper)
            print("{} ending".format(self.name))


    def join(self, timeout = None):
        self._StopEvent.set()
        threading.Thread.join(self,timeout)

if __name__ == '__main__':
    testthread = experiment()
    testthread2 = experiment()
    testthread.start()
    testthread2.start()

    import time
    time.sleep(20.0)

    testthread.join()
    testthread2.join()
'''
BROKEN

def start_counting():
    print("we are starting!")
    for x in range(1,20):
        print(x)
        sleep(.5)

def stop_early(x : threading.Thread):
    print("time to close up shop")
    timeout = None
    theEnd.set()
    print("got below .set()")
    
    x.join(timeout)
    print("got past .join()")


if __name__ == '__main__':
    t1 = threading.Thread(target = start_counting)
    t1.start()
    while not theEnd.is_set():
        sleep(.5)
        if (random.randint(0,4) == 0):
            stop_early(t1)
            break
    print("done threading")
'''