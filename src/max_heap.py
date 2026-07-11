import heapq
from parser import feature_distance, build_index_feature_pairs

def find_k_nearest(query_index, query_vector, song_vectors, k=5):
    # k nearest neighbors using a max-heap of size k
    # heap holds the k closest songs seen so far, with the farthest on top

    if k <= 0:
        return []

    heap = []
    for index, vector in song_vectors:
        if index == query_index:
            continue

        distance = feature_distance(query_vector, vector)
        heap_item = (-distance, index)

        if len(heap) < k:
            heapq.heappush(heap, heap_item)
        elif distance < -heap[0][0]:
            heapq.heapreplace(heap, heap_item)

    results = []
    while heap:
        neg_distance, index = heapq.heappop(heap)
        results.append((index, -neg_distance))

    results.reverse()
    return results