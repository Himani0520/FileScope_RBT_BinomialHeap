import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from datetime import datetime
import humanize
import threading

# ---------------- BINOMIAL HEAP ----------------
class BinomialNode:
    def __init__(self, key, path):
        self.key = key
        self.path = path
        self.name = os.path.basename(path) if path else ""
        self.parent = None
        self.child = None
        self.sibling = None
        self.degree = 0

class BinomialHeap:
    def __init__(self):
        self.head = None

    def merge_root_lists(self, h1, h2):
        if not h1: return h2
        if not h2: return h1
        if h1.degree <= h2.degree:
            head = h1; h1 = h1.sibling
        else:
            head = h2; h2 = h2.sibling
        tail = head
        while h1 and h2:
            if h1.degree <= h2.degree:
                tail.sibling = h1
                h1 = h1.sibling
            else:
                tail.sibling = h2
                h2 = h2.sibling
            tail = tail.sibling
        tail.sibling = h1 if h1 else h2
        return head

    def link(self, y, z):
        y.parent = z
        y.sibling = z.child
        z.child = y
        z.degree += 1

    def union(self, other):
        new_head = self.merge_root_lists(self.head, other.head)
        if not new_head:
            self.head = None
            return
        prev = None
        curr = new_head
        nex = curr.sibling
        while nex:
            if (curr.degree != nex.degree) or (nex.sibling and nex.sibling.degree == curr.degree):
                prev = curr
                curr = nex
            elif curr.key <= nex.key:
                curr.sibling = nex.sibling
                self.link(nex, curr)
            else:
                if prev:
                    prev.sibling = nex
                else:
                    new_head = nex
                self.link(curr, nex)
                curr = nex
            nex = curr.sibling
        self.head = new_head

    def insert(self, key, path):
        node = BinomialNode(key, path)
        tmp = BinomialHeap(); tmp.head = node
        self.union(tmp)

    def get_min(self):
        if not self.head: return None
        mn = self.head
        x = self.head.sibling
        while x:
            if x.key < mn.key: mn = x
            x = x.sibling
        return mn

    def extract_min(self):
        if not self.head: return None
        prev_min = None
        min_node = self.head
        curr = self.head
        while curr.sibling:
            if curr.sibling.key < min_node.key:
                min_node = curr.sibling
                prev_min = curr
            curr = curr.sibling

        if prev_min:
            prev_min.sibling = min_node.sibling
        else:
            self.head = min_node.sibling

        child = min_node.child
        prev_child = None
        while child:
            nxt = child.sibling
            child.sibling = prev_child
            child.parent = None
            prev_child = child
            child = nxt

        tmp = BinomialHeap()
        tmp.head = prev_child
        self.union(tmp)

        return min_node

# ---------------- RBT ----------------
class FileNode:
    def __init__(self, path, size, is_nil=False):
        self.key = size
        self.path = path
        self.name = os.path.basename(path) if path else ""
        self.modified_time = 0 if is_nil else (os.path.getmtime(path) if path else 0)
        self.left = None; self.right = None; self.parent = None
        self.color = "RED"

class FileSystemTree:
    def __init__(self):
        self.NIL = FileNode("", 0, is_nil=True)
        self.NIL.color = "BLACK"
        self.root = self.NIL

    def left_rotate(self, x):
        y = x.right; x.right = y.left
        if y.left != self.NIL: y.left.parent = x
        y.parent = x.parent
        if x.parent is None: self.root = y
        elif x == x.parent.left: x.parent.left = y
        else: x.parent.right = y
        y.left = x; x.parent = y

    def right_rotate(self, x):
        y = x.left; x.left = y.right
        if y.right != self.NIL: y.right.parent = x
        y.parent = x.parent
        if x.parent is None: self.root = y
        elif x == x.parent.right: x.parent.right = y
        else: x.parent.left = y
        y.right = x; x.parent = y

    def insert(self, path, size):
        node = FileNode(path, size); node.left = self.NIL; node.right = self.NIL
        y = None; x = self.root
        while x != self.NIL:
            y = x
            if node.key < x.key: x = x.left
            else: x = x.right
        node.parent = y
        if y is None: self.root = node
        elif node.key < y.key: y.left = node
        else: y.right = node
        self.insert_fixup(node)

    def insert_fixup(self, k):
        while k.parent and k.parent.color == "RED":
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u and u.color == "RED":
                    u.color = "BLACK"; k.parent.color = "BLACK"; k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent; self.right_rotate(k)
                    k.parent.color = "BLACK"; k.parent.parent.color = "RED"
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u and u.color == "RED":
                    u.color = "BLACK"; k.parent.color = "BLACK"; k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent; self.left_rotate(k)
                    k.parent.color = "BLACK"; k.parent.parent.color = "RED"
                    self.right_rotate(k.parent.parent)
            if k == self.root: break
        self.root.color = "BLACK"

    def find_largest_file(self):
        node = self.root
        while node != self.NIL and node.right != self.NIL:
            node = node.right
        return node if node != self.NIL else None

    def find_most_recent_file(self):
        return self._find_most_recent_file_recursive(self.root, None)

    def _find_most_recent_file_recursive(self, node, current_latest):
        if node == self.NIL: return current_latest
        if current_latest is None or node.modified_time > current_latest.modified_time:
            current_latest = node
        current_latest = self._find_most_recent_file_recursive(node.left, current_latest)
        return self._find_most_recent_file_recursive(node.right, current_latest)

