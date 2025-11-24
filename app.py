import streamlit as st
import networkx as nx
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config

# --------------------------
# 1. Testcase Definitions
# --------------------------
SCALE = 200 

TESTCASES = {
    "Testcase 1: Hexagon/Grid (DFS/BFS)": {
        "nodes": ["a", "b", "c", "d", "e", "f", "g"],
        "edges": [
            ("a", "b", 1), ("a", "f", 1),
            ("b", "c", 1), ("b", "g", 1),
            ("c", "d", 1), ("c", "g", 1),
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
    "Testcase 2: Pentagon (Complete Graph)": {
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
    "Testcase 3: Composite (Square + Rect)": {
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
    "Testcase 4: Weighted Shortest Path": {
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
    }
}

# --------------------------
# 2. Helper Classes & Functions
# --------------------------

class GraphAlgorithms:
    def __init__(self, G):
        self.G = G

    def get_dfs_steps(self, start_node):
        steps = []
        visited = set()
        def dfs(u):
            visited.add(u)
            steps.append(("node", u, f"Visit Node {u}"))
            for v in self.G.neighbors(u):
                if v not in visited:
                    steps.append(("edge", (u, v), f"Explore Edge {u}-{v}"))
                    dfs(v)
        dfs(start_node)
        return steps

    def get_bfs_steps(self, start_node):
        steps = []
        visited = set()
        queue = [start_node]
        visited.add(start_node)
        steps.append(("node", start_node, f"Start at {start_node}"))
        
        while queue:
            u = queue.pop(0)
            for v in self.G.neighbors(u):
                if v not in visited:
                    visited.add(v)
                    steps.append(("edge", (u, v), f"Discover Edge {u}-{v}"))
                    steps.append(("node", v, f"Visit Node {v}"))
                    queue.append(v)
        return steps

    def get_dijkstra_steps(self, start, end):
        # Dijkstra implementation that logs steps for visualization
        # Returns list of steps: (type, value, description, current_distances_dict)
        import heapq
        
        steps = []
        pq = [(0, start)]
        distances = {node: float('inf') for node in self.G.nodes()}
        distances[start] = 0
        visited = set()
        
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
                    heapq.heappush(pq, (distances[v], v))
                    steps.append(("update", v, f"Update {v} Distance: {distances[v]}", distances.copy()))
                    
        return steps, distances[end]

    def get_mst_steps(self, algo="kruskal"):
        steps = []
        if algo == "kruskal":
            # Manual Kruskal for step visualization
            edges = sorted(self.G.edges(data=True), key=lambda x: x[2]['weight'])
            parent = {n: n for n in self.G.nodes()}
            def find(n):
                if parent[n] != n: parent[n] = find(parent[n])
                return parent[n]
            def union(n1, n2):
                root1, root2 = find(n1), find(n2)
                if root1 != root2: parent[root1] = root2; return True
                return False
            
            mst_weight = 0
            for u, v, d in edges:
                w = d['weight']
                steps.append(("check_edge", (u, v), f"Checking Edge {u}-{v} (W: {w})"))
                if union(u, v):
                    mst_weight += w
                    steps.append(("add_edge", (u, v), f"Added Edge {u}-{v} to MST"))
                    steps.append(("node", u, ""))
                    steps.append(("node", v, ""))
                else:
                    steps.append(("skip", (u, v), f"Skipped {u}-{v} (Cycle detected)"))
            return steps, mst_weight
        else: 
            # Simplified Prim
            mst = nx.minimum_spanning_tree(self.G, algorithm="prim")
            weight = mst.size(weight="weight")
            for u, v, d in mst.edges(data=True):
                steps.append(("add_edge", (u, v), f"MST Edge: {u}-{v}"))
            return steps, weight

def convert_to_agraph(G, highlight_nodes=None, highlight_edges=None, current_node=None, pos_fixed=None):
    if highlight_nodes is None: highlight_nodes = set()
    if highlight_edges is None: highlight_edges = set()

    nodes = []
    edges = []

    for n in G.nodes():
        # --- FEATURE: Label Inside Node ---
        # shape='circle' ทำให้ตัวหนังสืออยู่ข้างใน
        # ปรับสี: ถ้าเป็น Current Node (กำลังพิจารณา) -> สีส้ม, Visited -> เขียว
        color = "#FFFFFF" 
        font_color = "black"
        
        if n == current_node:
            color = "#FFA500" # Orange
            font_color = "white"
        elif n in highlight_nodes:
            color = "#006400" # Dark Green
            font_color = "white"
        
        x, y = 0, 0
        if pos_fixed and n in pos_fixed:
            x, y = pos_fixed[n]
        
        nodes.append(Node(
            id=n, 
            label=str(n), 
            shape="circle", # <--- สำคัญ: ทำให้เป็นวงกลมและตัวหนังสืออยู่ข้างใน
            size=25, 
            color=color,
            font={'color': font_color},
            x=x, y=y,
            fixed=True if pos_fixed else False
        ))

    for u, v, d in G.edges(data=True):
        edge_color = "#CCCCCC"
        width = 2
        
        # Check undirected
        if (u, v) in highlight_edges or (v, u) in highlight_edges:
            edge_color = "#228B22" # Green
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
        st.session_state["step_idx"] = -1 # -1 means not started or finished
    if "algo_steps" not in st.session_state:
        st.session_state["algo_steps"] = []
    
    st.title("Graph Algorithms: :orange[Step-by-Step Learning]")

    # --- Sidebar: Configuration ---
    st.sidebar.header("1. Graph Setup")
    selected_testcase = st.sidebar.selectbox("Load Testcase", ["Custom"] + list(TESTCASES.keys()))
    
    if st.sidebar.button("Reset / Load Graph"):
        st.session_state["step_idx"] = -1
        st.session_state["algo_steps"] = []
        if selected_testcase != "Custom":
            tc = TESTCASES[selected_testcase]
            st.session_state["graph_data"]["nodes"] = tc["nodes"][:]
            st.session_state["graph_data"]["edges"] = [{"u": u, "v": v, "w": w} for u, v, w in tc["edges"]]
            st.session_state["graph_data"]["pos"] = tc.get("pos")
        else:
            st.session_state["graph_data"] = {"nodes": [], "edges": [], "pos": None}
        st.rerun()

    # Manual Edit (Sidebar is more reliable than Canvas click)
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
                # Add nodes if not exist
                if u not in st.session_state["graph_data"]["nodes"]: st.session_state["graph_data"]["nodes"].append(u)
                if v not in st.session_state["graph_data"]["nodes"]: st.session_state["graph_data"]["nodes"].append(v)
                st.session_state["graph_data"]["edges"].append({"u": u, "v": v, "w": w})
                st.rerun()

    # --- Sidebar: Algorithm Control ---
    st.sidebar.header("2. Algorithm Control")
    
    # Construct Graph Object
    G = nx.Graph()
    for n in st.session_state["graph_data"]["nodes"]: G.add_node(n)
    for e in st.session_state["graph_data"]["edges"]: G.add_edge(e['u'], e['v'], weight=e['w'])
    
    algo_choice = st.sidebar.selectbox("Algorithm", ["DFS", "BFS", "Dijkstra", "MST (Kruskal)"])
    
    start_node = None
    end_node = None
    if list(G.nodes()):
        if algo_choice != "MST (Kruskal)":
            start_node = st.sidebar.selectbox("Start Node", list(G.nodes()))
        if algo_choice == "Dijkstra":
            end_node = st.sidebar.selectbox("End Node", list(G.nodes()), index=len(G.nodes())-1)
            
    if st.sidebar.button("Initialize Algorithm"):
        algo = GraphAlgorithms(G)
        steps = []
        if algo_choice == "DFS": steps = algo.get_dfs_steps(start_node)
        elif algo_choice == "BFS": steps = algo.get_bfs_steps(start_node)
        elif algo_choice == "Dijkstra": steps, _ = algo.get_dijkstra_steps(start_node, end_node)
        elif algo_choice == "MST (Kruskal)": steps, _ = algo.get_mst_steps("kruskal")
        
        st.session_state["algo_steps"] = steps
        st.session_state["step_idx"] = 0 # Start at first step
        st.rerun()

    # --- Main Area ---
    col_vis, col_info = st.columns([3, 1])
    
    # Logic to Determine Current Visualization State based on step_idx
    highlight_nodes = set()
    highlight_edges = set()
    current_node_vis = None
    log_msg = "Ready to start."
    distances_data = {}
    
    if st.session_state["step_idx"] >= 0 and st.session_state["algo_steps"]:
        # Replay steps up to current index
        idx = st.session_state["step_idx"]
        current_step = st.session_state["algo_steps"][idx]
        
        # Unpack step data
        # Common formats: (type, val, msg) or (type, val, msg, dist_dict)
        s_type = current_step[0]
        val = current_step[1]
        log_msg = current_step[2] if len(current_step) > 2 else ""
        
        # Dijkstra has distance dict at index 3
        if len(current_step) > 3:
            distances_data = current_step[3]

        # Process History for Colors
        for i in range(idx + 1):
            s = st.session_state["algo_steps"][i]
            if s[0] == "node" or s[0] == "update" or s[0] == "finished":
                highlight_nodes.add(s[1])
            elif s[0] == "edge" or s[0] == "add_edge":
                highlight_edges.add(s[1])
            elif s[0] == "current":
                current_node_vis = s[1]
                highlight_nodes.add(s[1])
            
            # Special highlighting for current step action
            if i == idx:
                if s[0] == "check_edge":
                    highlight_edges.add(s[1]) # Temporarily highlight edge being checked
    
    with col_vis:
        # --- Controller Buttons ---
        b1, b2, b3 = st.columns([1, 1, 2])
        if b1.button("◀ Prev Step"):
            if st.session_state["step_idx"] > 0:
                st.session_state["step_idx"] -= 1
                st.rerun()
        
        if b2.button("Next Step ▶"):
            if st.session_state["step_idx"] < len(st.session_state["algo_steps"]) - 1:
                st.session_state["step_idx"] += 1
                st.rerun()
                
        # --- Graph Visualization ---
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
        
        # 1. Log Box
        st.info(f"**Action:** {log_msg}")
        
        # 2. Dijkstra Table
        if algo_choice == "Dijkstra" and distances_data:
            st.markdown("---")
            st.write("📊 **Distance Table**")
            # Convert dict to clean dataframe
            df = pd.DataFrame(list(distances_data.items()), columns=["Node", "Dist"])
            # Format infinity
            df['Dist'] = df['Dist'].apply(lambda x: "∞" if x == float('inf') else x)
            df = df.sort_values(by="Node")
            st.dataframe(df, hide_index=True)
            
        # 3. Legend
        st.markdown("---")
        st.caption("**Legend:**")
        st.markdown("⚪ White: Unvisited")
        st.markdown("🟠 Orange: Processing")
        st.markdown("🟢 Green: Visited / Path")

if __name__ == "__main__":
    main()