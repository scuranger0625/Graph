import random

class UnionFind:
    """
    並查集（Union-Find）資料結構，適用於動態連通性問題，
    常用於處理群體分裂與合併、網路連線等。
    - 時間複雜度：
        * find() 與 union() 在路徑壓縮與加權合併後為 O(α(N))，幾乎視為常數。
    """
    def __init__(self, n):
        self.parent = list(range(n))  # 初始每個元素的根是自己
        self.size = [1] * n           # 每棵樹的大小預設為 1

    def find(self, x):
        """
        尋找 x 的根節點，並進行路徑壓縮。
        時間複雜度：O(α(N))，α 是阿克曼函數的反函數，極慢增長。
        """
        while x != self.parent[x]:
            self.parent[x] = self.parent[self.parent[x]]  # 路徑壓縮：讓節點跳過父節點直連到祖父節點
            x = self.parent[x]
        return x

    def union(self, x, y):
        """
        合併 x, y 所在的集合，根據大小選擇誰掛誰，避免形成高樹。
        時間複雜度：O(α(N))
        """
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return
        if self.size[root_x] < self.size[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        else:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]

    def connected(self, x, y):
        """
        檢查兩個節點是否已連通。
        時間複雜度：O(α(N))
        """
        return self.find(x) == self.find(y)

class Percolation:
    """
    模擬滲流系統：從頂部灌水，看是否能從頂部流到底部。
    適用於：
    - 水或油在岩層中的滲透模擬
    - 疾病從初始感染點蔓延至社群的條件
    - 火災是否能從森林頂端蔓延至底部
    - 網路節點連通性是否足以讓資料流通
    """
    def __init__(self, n):
        self.n = n
        self.grid = [[False] * n for _ in range(n)]  # 初始所有格子為 blocked
        self.uf = UnionFind(n * n + 2)  # 額外兩個虛擬節點：頂部與底部
        self.top_virtual = n * n
        self.bottom_virtual = n * n + 1

    def _xy_to_1d(self, row, col):
        return row * self.n + col

    def open(self, row, col):
        """
        開啟格子並與上下左右相鄰的開格子做 union 操作。
        - 最多執行 4 次 union（對角不處理）
        - 若該格位於頂部或底部，需與虛節點連結
        時間複雜度：O(1) 次 union，每次 O(α(N)) ≈ 常數
        """
        if self.grid[row][col]:
            return

        self.grid[row][col] = True
        index = self._xy_to_1d(row, col)

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            r, c = row + dx, col + dy
            if 0 <= r < self.n and 0 <= c < self.n:
                if self.grid[r][c]:
                    self.uf.union(index, self._xy_to_1d(r, c))

        if row == 0:
            self.uf.union(index, self.top_virtual)
        if row == self.n - 1:
            self.uf.union(index, self.bottom_virtual)

    def percolates(self):
        """
        檢查頂部虛節點與底部虛節點是否連通。
        時間複雜度：O(α(N))
        """
        return self.uf.connected(self.top_virtual, self.bottom_virtual)

def run_simulation(n, trials):
    """
    執行 Monte Carlo 模擬，重複多次實驗計算平均臨界滲流比例。
    時間複雜度：O(trials × N^2 × α(N))，最壞情況下開滿所有格子
    適用於：
    - 統計學模擬預估滲流閾值（percolation threshold）
    - 用於實驗不同系統下的連通性行為
    """
    total_open = 0
    for _ in range(trials):
        perc = Percolation(n)
        opened = 0
        while not perc.percolates():
            row = random.randint(0, n - 1)
            col = random.randint(0, n - 1)
            if not perc.grid[row][col]:
                perc.open(row, col)
                opened += 1
        total_open += opened / (n * n)
    return total_open / trials

# 🚀 實際執行主程式
if __name__ == "__main__":
    n = 20         # 網格大小：20x20
    trials = 50    # 模擬次數
    estimate = run_simulation(n, trials)
    print(f"平均滲流臨界比例 ≈ {estimate:.4f}")