# ---------------- GUI ----------------
class DualExplorerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RBT + Binomial Heap Visualizer")

        self.tree = FileSystemTree()
        self.heap = BinomialHeap()

        self.selected_path = None
        self.sort_option = tk.StringVar(value="Size Asc")
        self.search_var = tk.StringVar()
        self.all_nodes = []

        self.setup_gui()
        self.root.bind("<Configure>", lambda e: self.draw_all())

    def setup_gui(self):
        ctrl = ttk.Frame(self.root, padding=6); ctrl.pack(fill=tk.X)

        ttk.Button(ctrl, text="Select Directory", command=self.select_directory).pack(side=tk.LEFT, padx=4)
        ttk.Button(ctrl, text="Find Largest File (RBT)", command=self.find_largest_file).pack(side=tk.LEFT, padx=4)
        ttk.Button(ctrl, text="Find Most Recent (RBT)", command=self.find_most_recent_file).pack(side=tk.LEFT, padx=4)
        ttk.Button(ctrl, text="Find Smallest (Heap)", command=self.find_smallest_file).pack(side=tk.LEFT, padx=4)
        ttk.Button(ctrl, text="Extract Smallest (Heap)", command=self.extract_smallest).pack(side=tk.LEFT, padx=4)

        ttk.Entry(ctrl, textvariable=self.search_var, width=20).pack(side=tk.LEFT, padx=4)
        ttk.Button(ctrl, text="Search", command=self.search_file).pack(side=tk.LEFT, padx=4)

        sort_box = ttk.Combobox(ctrl, textvariable=self.sort_option, width=15)
        sort_box['values'] = ["Size Asc", "Size Desc", "Date Modified"]
        sort_box.pack(side=tk.LEFT, padx=4)
        sort_box.bind("<<ComboboxSelected>>", lambda e: self.update_list())

        self.progress_var = tk.DoubleVar()
        ttk.Progressbar(ctrl, variable=self.progress_var, maximum=100).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)

        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL); paned.pack(fill=tk.BOTH, expand=True)
        left_frame = ttk.Frame(paned); right_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=3); paned.add(right_frame, weight=2)

        self.canvas_rbt = tk.Canvas(left_frame, bg='white'); self.canvas_rbt.pack(fill=tk.BOTH, expand=True)
        self.canvas_heap = tk.Canvas(right_frame, bg='white', height=300); self.canvas_heap.pack(fill=tk.BOTH)

        self.tree_view = ttk.Treeview(right_frame, columns=("name","size","modified"), show="headings")
        for col in ("name","size","modified"):
            self.tree_view.heading(col, text=col.capitalize())
        self.tree_view.pack(fill=tk.BOTH, expand=True)
        self.tree_view.bind("<<TreeviewSelect>>", self.on_select)

        self.details_label = ttk.Label(right_frame, text="Select a file", anchor="w", justify="left")
        self.details_label.pack(fill=tk.X)

        self.stats_label = ttk.Label(right_frame, text="", anchor="w", justify="left")
        self.stats_label.pack(fill=tk.X)

    def select_directory(self):
        d = filedialog.askdirectory()
        if d:
            threading.Thread(target=self.scan_directory, args=(d,), daemon=True).start()

    def scan_directory(self, directory):
        files = [os.path.join(r, f) for r, _, fs in os.walk(directory) for f in fs]
        total = len(files)
        self.tree = FileSystemTree(); self.heap = BinomialHeap()
        self.all_nodes = []

        for i, p in enumerate(files, 1):
            try:
                size = os.path.getsize(p)
                self.tree.insert(p, size)
                self.heap.insert(size, p)
                self.all_nodes.append((p, size))
            except: pass
            self.progress_var.set((i/total)*100)

        self.update_stats()
        self.draw_all()
        self.update_list()

    def update_stats(self):
        if not self.all_nodes: return
        total_files = len(self.all_nodes)
        total_size = sum(s for _, s in self.all_nodes)
        largest = max(self.all_nodes, key=lambda x: x[1])
        smallest = min(self.all_nodes, key=lambda x: x[1])

        self.stats_label.config(text=f"""
Files: {total_files}
Total Size: {humanize.naturalsize(total_size)}
Largest: {os.path.basename(largest[0])}
Smallest: {os.path.basename(smallest[0])}
""")

    def search_file(self):
        keyword = self.search_var.get().lower()
        for item in self.tree_view.get_children():
            name = self.tree_view.item(item)["values"][0].lower()
            if keyword in name:
                self.tree_view.selection_set(item)
                self.tree_view.see(item)
                break

    def on_select(self, event):
        selected = self.tree_view.selection()
        if not selected: return
        item = selected[0]
        path = self.tree_view.item(item, "tags")[0]
        self.selected_path = path
        self.show_details(path)
        self.draw_all()

    def show_details(self, path):
        size = humanize.naturalsize(os.path.getsize(path))
        mod = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")

        self.details_label.config(text=f"""
Name: {os.path.basename(path)}
Size: {size}
Path: {path}
Modified: {mod}
""")

    def update_list(self):
        for i in self.tree_view.get_children():
            self.tree_view.delete(i)

        nodes = []
        self._collect_nodes(self.tree.root, nodes)

        option = self.sort_option.get()
        if option == "Size Desc":
            nodes.sort(key=lambda x: x.key, reverse=True)
        elif option == "Date Modified":
            nodes.sort(key=lambda x: x.modified_time, reverse=True)
        else:
            nodes.sort(key=lambda x: x.key)

        for node in nodes:
            size = humanize.naturalsize(node.key)
            mod = datetime.fromtimestamp(node.modified_time).strftime("%Y-%m-%d %H:%M:%S")
            self.tree_view.insert("", tk.END, values=(node.name, size, mod), tags=(node.path,))

    def _collect_nodes(self, node, arr):
        if node == self.tree.NIL: return
        self._collect_nodes(node.left, arr)
        arr.append(node)
        self._collect_nodes(node.right, arr)

    def draw_all(self):
        self.canvas_rbt.delete("all")
        self.canvas_heap.delete("all")

        if self.tree.root and self.tree.root != self.tree.NIL:
            self.draw_rbt_node(self.tree.root, 600, 30, 300)

        node = self.heap.head
        x = 100
        while node:
            self.draw_heap_tree(node, x, 60)
            x += 200
            node = node.sibling

    def draw_rbt_node(self, node, x, y, dx):
        if node == self.tree.NIL: return
        fill = "blue" if node.path == self.selected_path else ("red" if node.color=="RED" else "black")
        self.canvas_rbt.create_oval(x-18,y-18,x+18,y+18, fill=fill)
        self.canvas_rbt.create_text(x,y,text=node.name[:6], fill="white")
        if node.left != self.tree.NIL:
            self.canvas_rbt.create_line(x,y,x-dx,y+70)
            self.draw_rbt_node(node.left, x-dx, y+70, dx//2)
        if node.right != self.tree.NIL:
            self.canvas_rbt.create_line(x,y,x+dx,y+70)
            self.draw_rbt_node(node.right, x+dx, y+70, dx//2)

    def draw_heap_tree(self, node, x, y):
        if not node: return
        self.canvas_heap.create_oval(x-18,y-18,x+18,y+18, fill="orange")
        self.canvas_heap.create_text(x,y,text=node.name[:6], fill="white")
        c = node.child; cx = x - 60; cy = y + 90
        while c:
            self.canvas_heap.create_line(x, y, cx, cy)
            self.draw_heap_tree(c, cx, cy)
            cx += 100
            c = c.sibling

    def find_largest_file(self):
        n = self.tree.find_largest_file()
        if n: messagebox.showinfo("Largest", n.path)

    def find_most_recent_file(self):
        n = self.tree.find_most_recent_file()
        if n: messagebox.showinfo("Recent", n.path)

    def find_smallest_file(self):
        n = self.heap.get_min()
        if n: messagebox.showinfo("Smallest", n.path)

    def extract_smallest(self):
        n = self.heap.extract_min()
        if n:
            messagebox.showinfo("Extracted", n.path)
            self.draw_all()

# RUN
if __name__ == "__main__":
    root = tk.Tk()
    app = DualExplorerGUI(root)
    root.geometry("1200x800")
    root.mainloop()