import random, multiprocessing, time

DESIRED_PROC_DEPTH = 2 #number of processes
proc_depth = 1 #counter for number of processes 

def main():
    #import sys; sys.setrecursionlimit(2**30)
    num_elements = 20000
    list_of_numbers = [random.randint(0,num_elements) for num in range(num_elements)]
    # print list_of_numbers
    simple_start = time.time()
    simple_sorted = quicksort_seq(list_of_numbers)
    simple_total_time = time.time() - simple_start
    print "Using a single thread we sorted " + str(num_elements) + " elements in " + str(simple_total_time) + " seconds"
    the_q = multiprocessing.Queue()
    sorter = MTQuickSort(list_of_numbers, the_q)
    start = time.time()
    sorter.start()
    mt_total_time = time.time() - start
    sorted_list = the_q.get()
    # print sorted_list
    sorter.join()
    print "Sorted " + str(num_elements) + " elements in " + str(mt_total_time) + " seconds"


class MTQuickSort(multiprocessing.Process):

    def __init__(self, list_to_sort, queue):
        super(MTQuickSort, self).__init__()
        #print self.name
        self.queue = queue
        self.list = list_to_sort

    def run(self):
        self.queue.put(self.quicksort(self.list))

    def quicksort(self, list):
        global proc_depth
        global DESIRED_PROC_DEPTH
        if len(list) is 0:
            return []
        else:
            pivot = list[0]
            less = [x for x in list[1:] if x <= pivot]
            greater = [x for x in list[1:] if x > pivot]
            if proc_depth < DESIRED_PROC_DEPTH:
                proc_depth += 1
                #2 threads
                lessor_q = multiprocessing.Queue()
                greater_q = multiprocessing.Queue()
                qs_process1 = MTQuickSort(less, lessor_q)
                qs_process2 = MTQuickSort(greater, greater_q)
                qs_process1.start()
                qs_process2.start()
                to_return = lessor_q.get() + [pivot] + greater_q.get()
                qs_process1.join()
                qs_process2.join()
                return to_return
            else:
                less_than_pivot = self.quicksort(less)
                greater_than_pivot = self.quicksort(greater)
                return less_than_pivot + [pivot] + greater_than_pivot

def quicksort_seq(arr):
    if len(arr)<=1:
        return arr
    index = random.randint(0,len(arr)-1)
    pivot = arr[index]
    #print pivot
    left = []
    right = []
    equal = []
    for i in range(len(arr)):
        if arr[i]<pivot:
            left.append(arr[i])
        elif arr[i]>pivot:
            right.append(arr[i])
        elif arr[i] is pivot:
            equal.append(arr[i])
    return quicksort_seq(left) + equal + quicksort_seq(right)

if __name__ == '__main__':
    main()