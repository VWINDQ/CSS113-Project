import streamlit as st
import networkx as nx
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config
import heapq  # Imported at top level for better practice

# --------------------------
# 1. Testcase Definitions
# --------------------------
SCALE = 200 

TESTCASES = {
    "DFS/BFS: 3x3 Grid": {
        "nodes": ["a", "b", "c", "d", "e", "f", "g", "h", "i"],
        "edges": [
            # แนวนอน
            ("a", "b", 1), ("b", "c", 1),
            ("h", "i", 1), ("i", "d", 1),
            ("g", "f", 1), ("f", "e", 1),
            # แนวตั้ง
            ("a", "h", 1), ("h", "g", 1),
            ("b", "i", 1), ("i", "f", 1),
            ("c", "d", 1), ("d", "e", 1)
        ],
        "pos": {
            # แถวบน
            "a": (-2*SCALE, -2*SCALE), "b": (0, -2*SCALE), "c": (2*SCALE, -2*SCALE),
            # แถวกลาง
            "h": (-2*SCALE, 0),        "i": (0, 0),        "d": (2*SCALE, 0),
            # แถวล่าง
            "g": (-2*SCALE, 2*SCALE),  "f": (0, 2*SCALE),  "e": (2*SCALE, 2*SCALE)
        }
    },
    "DFS/BFS: Hexagon/Grid": {
        "nodes": ["a", "b", "c", "d", "e", "f", "g"],
        "edges": [
            ("a", "b", 1), ("a", "f", 1),
            ("b", "c", 1), ("b", "g", 1), ("b", "f", 1),
            ("c", "d", 1), ("c", "g", 1), ("c", "e", 1),
            ("d", "e", 1),
            ("e", "f", 1), ("e", "g", 1),
            ("f", "g", 1)
        ],
        "pos": {
            "a": (-2*SCALE, 0), "b": (-1*SCALE, -1*SCALE), "f": (-1*SCALE, 1*SCALE),
            "g": (0, 0),
            "c": (1*SCALE, -1*SCALE), "e": (1*SCALE, 1*SCALE), "d": (2*SCALE, 0)
        }
    },
    "DFS/BFS: Pentagon Star": {
        "nodes": ["A", "B", "C", "D", "E"],
        "edges": [
            ("A", "B", 1), ("A", "C", 1), ("A", "D", 1), ("A", "E", 1),
            ("B", "C", 1), ("B", "D", 1), ("B", "E", 1),
            ("C", "D", 1), ("C", "E", 1),
            ("D", "E", 1)
        ],
        "pos": {
            "A": (0, -2*SCALE), "B": (1.9*SCALE, -0.6*SCALE), "C": (1.2*SCALE, 1.5*SCALE),
            "D": (-1.2*SCALE, 1.5*SCALE), "E": (-1.9*SCALE, -0.6*SCALE)
        }
    },
    "DFS/BFS: Composite (Square + Rect)": {
        "nodes": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"],
        "edges": [
            ("a", "b", 1), ("b", "c", 1), ("c", "d", 1), ("d", "a", 1), ("b", "d", 1), 
            ("c", "e", 1), ("c", "g", 1), ("e", "f", 1), ("f", "g", 1), ("e", "g", 1), 
            ("g", "j", 1), ("j", "i", 1), ("i", "h", 1), ("h", "g", 1), 
            ("g", "k", 1), ("j", "k", 1), ("i", "k", 1), ("h", "k", 1)  
        ],
        "pos": {
            "a": (-3*SCALE, -1*SCALE), "b": (-1*SCALE, -1*SCALE), 
            "d": (-3*SCALE, 1*SCALE), "c": (-1*SCALE, 1*SCALE),
            "e": (-1*SCALE, 3*SCALE), "f": (1*SCALE, 3*SCALE), "g": (1*SCALE, 1*SCALE),
            "j": (1*SCALE, -1*SCALE), "i": (3*SCALE, -1*SCALE), "h": (3*SCALE, 1*SCALE),
            "k": (2*SCALE, 0)
        }
    },
      "DFS/BFS: Start A to K": {
        "nodes": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
        "edges": [
            # --- แก้ไขเส้นเชื่อมให้ตรงภาพซ้ายเป๊ะๆ ---
            ("A", "B", 3), ("A", "C", 4), ("A", "F", 5), # A ไป F (ไม่ใช่ D)
            
            ("B", "D", 6), ("B", "J", 8),
            ("C", "F", 3),
            
            ("D", "E", 3), ("D", "G", 5), ("D", "H", 6),
            ("E", "G", 4),
            
            ("F", "H", 8), ("F", "K", 7),
            
            ("G", "J", 8), ("G", "I", 2),
            ("H", "I", 7),
            
            ("I", "J", 6),
            ("J", "K", 8)
        ],
        "pos": {
            # ยอด A (กลางบน)
            "A": (0.5*SCALE, -3.0*SCALE),
            
            # ปีกซ้าย (B และ J เฉียงออกไปทางซ้าย)
            "B": (-2.5*SCALE, -1.5*SCALE), 
            "J": (-2.8*SCALE, 3.0*SCALE),
            
            # ปีกขวา (C, F, K เฉียงออกไปทางขวา)
            "C": (3.0*SCALE, -1.5*SCALE),
            "F": (3.5*SCALE, 0.5*SCALE),   # F ขยับออกขวาให้เส้น A->F เฉียงสวยๆ
            "K": (3.5*SCALE, 3.0*SCALE),
            
            # โซนกลาง (D, E)
            "D": (0.2*SCALE, -0.5*SCALE),  # D อยู่ต่ำกว่า B นิดหน่อย
            "E": (-1.5*SCALE, 0.2*SCALE),  # E อยู่ซ้าย D
            
            # โซนล่างใน (G, H, I)
            "G": (-0.8*SCALE, 1.8*SCALE),  # G อยู่ระหว่าง E กับ I
            "H": (1.8*SCALE, 1.5*SCALE),   # H อยู่ขวา
            "I": (0.8*SCALE, 2.5*SCALE)    # I อยู่เหนือเส้น J-K นิดนึง
        }
    },
    "Dijkstra: Start a to e": {
        "nodes": ["a", "b", "c", "d", "e"],
        "edges": [
            ("a", "b", 4), ("a", "c", 2),
            ("b", "c", 1), ("b", "d", 5),
            ("c", "d", 8), ("c", "e", 10),
            ("d", "e", 2)
        ],
        "pos": {
            "a": (-2*SCALE, 0),
            "b": (0, 1*SCALE), "c": (0, -1*SCALE),
            "d": (2*SCALE, 1*SCALE), "e": (2*SCALE, -1*SCALE)
        }
    },
    "Dijkstra: Start a to d": {
        "nodes": ["a", "b", "c", "d", "e"],
        "edges": [
            ("a", "b", 6), ("a", "c", 7), ("a", "e", 5),
            ("b", "c", 2),
            ("c", "e", 1), ("c", "d", 3),
            ("e", "d", 2)
        ],
        "pos": {
            "b": (0, -2.5*SCALE),          
            "a": (-2.5*SCALE, 0),          
            "c": (2.5*SCALE, 0),           
            "e": (-1.5*SCALE, 2.5*SCALE),  
            "d": (1.5*SCALE, 2.5*SCALE)    
        }
    },
    "Dijkstra: Start a to f": {
        "nodes": ["a", "b", "c", "d", "e", "f"],
        "edges": [
            ("a", "b", 10), ("a", "c", 5),
            ("b", "c", 3), ("b", "d", 2),
            ("c", "e", 9),
            ("d", "e", 4), ("d", "f", 6),
            ("e", "f", 7)
        ],
        "pos": {
            "a": (-3*SCALE, 0),            
            "b": (-1*SCALE, -2*SCALE),     
            "c": (-1*SCALE, 2*SCALE),      
            "d": (1*SCALE, -0.5*SCALE),    
            "f": (3*SCALE, -0.5*SCALE),    
            "e": (3*SCALE, 2*SCALE)        
        }
    },
    "Dijkstra: Weighted Shortest Path": {
        "nodes": ["S", "A", "B", "C", "D", "E", "F", "T"],
        "edges": [
            ("S", "A", 2), ("S", "B", 5), ("S", "C", 3),
            ("A", "B", 2), ("A", "D", 6),
            ("B", "D", 3), ("B", "E", 3), ("B", "C", 2), ("B", "F", 6),
            ("C", "F", 7),
            ("D", "E", 3), ("D", "T", 6),
            ("E", "F", 3), ("E", "T", 2),
            ("F", "T", 4)
        ],
        "pos": {
            "S": (-3*SCALE, 0),
            "A": (-1*SCALE, -2*SCALE), "B": (-1*SCALE, 0), "C": (-1*SCALE, 2*SCALE),
            "D": (1*SCALE, -2*SCALE), "E": (1*SCALE, 0), "F": (1*SCALE, 2*SCALE),
            "T": (3*SCALE, 0)
        }
    },
    "MST: Hexagon & Center": {
        "nodes": ["a", "b", "c", "d", "e", "f", "g"],
        "edges": [
            # รอบนอก
            ("a", "b", 2), ("b", "c", 3), ("c", "d", 5),
            ("d", "e", 4), ("e", "f", 2), ("f", "a", 3),
            # เส้นผ่าศูนย์กลางแนวตั้ง
            ("b", "f", 4), ("c", "e", 3),
            # จุดศูนย์กลาง g
            ("g", "b", 3), ("g", "c", 4), ("g", "e", 3), ("g", "f", 5)
        ],
        "pos": {
            "g": (0, 0),                # กลาง
            "a": (-3*SCALE, 0),         # ซ้ายสุด
            "d": (3*SCALE, 0),          # ขวาสุด
            "b": (-1.5*SCALE, -2*SCALE), # บนซ้าย
            "c": (1.5*SCALE, -2*SCALE),  # บนขวา
            "f": (-1.5*SCALE, 2*SCALE),  # ล่างซ้าย
            "e": (1.5*SCALE, 2*SCALE)    # ล่างขวา
        }
    },
    "MST: Pentagon Star": {
        "nodes": ["a", "b", "c", "d", "e"],
        "edges": [
            # รอบนอก
            ("a", "b", 3), ("b", "c", 5), ("c", "d", 5),
            ("d", "e", 6), ("e", "a", 4),
            # ดาวภายใน (Star)
            ("b", "e", 8), ("b", "d", 11),
            ("c", "a", 4), ("c", "e", 8),
            ("d", "a", 9)
        ],
        "pos": {
            # c: ยอดบนสุด (ในรูปเขียน b แต่แก้เป็น c)
            "c": (0, -2.5*SCALE),           
            
            # b: ปีกซ้าย
            "b": (-2.5*SCALE, -0.8*SCALE), 
            
            # d: ปีกขวา
            "d": (2.5*SCALE, -0.8*SCALE),   
            
            # a: ล่างซ้าย
            "a": (-1.5*SCALE, 2.5*SCALE),   
            
            # e: ล่างขวา
            "e": (1.5*SCALE, 2.5*SCALE)     
        }
    },
    "MST: Rectangle & Cross": {
        "nodes": ["a", "b", "c", "d", "e"], # d คือ D ในรูป
        "edges": [
            # กรอบสี่เหลี่ยม
            ("a", "b", 1), # บน
            ("b", "c", 2), # ขวา
            ("c", "d", 3), # ล่าง
            ("d", "a", 2), # ซ้าย
            # เส้นทแยงมุมเข้าหา e
            ("a", "e", 3), 
            ("b", "e", 2),
            ("c", "e", 4),
            ("d", "e", 1)
        ],
        "pos": {
            "e": (0, 0),               # e: จุดกึ่งกลาง
            
            "a": (-2*SCALE, -1.5*SCALE), # a: บนซ้าย
            "b": (2*SCALE, -1.5*SCALE),  # b: บนขวา
            
            "d": (-2*SCALE, 1.5*SCALE),  # D: ล่างซ้าย
            "c": (2*SCALE, 1.5*SCALE)    # c: ล่างขวา
        }
    },
    "MST: House Shape": {
        "nodes": ["a", "b", "c", "d", "e"],
        "edges": [
            # หลังคา
            ("a", "b", 1), ("a", "e", 2),
            # คานขวาง
            ("b", "e", 3),
            # กำแพง/พื้น
            ("b", "c", 3), ("c", "d", 3), ("d", "e", 1),
            # เส้นกากบาทภายใน
            ("b", "d", 4), 
            ("c", "e", 2)
        ],
        "pos": {
            "a": (0, -3*SCALE),          # a: ยอดหลังคา
            
            "b": (-2*SCALE, -1*SCALE),   # b: มุมหลังคาซ้าย
            "e": (2*SCALE, -1*SCALE),    # e: มุมหลังคาขวา
            
            "c": (-2*SCALE, 2*SCALE),    # c: ฐานซ้าย
            "d": (2*SCALE, 2*SCALE)      # d: ฐานขวา
        }
    },
    "MST: Complex Bridge": {
        "nodes": ["L", "A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3", "R"],
        "edges": [
            # --- ซ้ายสุด (L) ---
            ("L", "A1", 1), ("L", "A2", 2), ("L", "A3", 3),

            # --- แถวตั้ง 1 (A) ---
            ("A1", "A2", 3), ("A2", "A3", 5),

            # --- เชื่อม A ไป B ---
            ("A1", "B1", 4), # บน-บน
            ("A2", "B2", 2), # กลาง-กลาง
            ("A3", "B3", 5), # ล่าง-ล่าง
            ("A1", "B2", 5), # ทแยงลง (บนไปกลาง)
            ("A3", "B2", 4), # ทแยงขึ้น (ล่างไปกลาง)

            # --- แถวตั้ง 2 (B) ---
            ("B1", "B2", 3), ("B2", "B3", 3),

            # --- เชื่อม B ไป C ---
            ("B1", "C1", 4), # บน-บน
            ("B2", "C2", 3), # กลาง-กลาง
            ("B3", "C3", 4), # ล่าง-ล่าง
            ("B2", "C1", 2), # ทแยงลง (บนไปกลาง)
            
            # >>> บรรทัดนี้ครับที่น่าจะหายไปในรอบก่อน <<<
            ("B2", "C3", 2), # ทแยงลง (กลางไปล่าง) 
            # >>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<

            # --- แถวตั้ง 3 (C) ---
            ("C1", "C2", 5), ("C2", "C3", 4),

            # --- ขวาสุด (R) ---
            ("C1", "R", 4), ("C2", "R", 3), ("C3", "R", 4)
        ],
        "pos": {
            # ใช้สเกลกว้าง เพื่อให้เห็นเส้นชัดเจน
            "L": (-4.5*SCALE, 0),

            "A1": (-2.5*SCALE, -1.5*SCALE), "A2": (-2.5*SCALE, 0), "A3": (-2.5*SCALE, 1.5*SCALE),

            "B1": (0, -1.5*SCALE),          "B2": (0, 0),          "B3": (0, 1.5*SCALE),

            "C1": (2.5*SCALE, -1.5*SCALE),  "C2": (2.5*SCALE, 0),  "C3": (2.5*SCALE, 1.5*SCALE),

            "R": (4.5*SCALE, 0)
        }
    }
}


