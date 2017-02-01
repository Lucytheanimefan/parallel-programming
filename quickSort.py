import random
from multiprocessing import *
import multiprocessing
import sys
import random, time

#global variables
processes = 1
set_num_processes = 2

def main():
	sys.setrecursionlimit(2**30)
	num_elem = 2000
	to_sort = [random.randint(0,num_elem) for num in range(num_elem)]
	print "Going to sort: "+str(to_sort)
	originalQS_start = time.time()
	original_sorted = originalQuickSort(to_sort)
	original_time = time.time() - originalQS_start
	print "Original sequential quick sort sorted "+str(original_sorted)+" in "+str(original_time)+ " s"
	print "-----------------------------------------"
	q = multiprocessing.Queue()
	psort = MTQuickSort(to_sort, q)
	parallel_start = time.time()
	psort.start()
	p_time = time.time() - parallel_start
	psorted = q.get()
	psort.join()
	print "Parallel quick sort sorted "+str(psorted)+" in "+str(p_time)+" s"





class MTQuickSort(multiprocessing.Process):

    def __init__(self, list_to_sort, queue):
        super(MTQuickSort, self).__init__()
        print self.name
        self.queue = queue
        self.list = list_to_sort

    def run(self):
		self.queue.put(self.quicksort(self.list))

    def quicksort(self, my_list):
		global processes
		global set_num_processes
		if len(my_list) is 0:
			print "List is empty"
			return []
		else:
			pivot = my_list[0] #not random
			print "Pivot: "+str(pivot)
			left = [x for x in my_list[1:] if x<=pivot] #elements less than or equal to pivot
			right = [x for x in my_list[1:] if x > pivot] #elements greater than or equal to pivot
			if processes < set_num_processes:
				processes+=1
				#create threads in blocks of 2, list is partitioned into 2 parts
				left_q = multiprocessing.Queue()
				right_q = multiprocessing.Queue()
				qs_process_left = MTQuickSort(left, left_q)
				qs_process_right = MTQuickSort(right, right_q)
				qs_process_left.start()
				qs_process_right.start()
				to_return = left_q.get() + [pivot] + right_q.get()
				qs_process_left.join()
				qs_process_right.join()
				return to_return

	

def originalQuickSort(arr):
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
	return originalQuickSort(left) + equal + originalQuickSort(right)

if __name__ == '__main__':
	main()