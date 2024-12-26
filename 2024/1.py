import numpy as np

with open('1.txt') as f:
    pairs = [(int(x) for x in line.split('   ')) for line in f]

left, right = zip(*pairs)
left, right = np.array(left), np.array(right)
left.sort()
right.sort()

dst_sum = np.abs(left - right).sum()
print(dst_sum)

right_bincount = np.bincount(right, minlength=left.max() + 1)
similarity_score = (left * right_bincount[left]).sum()
print(similarity_score)
