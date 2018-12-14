import animation
import random
import time
import sys
import argparse

def inorder(y, zeros = False):
    if zeros:
        x = list(filter(lambda i: i!=0, y))
    else:
        x = y

    i = 0
    j = len(x)
    while i + 1 < j:
        if x[i] > x[i + 1]:
            return False
        i += 1
    return True


class radixsort(animation.SortingAlgorithm):
    def sort(self):
        arrcopy = []
        for i in range(len(self.array)):
            arrcopy.append(self.get(i))

        for i in range(len(self.array)):
            self.set(arrcopy[i],arrcopy[i]) 


class jsquirks(animation.SortingAlgorithm):
    def initialize(self):

        self.drawcolor((248, 24, 148))
        self.fit()

    def sort(self):
        arrcopy = []
        for i in range(len(self.array)):
            arrcopy.append(self.get(i))

        for i in range(len(self.array)):
            self.set(arrcopy[i],arrcopy[i]) 

    def shutdown(self):
        self.write("Javascript has Quirks")

class stalinsort(animation.SortingAlgorithm):
    def sort(self):
        while not inorder(self.array,True):
            index = random.randint(0,len(self.array)-1)
            self.array[index] = 0
            self.update()
        while True:
            self.update()

class heapsort(animation.SortingAlgorithm):
    def sort(self): 
        n = len(self.array) 
    
        # Build a maxheap. 
        for i in range(n, -1, -1): 
            self.update()
            self.heapify(n, i) 
    
        # One by one extract elements 
        for i in range(n-1, 0, -1): 
            self.array[i], self.array[0] = self.array[0], self.array[i] # swap 
            self.heapify(i, 0) 
            self.update()

    def heapify(self, n, i): 
        self.update()
        largest = i # Initialize largest as root 
        l = 2 * i + 1     # left = 2*i + 1 
        r = 2 * i + 2     # right = 2*i + 2 
    
        # See if left child of root exists and is 
        # greater than root 
        if l < n and self.array[i] < self.array[l]: 
            largest = l 
    
        # See if right child of root exists and is 
        # greater than root 
        if r < n and self.array[largest] < self.array[r]: 
            largest = r 
    
        # Change root, if needed 
        if largest != i: 
            self.array[i],self.array[largest] = self.array[largest],self.array[i] # swap 
    
            # Heapify the root. 
            self.heapify(n, largest) 
        self.update()
  

class bogosort(animation.SortingAlgorithm):
    def initialize(self):
        self.scramble(8)

        self.linewidth(50)
        self.lineheightmultiplier(40)
        self.fit() 

    def sort(self):
        while not inorder(self.array):
            random.shuffle(self.array)
            self.update()

class insertionsort(animation.SortingAlgorithm):
    def sort(self):
        for index in range(1, len(self.array)):
            currentvalue = self.get(index)
            position = index

            while position>0 and self.array[position-1]>currentvalue:
                self.swap(position,position-1)
                position -= 1

            self.set(position,currentvalue)

class mergesort(animation.SortingAlgorithm):
    def sort(self):
        self.mergeSort(0,len(self.array)-1)


    def mergeSort(self,l,r): 
        if l < r: 

            # Same as (l+r)/2, but avoids overflow for 
            # large l and h 
            m = (l+(r-1))//2

            # Sort first and second halves 
            self.mergeSort(l, m) 
            self.mergeSort(m+1, r) 
            self.merge(l, m, r) 
      
    def merge(self, l, m, r): 
        n1 = m - l + 1
        n2 = r- m 
      
        # create temp arrays 
        L = [0] * (n1) 
        R = [0] * (n2) 
      
        # Copy data to temp arrays L[] and R[] 
        for i in range(0 , n1): 
            L[i] = self.get(l + i) 
      
        for j in range(0 , n2): 
            R[j] = self.get(m + 1 + j) 
      
        # Merge the temp arrays back into arr[l..r] 
        i = 0     # Initial index of first subarray 
        j = 0     # Initial index of second subarray 
        k = l     # Initial index of merged subarray 
      
        while i < n1 and j < n2 : 
            self.update()
            if L[i] <= R[j]: 
                self.set(k,L[i]) 
                i += 1
            else: 
                self.set(k, R[j]) 
                j += 1
            k += 1
      
        # Copy the remaining elements of L[], if there 
        # are any 
        while i < n1: 
            self.set(k,L[i]) 
            i += 1
            k += 1
      
        # Copy the remaining elements of R[], if there 
        # are any 
        while j < n2: 
            self.set(k, R[j]) 
            j += 1
            k += 1


