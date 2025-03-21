# DFS 出題機器：使用 GUI 自動出題，含解題步驟說明

# 演算法提示：
# 1. 從某個頂點 v 開始
# 2. 從 v 的鄰接串列中選擇一個尚未被拜訪的頂點 w，然後繼續從 w 展開搜尋
# 3. 將目前在 v 的鄰接串列中的位置推入堆疊（push）
# 4. 當目前節點沒有任何尚未拜訪的鄰接節點時，就從堆疊中「彈出（pop）」先前儲存的位置，回到上一個節點繼續處理其鄰接串列
# 5. 為了避免重複或進入迴圈，對每個節點設定是否拜訪過的標記（例如 visited = True/False）

import random
import tkinter as tk
from tkinter import messagebox

def generate_graph():
    nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    n = random.randint(6, 8)  # 增加節點數以提高難度
    selected = random.sample(nodes, n)
    graph = {node: [] for node in selected}
    for node in selected:
        choices = [x for x in selected if x != node and x not in graph[node]]
        graph[node] = random.sample(choices, random.randint(1, min(3, len(choices))))  # 增加連接數
    return graph

def dfs_recursive(graph, node, visited, trace, steps):
    if node in visited:
        return
    visited.add(node)
    steps.append(f"拜訪節點 {node}")
    trace.append(node)
    for neighbor in graph[node]:
        steps.append(f"從 {node} 前往 {neighbor}")
        dfs_recursive(graph, neighbor, visited, trace, steps)

def generate_dfs_question():
    graph = generate_graph()
    start_node = list(graph.keys())[0]
    visited = set()
    trace = []
    steps = []
    dfs_recursive(graph, start_node, visited, trace, steps)

    options = [trace[:]]
    while len(options) < 4:
        new_trace = trace[:]
        random.shuffle(new_trace)
        if new_trace not in options:
            options.append(new_trace)
    random.shuffle(options)

    return graph, start_node, trace, options, steps

def show_question():
    graph, start, answer, options, steps = generate_dfs_question()

    for widget in frame.winfo_children():
        widget.destroy()

    hint = (
        "【DFS 演算法提示】\n"
        "1. 從某個頂點開始。\n"
        "2. 優先拜訪尚未拜訪的鄰居。\n"
        "3. 若無可走節點則回溯。\n"
        "4. 記得標記已拜訪的節點以避免循環。\n"
    )
    tk.Label(frame, text=hint, justify="left", fg="blue").pack(anchor="w", pady=(0,10))

    question = f"以下為圖的鄰接表：\n"
    for k, v in graph.items():
        question += f"{k}: {v}\n"
    question += f"\n從節點 {start} 開始使用 DFS 遞迴，請選出正確的走訪順序："

    tk.Label(frame, text=question, justify="left").pack(anchor="w")

    def check_answer(i):
        result = ""
        if options[i] == answer:
            result = f"答對了！✔\n\n[解題步驟]\n" + "\n".join(steps)
            messagebox.showinfo("結果", result)
        else:
            result = f"答錯了 ❌\n正確答案是：{answer}\n\n[解題步驟]\n" + "\n".join(steps)
            messagebox.showerror("結果", result)

    for i, opt in enumerate(options):
        btn = tk.Button(frame, text=f"({chr(65+i)}) {opt}", command=lambda i=i: check_answer(i))
        btn.pack(anchor="w")

# 建立 GUI 視窗
root = tk.Tk()
root.title("DFS 出題機器")
frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

generate_button = tk.Button(root, text="產生新題目", command=show_question)
generate_button.pack(pady=10)
show_question()

root.mainloop()
