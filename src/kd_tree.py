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

    if not tracks:
        return None

    k = len(tracks[0][1])
    axis = depth % k

    tracks = sorted(tracks, key=lambda track: track[1][axis])
    mid = len(tracks) // 2
    i, f = tracks[mid]

    return Node (
        index = i,
        features = f,
        axis = axis,
        left = build_tree(tracks[:mid], depth+1),
        right = build_tree(tracks[mid+1:], depth+1)
    )

def distance(features1, features2):

    result = 0
    for i in range(len(features1)):
        result += (features1[i] - features2[i]) ** 2

    return result

def nearest(root, target, best=None):

    if not root:
        return best

    if not best or distance(root.features, target) < distance(target, best.features):
        best = root

    axis = root.axis
    if target[axis] < root.features[axis]:
        near = root.left
        far = root.right
    else:
        near = root.right
        far = root.left

    best = nearest(near, target, best)

    if (target[axis] - root.features[axis]) ** 2 < distance(best.features, target):
        best = nearest(far, target, best)

    return best



df = parser.load_data()
matrix = parser.get_feature_matrix(df)
tracks = list(enumerate(matrix))

build_tree(tracks)