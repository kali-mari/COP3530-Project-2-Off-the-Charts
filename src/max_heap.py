from parser import feature_distance
 
class maxheap:
    def __init__(self):
        self.data = []
 
    def __len__(self):
        return len(self.data)
 
    def peek(self):
        return self.data[0]
 
    def push(self, item):
        self.data.append(item)
        self._sift_up(len(self.data) - 1)
 
    def pop(self):
        largest = self.data[0]
        last = self.data.pop()
        if self.data:
            self.data[0] = last
            self._sift_down(0)
        return largest
 
    def replace(self, item):
        largest = self.data[0]
        self.data[0] = item
        self._sift_down(0)
        return largest
 
    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self.data[i] > self.data[parent]:
                self.data[i], self.data[parent] = self.data[parent], self.data[i]
                i = parent
            else:
                break
 
    def _sift_down(self, i):
        n = len(self.data)
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            largest = i
 
            if left < n and self.data[left] > self.data[largest]:
                largest = left
            if right < n and self.data[right] > self.data[largest]:
                largest = right
 
            if largest == i:
                break
 
            self.data[i], self.data[largest] = self.data[largest], self.data[i]
            i = largest
 
 
def find_k_nearest(query_index, query_vector, song_vectors, k=5):
    # k nearest neighbors using a max-heap of size k
    # heap holds the k closest songs seen so far, with the farthest on top
    
    if k <= 0:
        return []
 
    heap = maxheap()
    for index, vector in song_vectors:
        if index == query_index:
            continue
 
        distance = feature_distance(query_vector, vector)
        item = (distance, index)
 
        if len(heap) < k:
            heap.push(item)
        elif distance < heap.peek()[0]:
            heap.replace(item)
 
    results = []
    while heap:
        distance, index = heap.pop()
        results.append((index, distance))
 
    results.reverse()
    return results