# --------------------------
# 2. Helper Classes & Functions
# --------------------------

class GraphAlgorithms:
    def __init__(self, G):
        self.G = G

    def get_dfs_steps(self, start_node):
        steps = [] # 1. สร้างลิสต์ว่าง ไว้เก็บขั้นตอนการทำงาน (เพื่อเอาไปทำ Animation)
        visited = set() # 2. สร้างเซต (Set) ไว้จดว่าโหนดไหน "ไปมาแล้ว" (ป้องกันการเดินวนเป็นวงกลม)
        traversal_order = [] # 3. สร้างลิสต์ไว้เก็บลำดับโหนดที่ไปเยือนจริง ๆ (เพื่อสรุปผลตอนจบ)
        def dfs(u): # 4. นิยามฟังก์ชันย่อยชื่อ dfs รับพารามิเตอร์ u (โหนดปัจจุบัน)
            visited.add(u) # 5. ประทับตราว่า "ถึงโหนด u แล้วนะ" ลงในสมุดบันทึก visited
            traversal_order.append(u) # 6. เพิ่ม u เข้าไปในลิสต์สรุปผล
            steps.append(("node", u, f"Visit Node {u}")) # 7. บันทึก Step: บอกระบบกราฟว่า "ตอนนี้อยู่ที่โหนด u" (สีจะเปลี่ยน)
            for v in self.G.neighbors(u): # 8. Loop เพื่อนบ้าน: วนลูปเช็กเพื่อนบ้าน (v) ทุกคนที่เชื่อมกับ u
                if v not in visited: # 9. ถ้าเพื่อนคนนี้ (v) ยังไม่เคยไปหา (ไม่อยู่ใน visited)
                    steps.append(("edge", (u, v), f"Explore Edge {u}-{v}")) # 10. บันทึก Step: บอกระบบกราฟว่า "กำลังจะวิ่งผ่านเส้น u->v" (เส้นจะไฮไลต์)
                    dfs(v) # 11. ***สำคัญที่สุด*** เรียกฟังก์ชัน dfs(v) ซ้ำ! (กระโดดไปที่ v แล้วทำข้อ 4 ใหม่)
        if start_node: # 12. เริ่มต้นกระบวนการทั้งหมด โดยเรียก dfs ใส่จุดเริ่มต้นเข้าไป
            dfs(start_node)
        return steps, traversal_order # 13. ส่งคืนขั้นตอนทั้งหมด และลำดับการเดิน

    def get_bfs_steps(self, start_node):
        steps = []
        visited = set()
        traversal_order = []
        queue = [start_node] # 4. ***หัวใจของ BFS*** สร้างคิว และใส่จุดเริ่มต้นเข้าไปเป็นคนแรก
        visited.add(start_node) # 5. ประทับตราทันทีว่าจุดเริ่มต้น "จองแล้ว" (กันคนอื่นใส่ซ้ำเข้าคิว)
        steps.append(("node", start_node, f"Start at {start_node}")) # 6. บันทึก Step แรก: เริ่มที่จุด start
        
        while queue: # 7. วนลูป "ตราบใดที่ในคิวยังมีโหนดเหลืออยู่" (ถ้าคิวว่างคือจบ)
            u = queue.pop(0) # 8. ***สำคัญ*** ดึงโหนด "คนแรกสุด" ออกจากคิว (First-In, First-Out) มาเป็น u
            traversal_order.append(u) # 9. บันทึกว่าเรา process โหนด u แล้ว
            for v in self.G.neighbors(u): # 10. Loop เพื่อนบ้าน: ดูเพื่อน (v) ทุกคนของ u
                if v not in visited: # 11. ถ้าเพื่อนคนนี้ (v) ยังไม่เคยถูกจอง (ไม่อยู่ใน visited)
                    visited.add(v) # 12. รีบจองทันที! (Mark visited) เพื่อไม่ให้โหนดอื่นใส่ v เข้าคิวซ้ำ
                    steps.append(("edge", (u, v), f"Discover Edge {u}-{v}")) # 13. บันทึก Step: โชว์เส้นเชื่อม u->v
                    steps.append(("node", v, f"Visit Node {v}")) # 14. บันทึก Step: โชว์ว่าเจอโหนด v แล้ว
                    queue.append(v) # 15. ***สำคัญ*** เอา v ไปต่อท้ายแถวในคิว (รอรอบถัดไป)
        return steps, traversal_order

    def get_dijkstra_steps(self, start, end):
        # Dijkstra implementation that logs steps for visualization
        steps = []
        pq = [(0, start)]
        distances = {node: float('inf') for node in self.G.nodes()}
        distances[start] = 0
        visited = set()
        prev = {node: None for node in self.G.nodes()}
        
        steps.append(("node", start, f"Start at {start}, Dist: 0", distances.copy()))
        
        while pq:
            d, u = heapq.heappop(pq)
            
            if u in visited:
                continue
            visited.add(u)
            steps.append(("current", u, f"Processing Node {u} (Dist: {d})", distances.copy()))
            
            if u == end:
                steps.append(("finished", u, f"Reached Target {u}!", distances.copy()))
                break
            
            for v in self.G.neighbors(u):
                weight = self.G[u][v]['weight']
                steps.append(("check_edge", (u, v), f"Check neighbor {v} via {u} (Weight: {weight})", distances.copy()))
                
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    prev[v] = u
                    heapq.heappush(pq, (distances[v], v))
                    steps.append(("update", v, f"Update {v} Distance: {distances[v]}", distances.copy()))
        
        # --- Reconstruct Shortest Path ---
        path_nodes = []
        if distances[end] != float('inf'):
            cur = end
            while cur is not None:
                path_nodes.append(cur)
                if cur == start:
                    break
                cur = prev[cur]
            path_nodes.reverse()
            
            if path_nodes and path_nodes[0] == start:
                for i in range(len(path_nodes) - 1):
                    u = path_nodes[i]
                    v = path_nodes[i + 1]
                    steps.append((
                        "edge",
                        (u, v),
                        f"Shortest Path Edge: {u}-{v}",
                        distances.copy()
                    ))
                for n in path_nodes:
                    steps.append((
                        "node",
                        n,
                        f"On Shortest Path: {n}",
                        distances.copy()
                    ))
        
        return steps, distances[end], path_nodes

    def get_mst_steps(self, algo="kruskal", start_node=None):
        steps = []
        mst_edges = []
        
        if algo == "kruskal":
            edges = sorted(self.G.edges(data=True), key=lambda x: x[2]['weight']) #นำทุกเส้นมาเรียงจากน้อยไปมาก
            parent = {n: n for n in self.G.nodes()} #การกำหนดค่าเริ่มต้นให้แต่ละโหนดเป็นเซตอิสระ
            def find(n): #หาว่าอยู่กลุ่มไหน
                if parent[n] != n: #ถ้าชื่อรากไม่ใช่ชื่อตัวเองตัวแสดงว่าเคยถูกเชื่อมแล้ว
                    parent[n] = find(parent[n]) #หาตัวราก
                return parent[n] #ส่งค่ารากหรือตัวแรกกลับ
            def union(n1, n2):  
                root1, root2 = find(n1), find(n2)
                if root1 != root2: #ถ้ารากของ n1 กับ n2 ไม่เหมือนกันเชื่อมกันได้
                    parent[root1] = root2
                    return True
                return False 
            
            mst_weight = 0
            for u, v, d in edges:
                w = d['weight']
                steps.append(("check_edge", (u, v), f"Checking Edge {u}-{v} (W: {w})")) ##visual
                if union(u, v):
                    mst_weight += w #บวกน้ำหนัก
                    mst_edges.append((u, v, w)) #เส้นที่ถูกเลือกจริง
                    steps.append(("add_edge", (u, v), f"Added Edge {u}-{v} to MST")) #visual
                    steps.append(("node", u, ""))
                    steps.append(("node", v, ""))
                else:
                    steps.append(("skip", (u, v), f"Skipped {u}-{v} (Cycle detected)")) #visual
            return steps, mst_weight, mst_edges
            
        elif algo == "prim":
            # Manual Prim Implementation for Step Visualization
            if not start_node: #ถ้าไม่ได้เลือกโหนด strat ให้เลือกตัวแรก
                if self.G.number_of_nodes() > 0:
                    start_node = list(self.G.nodes())[0]
                else:
                    return [], 0, []

            visited = {start_node} #เอาstart โหนดเข้า visted 
            steps.append(("node", start_node, f"Start Prim at {start_node}")) # visual
            
            # PQ stores (weight, u, v) where u is in MST, v is candidate
            pq = [] #เก็บเส้นที่รอดำเนินการ
            for v in self.G.neighbors(start_node): #วนลูปดูโหนดที่เชื่อมกับ startโหนด
                w = self.G[start_node][v]['weight'] #ดึงค่าน้ำหนัดที่เส้นเชื่อมนั้น
                heapq.heappush(pq, (w, start_node, v))#เอาเข้า pq เรียงโดยดุจาก w ที่น้อยที่สุด
                steps.append(("check_edge", (start_node, v), f"Add potential edge {start_node}-{v} (W: {w})")) #บันทึกประวัติการเพิ่มเส้นเชื่อมทางเลือก visual
            
            mst_weight = 0
            
            while pq and len(visited) < self.G.number_of_nodes(): #pq ไม่ว่าง และ ยังไม่ visit ครบทุกโหนด
                w, u, v = heapq.heappop(pq) #ดึงเส้นเชือกที่มีน้ำหนักน้อยที่สุดออกมาจากคิว
                
                if v in visited: #ดูว่าเคยลากไปยัง
                    # Edge goes to already visited node -> Skip (Cycle)
                    continue
                
                # Add v to MST
                visited.add(v) #เพิ่ม v ไป visited
                mst_weight += w # บวกน้ำหนัก
                mst_edges.append((u, v, w)) #เก็บเส้นเชือกไว้ในคำตอบ
                
                steps.append(("add_edge", (u, v), f"Select Edge {u}-{v} (W: {w})")) #visual
                steps.append(("node", v, f"Visit Node {v}"))
                
                # Add neighbors of v to PQ
                for neighbor in self.G.neighbors(v): #วนลูปดูโหนดรอบๆโหนด v
                    if neighbor not in visited: #เอาแค่โหนดที่ไม่ได้อยู๋ใน mst
                        new_w = self.G[v][neighbor]['weight']
                        heapq.heappush(pq, (new_w, v, neighbor)) # เพิ่มเส้นใหม่ไปในคิว
                        steps.append(("check_edge", (v, neighbor), f"Add potential edge {v}-{neighbor} (W: {new_w})"))
            
            return steps, mst_weight, mst_edges

