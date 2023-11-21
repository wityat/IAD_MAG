class ThreeHeap:
    def __init__(self):
        self.heap = []

    def parent(self, i):
        return (i - 1) // 3

    def left_child(self, i):
        return 3 * i + 1

    def middle_child(self, i):
        return 3 * i + 2

    def right_child(self, i):
        return 3 * i + 3

    def insert(self, key):
        self.heap.append(key)
        self.heapify_up(len(self.heap) - 1)

    def heapify_up(self, i):
        while i != 0 and self.heap[self.parent(i)] > self.heap[i]:
            self.heap[i], self.heap[self.parent(i)] = self.heap[self.parent(i)], self.heap[i]
            i = self.parent(i)

    def extract_min(self):
        if not self.heap:
            return None
        root = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self.heapify_down(0)
        return root

    def heapify_down(self, i):
        smallest = i
        l = self.left_child(i)
        m = self.middle_child(i)
        r = self.right_child(i)
        if l < len(self.heap) and self.heap[l] < self.heap[smallest]:
            smallest = l
        if m < len(self.heap) and self.heap[m] < self.heap[smallest]:
            smallest = m
        if r < len(self.heap) and self.heap[r] < self.heap[smallest]:
            smallest = r
        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self.heapify_down(smallest)


class Node:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = None
        self.child = None
        self.sibling = None


class BinomialHeap:
    def __init__(self):
        self.head = None

    def merge(self, h1, h2):
        if h1 is None:
            return h2
        if h2 is None:
            return h1
        if h1.degree < h2.degree:
            h1.sibling = self.merge(h1.sibling, h2)
            return h1
        else:
            h2.sibling = self.merge(h1, h2.sibling)
            return h2

    def union(self, h2):
        self.head = self.merge(self.head, h2.head)
        if self.head is None:
            return
        prev_x = None
        x = self.head
        next_x = x.sibling
        while next_x is not None:
            if x.degree != next_x.degree or (next_x.sibling is not None and next_x.sibling.degree == x.degree):
                prev_x = x
                x = next_x
            elif x.key <= next_x.key:
                x.sibling = next_x.sibling
                self.link(next_x, x)
            else:
                if prev_x is None:
                    self.head = next_x
                else:
                    prev_x.sibling = next_x
                self.link(x, next_x)
                x = next_x
            next_x = x.sibling

    def link(self, y, z):
        y.parent = z
        y.sibling = z.child
        z.child = y
        z.degree += 1

    def insert(self, key):
        h = BinomialHeap()
        h.head = Node(key)
        self.union(h)

    def get_min(self):
        if self.head is None:
            return None
        y = self.head
        x = y.sibling
        min = y.key
        while x is not None:
            if x.key < min:
                y = x
                min = x.key
            x = x.sibling
        return min

    def extract_min(self):
        if self.head is None:
            return None
        min = self.get_min()
        prev_x = None
        x = self.head
        while x.key != min:
            prev_x = x
            x = x.sibling
        if prev_x is None:
            self.head = x.sibling
        else:
            prev_x.sibling = x.sibling
        h = BinomialHeap()
        h.head = x.child
        child = x.child
        while child is not None:
            child.parent = None
            child = child.sibling
        self.union(h)
        return min
