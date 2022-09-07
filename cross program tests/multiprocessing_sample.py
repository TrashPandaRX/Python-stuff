"""A very simple parallel code example to execute parallel functions in python"""
import multiprocessing
import numpy as np
import time

#I slightly modified this code to add the timer, to measure how fast the prog ran and the single threaded, single process version
#t0 = time.time()

def multiprocessing_func(x):
    """Individually prints the squares y_i of the elements x_i of a vector x"""
    for x_i in x:
        y=x_i**2 
        #print('The square of ',x_i,' is ',y)   #temp removal

def chunks(input, n):
    """Yields successive n-sized chunks of input"""
    for i in range(0, len(input), n):
        yield input[i:i + n]

if __name__=='__main__':
 
    n_proc=1 #Numer of available processors
    while n_proc <= 8:
        t0 = time.time()

        print("using {} cores.".format(n_proc))
        x=np.arange(100000000) #Input
        chunked_x=list(chunks(x, int(x.shape[0]/n_proc)+1)) #Splits input among n_proc chunks
        processes=[] #Initialize the parallel processes list
        for i in np.arange(0,n_proc):
            """Execute the target function on the n_proc target processors using the splitted input""" 
            p = multiprocessing.Process(target=multiprocessing_func,args=(chunked_x[i],))
            processes.append(p)
            p.start()
        for process in processes:
            process.join()
        
        t1 = time.time() - t0
        print("Time elapsed: ", t1) # CPU seconds elapsed
        n_proc += 1

    # no multi processing
    print("now using no multiprocessing:")
    t0 = time.time()
    x=np.arange(100000000) #Input
    for x_i in x:
        y=x_i**2
    print("Time elapsed: ", time.time() - t0) # CPU seconds elapsed

    