def convert_to_agraph(G, highlight_nodes=None, highlight_edges=None, current_node=None, pos_fixed=None):
    if highlight_nodes is None:
        highlight_nodes = set()
    if highlight_edges is None:
        highlight_edges = set()

    nodes = []
    edges = []

    for n in G.nodes():
        color = "#FFFFFF" 
        font_color = "black"
        
        if n == current_node:
            color = "#FFA500"  # Orange
            font_color = "white"
        elif n in highlight_nodes:
            color = "#006400"  # Dark Green
            font_color = "white"
        
        x, y = 0, 0
        if pos_fixed and n in pos_fixed:
            x, y = pos_fixed[n]
        
        nodes.append(Node(
            id=n, 
            label=str(n), 
            shape="circle",
            size=25, 
            color=color,
            font={'color': font_color},
            x=x, y=y,
            fixed=True if pos_fixed else False
        ))

    for u, v, d in G.edges(data=True):
        edge_color = "#CCCCCC"
        width = 2
        
        if (u, v) in highlight_edges or (v, u) in highlight_edges:
            edge_color = "#228B22"  # Green
            width = 4
            
        edges.append(Edge(
            source=u, 
            target=v, 
            label=str(d.get('weight', '')),
            color=edge_color,
            width=width
        ))
        
    return nodes, edges

