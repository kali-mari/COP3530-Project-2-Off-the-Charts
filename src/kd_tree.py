import parser
from dataclasses import dataclass
from typing import Optional

@dataclass
class Node:
    index: int
    features: object
    axis: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None

def build_tree(tracks, depth=0):
# Input: matrix of song tracks paired with their index -> (index, [features, ...])
# Output: root node of the completed k-d tree

    if not tracks:
        return None

    # derives k dimensions from the number of features
    # axis cycles with depth
    k = len(tracks[0][1])
    axis = depth % k

    # sorts tracks by current axis and finds midpoint
    tracks = sorted(tracks, key=lambda track: track[1][axis])
    mid = len(tracks) // 2
    i, f = tracks[mid]

    return Node (
        index = i,
        features = f,
        axis = axis,

        # recursively builds the rest of the tree
        left = build_tree(tracks[:mid], depth+1),
        right = build_tree(tracks[mid+1:], depth+1)
    )

def distance(features1, features2):
# Input: list of feature statistics from two different tracks
# Output: sum of squared distances between each feature

    result = 0
    for i in range(len(features1)):
        result += (features1[i] - features2[i]) ** 2

    return result

def n_nearest(root, target, n, best=None):
# Input: root node of the tree,
#        list of target feature statistics,
#        number of nearest songs desired,
#        current nearest songs identified
# Output: list of the n nearest songs identified in reverse order,
#         last song is closest, first song is furthest

    if not root:
        return best

    if not best:
        best = []


    dist = distance(root.features, target)
    if len(best) < n:
        best.append((dist, root))
        best = sorted(best, key=lambda track: track[0])

    elif dist < best[-1][0]:
        best[-1] = (dist, root)
        best = sorted(best, key=lambda track: track[0])

    # determine which axis is being used
    axis = root.axis
    # determine which side of the tree is near vs far
    if target[axis] < root.features[axis]:
        near = root.left
        far = root.right
    else:
        near = root.right
        far = root.left

    # recursive search for nearest neighbor
    best = n_nearest(near, target, n, best)

    # determine if other side of the tree could have a closer child node
    if len(best) < n or (target[axis] - root.features[axis]) ** 2 < best[-1][0]:
        best = n_nearest(far, target, n, best)

    return best