class quicksort(animation.SortingAlgorithm):
    def sort(self):
        nItems = len(self.array)
        if nItems < 2:
            return
            
        todo = [(0, nItems - 1)]
        while todo:
            elem_idx, pivot_idx = low, high = todo.pop()
            self.popgetstack()
            self.popgetstack()
            elem = self.get(elem_idx, update=False)
            pivot = self.get(pivot_idx, update=False)
            
            while pivot_idx > elem_idx:
                self.update()
                if elem > pivot:
                    self.set(pivot_idx, elem)
                    pivot_idx -= 1
                    self.popgetstack()
                    elem = self.get(pivot_idx)
                    self.set(elem_idx, elem, update=False)
                else:
                    elem_idx += 1
                    self.popgetstack()
                    elem = self.get(elem_idx)
            self.set(pivot_idx, pivot,update=False)

            lsize = pivot_idx - low
            hsize = high - pivot_idx
            if lsize <= hsize:
                if 1 < lsize:
                    todo.append((pivot_idx + 1, high))
                    todo.append((low, pivot_idx - 1))
            else:
                todo.append((low, pivot_idx - 1))
            if 1 < hsize:
                todo.append((pivot_idx + 1, high))

class shellsort(animation.SortingAlgorithm):
    def sort(self):
        sublistcount = len(self.array)//2
        while sublistcount > 0:
            for startposition in range(sublistcount):
                self.gapInsertionSort(startposition,sublistcount)

            sublistcount = sublistcount // 2

    def gapInsertionSort(self,start,gap):
        for i in range(start+gap,len(self.array),gap):
            currentvalue = self.get(i)
            position = i

            while position>=gap and self.array[position-gap]>currentvalue:
                self.set(position,self.get(position-gap))
                position = position-gap

            self.set(position,currentvalue)


class bubblesort(animation.SortingAlgorithm):
    def sort(self):
        for passnum in range(len(self.array)-1,0,-1):
            for i in range(passnum):
                if self.array[i]>self.array[i+1]:
                    temp = self.array[i]
                    self.set(i, self.get(i+1))
                    self.array[i+1] = temp

class combsort(animation.SortingAlgorithm):
    def sort(self): 
        n = len(self.array) 
      
        # Initialize gap 
        gap = n 
      
        # Initialize swapped as true to make sure that 
        # loop runs 
        swapped = True
      
        # Keep running while gap is more than 1 and last 
        # iteration caused a swap 
        while gap !=1 or swapped == 1: 
      
            # Find next gap 
            gap = self.getNextGap(gap) 
      
            # Initialize swapped as false so that we can 
            # check if swap happened or not 
            swapped = False
      
            # Compare all elements with current gap 
            for i in range(0, n-gap): 
                if self.array[i] > self.array[i + gap]: 
                    self.swap(i, i+gap)
                    swapped = True

    def getNextGap(self,gap): 
        # Shrink gap by Shrink factor 
        gap = (gap * 10)/13
        if gap < 1: 
            return 1
        return int(gap)


parser = argparse.ArgumentParser(description="sorting visualiser")
parser.add_argument("algorithm",type=str,choices=[i.__name__ for i in animation.animators])
parser.add_argument("-d","--delay",type=int, default=0)
args = parser.parse_args()

if hasattr(args,"delay"):
    time.sleep(args.delay)

for i in animation.animators:
    if i.__name__ == args.algorithm:
        i(150).run()


# s = eval("{}(150)".format(sys.argv[1]))
# s.run()