# --------------------------
# 3. Main Streamlit App
# --------------------------

def main():
    st.set_page_config(page_title="Interactive Graph Algo", layout="wide")
    
    # Init Session State
    if "graph_data" not in st.session_state:
        st.session_state["graph_data"] = {"nodes": [], "edges": [], "pos": None}
    if "step_idx" not in st.session_state:
        st.session_state["step_idx"] = -1
    if "algo_steps" not in st.session_state:
        st.session_state["algo_steps"] = []
    if "final_result" not in st.session_state:
        st.session_state["final_result"] = ""
    
    st.title("Graph Algorithms: :orange[Step-by-Step Learning]")

    # --- Sidebar: Configuration ---
    st.sidebar.header("1. Graph Setup")
    selected_testcase = st.sidebar.selectbox("Load Testcase", ["Custom"] + list(TESTCASES.keys()))
    
    if st.sidebar.button("Reset / Load Graph"):
        st.session_state["step_idx"] = -1
        st.session_state["algo_steps"] = []
        st.session_state["final_result"] = ""
        if selected_testcase != "Custom":
            tc = TESTCASES[selected_testcase]
            st.session_state["graph_data"]["nodes"] = tc["nodes"][:]
            st.session_state["graph_data"]["edges"] = [{"u": u, "v": v, "w": w} for u, v, w in tc["edges"]]
            st.session_state["graph_data"]["pos"] = tc.get("pos")
        else:
            st.session_state["graph_data"] = {"nodes": [], "edges": [], "pos": None}
        st.rerun()

    # Manual Edit
    with st.sidebar.expander("📝 Edit Graph (Add Node/Edge)"):
        c1, c2 = st.columns(2)
        new_n = c1.text_input("New Node Name")
        if c2.button("Add Node"):
            if new_n and new_n not in st.session_state["graph_data"]["nodes"]:
                st.session_state["graph_data"]["nodes"].append(new_n)
                st.rerun()
        
        st.write("---")
        cc1, cc2, cc3 = st.columns(3)
        u = cc1.text_input("From")
        v = cc2.text_input("To")
        w = cc3.number_input("Weight", 1)
        if st.button("Add Edge"):
            if u and v:
                if u not in st.session_state["graph_data"]["nodes"]:
                    st.session_state["graph_data"]["nodes"].append(u)
                if v not in st.session_state["graph_data"]["nodes"]:
                    st.session_state["graph_data"]["nodes"].append(v)
                st.session_state["graph_data"]["edges"].append({"u": u, "v": v, "w": w})
                st.rerun()

    # --- Sidebar: Algorithm Control ---
    st.sidebar.header("2. Algorithm Control")
    
    # Construct Graph Object
    G = nx.Graph()
    for n in st.session_state["graph_data"]["nodes"]:
        G.add_node(n)
    for e in st.session_state["graph_data"]["edges"]:
        G.add_edge(e['u'], e['v'], weight=e['w'])
    
    algo_choice = st.sidebar.selectbox(
        "Algorithm",
        ["DFS", "BFS", "Dijkstra", "MST (Kruskal)", "MST (Prim)"]
    )
    
    start_node = None
    end_node = None
    if list(G.nodes()):
        # FIX: Allow start_node selection for Prim as well
        if algo_choice != "MST (Kruskal)":
            start_node = st.sidebar.selectbox("Start Node", list(G.nodes()))
        if algo_choice == "Dijkstra":
            end_node = st.sidebar.selectbox("End Node", list(G.nodes()), index=len(G.nodes())-1)
            
    if st.sidebar.button("Initialize Algorithm"):
        algo = GraphAlgorithms(G)
        steps = []
        result_text = ""
        
        if algo_choice == "DFS" and start_node:
            steps, order = algo.get_dfs_steps(start_node)
            result_text = f"**Traversal Order:**\n{' -> '.join(map(str, order))}"
            
        elif algo_choice == "BFS" and start_node:
            steps, order = algo.get_bfs_steps(start_node)
            result_text = f"**Traversal Order:**\n{' -> '.join(map(str, order))}"
            
        elif algo_choice == "Dijkstra" and start_node and end_node:
            steps, dist, path = algo.get_dijkstra_steps(start_node, end_node)
            if dist == float('inf'):
                result_text = f"**Target unreachable!** (Dist: ∞)"
            else:
                result_text = f"**Shortest Path:** {' -> '.join(map(str, path))}\n\n**Total Distance:** {dist}"
                
        elif algo_choice == "MST (Kruskal)":
            steps, weight, mst_edges = algo.get_mst_steps("kruskal")
            edge_str = ", ".join([f"({u}-{v})" for u, v, w in mst_edges])
            result_text = f"**Total MST Weight:** {weight}\n\n**Edges:** {edge_str}"
            
        elif algo_choice == "MST (Prim)":
            # FIX: Pass start_node to manual Prim
            steps, weight, mst_edges = algo.get_mst_steps("prim", start_node=start_node)
            edge_str = ", ".join([f"({u}-{v})" for u, v, w in mst_edges])
            result_text = f"**Total MST Weight:** {weight}\n\n**Edges:** {edge_str}"
        
        st.session_state["algo_steps"] = steps
        st.session_state["step_idx"] = 0
        st.session_state["final_result"] = result_text
        st.rerun()

    # --- Main Area ---
    col_vis, col_info = st.columns([3, 1])
    
    highlight_nodes = set()
    highlight_edges = set()
    current_node_vis = None
    log_msg = "Ready to start."
    distances_data = {}
    
    if st.session_state["step_idx"] >= 0 and st.session_state["algo_steps"]:
        idx = st.session_state["step_idx"]
        current_step = st.session_state["algo_steps"][idx]
        
        s_type = current_step[0]
        val = current_step[1]
        log_msg = current_step[2] if len(current_step) > 2 else ""
        
        if len(current_step) > 3:
            distances_data = current_step[3]

        for i in range(idx + 1):
            s = st.session_state["algo_steps"][i]
            if s[0] in ["node", "update", "finished"]:
                highlight_nodes.add(s[1])
            elif s[0] in ["edge", "add_edge"]:
                highlight_edges.add(s[1])
            elif s[0] == "current":
                current_node_vis = s[1]
                highlight_nodes.add(s[1])
            
            if i == idx and s[0] == "check_edge":
                highlight_edges.add(s[1])
    
    with col_vis:
        b1, b2, b3 = st.columns([1, 1, 2])
        if b1.button("◀ Prev Step"):
            if st.session_state["step_idx"] > 0:
                st.session_state["step_idx"] -= 1
                st.rerun()
        
        if b2.button("Next Step ▶"):
            if st.session_state["step_idx"] < len(st.session_state["algo_steps"]) - 1:
                st.session_state["step_idx"] += 1
                st.rerun()

        if b3.button("Instant Skip ⏩"):
            if st.session_state["algo_steps"]:
                st.session_state["step_idx"] = len(st.session_state["algo_steps"]) - 1
                st.rerun()
                
        nodes_data, edges_data = convert_to_agraph(
            G, 
            highlight_nodes=highlight_nodes,
            highlight_edges=highlight_edges,
            current_node=current_node_vis,
            pos_fixed=st.session_state["graph_data"]["pos"]
        )
        
        config = Config(
            width=700, 
            height=500, 
            directed=False, 
            physics=True if not st.session_state["graph_data"]["pos"] else False,
            hierarchical=False
        )
        
        st.caption(f"Step: {st.session_state['step_idx'] + 1} / {len(st.session_state['algo_steps'])}")
        agraph(nodes=nodes_data, edges=edges_data, config=config)

    with col_info:
        st.subheader("🔍 Status Panel")
        
        # --- Display Final Result ---
        if st.session_state["final_result"]:
            st.success(st.session_state["final_result"])
        
        st.info(f"**Action:** {log_msg}")
        
        if algo_choice == "Dijkstra" and distances_data:
            st.markdown("---")
            st.write("📊 **Distance Table**")
            df = pd.DataFrame(list(distances_data.items()), columns=["Node", "Dist"])
            
            # --- FIX: Ensure consistent type (string) for the column to avoid PyArrow errors ---
            df['Dist'] = df['Dist'].apply(lambda x: "∞" if x == float('inf') else str(x))
            
            df = df.sort_values(by="Node")
            st.dataframe(df, hide_index=True)
            
        st.markdown("---")
        st.caption("**Legend:**")
        st.markdown("⚪ White: Unvisited")
        st.markdown("🟠 Orange: Processing")
        st.markdown("🟢 Green: Visited / Path")

if __name__ == "__main__":
    main()