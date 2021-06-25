# copyright 2021 Hammurabi1750BC
from collections import Counter, deque
import heapq


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def string2tree(chars2encode):
    chars2encode = Counter(chars2encode)
    heap = [[chars2encode[char], char, TreeNode(val=char)] for char in chars2encode]
    # char as unique tiebreaker if priority is not unique, else heapq crashes if it tests whether node1 > node2
    # TypeError: '<' not supported between instances of 'TreeNode' and 'TreeNode'

    heapq.heapify(heap)
    while len(heap) > 1:
        [priority_l, char_l, node_l] = heapq.heappop(heap)
        [priority_r, char_r, node_r] = heapq.heappop(heap)
        new_parent = TreeNode(val=node_l.val + node_r.val)
        new_parent.left, new_parent.right = node_l, node_r
        heapq.heappush(heap, [priority_l + priority_r, str(len(char_l + char_r)) + char_l[-1] + char_r[-1], new_parent])

    root = heap[0][2]
    return root


def recurse2encode(node, huff_dict, code_so_far):
    if node:
        if node.left or node.right:
            recurse2encode(node.left, huff_dict, code_so_far + '0')
            recurse2encode(node.right, huff_dict, code_so_far + '1')
        else:
            huff_dict[node.val] = code_so_far
    return huff_dict


def huff2encode(string2encode):
    tree = string2tree(string2encode)
    huff_dict = recurse2encode(tree, huff_dict=dict(), code_so_far='')
    encoded = ''.join([huff_dict[char] for char in string2encode])
    return encoded, tree


def huff2decode(remainder2decode, tree):
    def recurse2decode(remainder, node):
        if node.left or node.right:
            char = recurse2decode(remainder, node.left if remainder.popleft() == '0' else node.right)
        else:
            char = node.val
        return char

    decoded2date, remainder2decode = '', deque(remainder2decode)
    while remainder2decode:
        decoded2date += recurse2decode(remainder2decode, node=tree)
    return decoded2date


if __name__ == "__main__":
    for s2e in ['A_DEAD_DAD_CEDED_A_BAD_BABE_A_BEADED_ABACA_BED',  # https://en.wikipedia.org/wiki/Huffman_coding
                'Thanks for considering me for Everlaw, I really appreciate it']:

        huff_encoded, huff_tree = huff2encode(s2e)
        huff_decoded = huff2decode(huff_encoded, huff_tree)
        print(huff_encoded)
        print('original matches decoded?', s2e == huff_decoded, ':', huff_decoded)
