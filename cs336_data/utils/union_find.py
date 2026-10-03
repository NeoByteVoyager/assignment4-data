


class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parent = list(range(0, n))

    def find(self, a):
        if self.parent[a] == a:
            return a
        else:
            return self.find(self.parent[a])

    def union(self, a, b):
        a_root = self.find(a)
        b_root = self.find(b)
        self.parent[a_root] = b_root

    def find_roots(self):
        roots = []
        for i in range(self.n):
            if self.parent[i] == i:
                roots.append(i)

        return roots