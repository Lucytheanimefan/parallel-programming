from multiprocessing import Pool
import datetime
import time



def solve1(letter):
	for i in range(0,5):
		ts = time.time()
		st = str(datetime.datetime.now())
		print(str(i) +'_'+ st +'_'+ letter)

def solve2(letter):
	for i in range(0,5):
		ts = time.time()
		st = str(datetime.datetime.now())
		print(str(i) +'_'+ st +'_'+ letter)

pool = Pool()
result1 = pool.apply_async(solve1, ['A'])    # evaluate "solve1(A)" asynchronously
result2 = pool.apply_async(solve2, ['B'])    # evaluate "solve2(B)" asynchronously
answer1 = result1.get(timeout=10)
answer2 = result2.get(timeout=10)

print("--------------")
solve1("A")
solve2("B")

