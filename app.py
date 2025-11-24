import streamlit as st
import networkx as nx
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
        "nodes": ["a", "b", "c", "d", "e"],
        "edges": [
            ("a", "b", 1), ("a", "c", 1), ("a", "d", 1), ("a", "e", 1),
            ("b", "c", 1), ("b", "d", 1), ("b", "e", 1),
            ("c", "d", 1), ("c", "e", 1),
            ("d", "e", 1)
        ],
        "pos": {
            "a": (0, -2*SCALE), "b": (1.9*SCALE, -0.6*SCALE), "c": (1.2*SCALE, 1.5*SCALE),
            "d": (-1.2*SCALE, 1.5*SCALE), "e": (-1.9*SCALE, -0.6*SCALE)
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
            steps.append(("node", u))
            for v in self.G.neighbors(u):
                if v not in visited:
                    steps.append(("edge", (u, v)))
                    dfs(v)
        dfs(start_node)
        return steps

    def get_bfs_steps(self, start_node):
        steps = []
        visited = set()
        queue = [start_node]
        visited.add(start_node)
        steps.append(("node", start_node))
        
        while queue:
            u = queue.pop(0)
            for v in self.G.neighbors(u):
                if v not in visited:
                    visited.add(v)
                    steps.append(("edge", (u, v)))
                    steps.append(("node", v))
                    queue.append(v)
        return steps

    def get_dijkstra_steps(self, start, end):
        try:
            path = nx.dijkstra_path(self.G, start, end, weight='weight')
            steps = []
            for i in range(len(path)):
                steps.append(("node", path[i]))
                if i < len(path) - 1:
                    steps.append(("edge", (path[i], path[i+1])))
            return steps, nx.dijkstra_path_length(self.G, start, end, weight='weight')
        except nx.NetworkXNoPath:
            return [], -1
        except Exception:
            return [], -1

    def get_mst_steps(self, algo="kruskal"):
        steps = []
        # Create MST using NetworkX built-in functions
        if algo == "kruskal":
            mst = nx.minimum_spanning_tree(self.G, algorithm="kruskal")
        else: # Prim
            mst = nx.minimum_spanning_tree(self.G, algorithm="prim")
            
        weight = mst.size(weight="weight")
        
        # Extract edges and nodes to visualize
        # Note: mst.edges(data=True) returns (u, v, data_dict)
        for u, v, d in mst.edges(data=True):
            steps.append(("edge", (u, v)))
            steps.append(("node", u))
            steps.append(("node", v))

        return steps, weight

def convert_to_agraph(G, highlight_nodes=None, path_edges=None, pos_fixed=None):
    if highlight_nodes is None: highlight_nodes = set()
    if path_edges is None: path_edges = set()

    nodes = []
    edges = []

    for n in G.nodes():
        color = "#FFFFFF" # White default
        label_color = "black"
        size = 25
        
        if n in highlight_nodes:
            color = "#006400" # Dark Green (Visited)
            label_color = "white"
        
        x, y = 0, 0
        if pos_fixed and n in pos_fixed:
            x, y = pos_fixed[n]
        
        nodes.append(Node(
            id=n, 
            label=str(n), 
            size=size, 
            color=color,
            font={'color': label_color},
            x=x, y=y,
            fixed=True if pos_fixed else False
        ))

    for u, v, d in G.edges(data=True):
        edge_color = "#CCCCCC" # Gray default
        width = 2
        
        # Check if edge is in path (undirected check)
        is_path = (u, v) in path_edges or (v, u) in path_edges
        
        if is_path:
            edge_color = "#228B22" # Forest Green (Visited path)
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
    st.set_page_config(page_title="Graph Algo Visualizer", layout="wide")
    
    if "graph_data" not in st.session_state:
        st.session_state["graph_data"] = {"nodes": [], "edges": [], "pos": None}
    
    st.title("Graph Algorithms Visualizer :blue[Instant Result]")
    st.markdown("""
    **Instructions:**
    1. Load a Testcase.
    2. Select an algorithm and click 'Calculate Path'.
    3. See the path text and the highlighted graph immediately.
    """)

    # --- Sidebar ---
    st.sidebar.header("Configuration")
    selected_testcase = st.sidebar.selectbox("Load Testcase", ["Custom"] + list(TESTCASES.keys()))
    
    if st.sidebar.button("Load Graph"):
        if selected_testcase != "Custom":
            tc = TESTCASES[selected_testcase]
            st.session_state["graph_data"]["nodes"] = tc["nodes"][:]
            st.session_state["graph_data"]["edges"] = [{"u": u, "v": v, "w": w} for u, v, w in tc["edges"]]
            st.session_state["graph_data"]["pos"] = tc.get("pos")
            st.rerun()
        else:
            st.session_state["graph_data"] = {"nodes": [], "edges": [], "pos": None}
            st.rerun()

    with st.sidebar.expander("Edit Graph Manually"):
        new_node = st.text_input("Add Node")
        if st.button("Add"):
            if new_node and new_node not in st.session_state["graph_data"]["nodes"]:
                st.session_state["graph_data"]["nodes"].append(new_node)
        
        c1, c2, c3 = st.columns(3)
        u_in = c1.text_input("Source")
        v_in = c2.text_input("Target")
        w_in = c3.number_input("Weight", value=1)
        if st.button("Add Edge"):
            if u_in and v_in:
                if u_in not in st.session_state["graph_data"]["nodes"]: st.session_state["graph_data"]["nodes"].append(u_in)
                if v_in not in st.session_state["graph_data"]["nodes"]: st.session_state["graph_data"]["nodes"].append(v_in)
                st.session_state["graph_data"]["edges"].append({"u": u_in, "v": v_in, "w": w_in})

    # --- Main Area ---
    G = nx.Graph()
    for n in st.session_state["graph_data"]["nodes"]: G.add_node(n)
    for e in st.session_state["graph_data"]["edges"]: G.add_edge(e['u'], e['v'], weight=e['w'])

    col_algo, col_graph = st.columns([1, 3])

    with col_algo:
        st.subheader("Algorithms")
        algo_choice = st.selectbox("Choose Algorithm", ["DFS", "BFS", "Dijkstra", "MST (Kruskal)", "MST (Prim)"])
        
        start_node = None
        end_node = None
        
        nodes = list(G.nodes())
        if nodes:
            if algo_choice in ["DFS", "BFS", "Dijkstra"]:
                start_node = st.selectbox("Start Node", nodes)
            if algo_choice == "Dijkstra":
                end_node = st.selectbox("Target Node", nodes, index=len(nodes)-1)
        
        run_btn = st.button("Calculate Path", type="primary")

    with col_graph:
        graph_placeholder = st.empty()
        
        # Default State variables
        visited_nodes = set()
        visited_edges = set()
        path_text = ""
        
        if run_btn and nodes:
            algo = GraphAlgorithms(G)
            steps = []
            
            # --- Algorithm Logic ---
            if algo_choice == "DFS":
                steps = algo.get_dfs_steps(start_node)
                # Filter just nodes for text display
                path_sequence = [val for s_type, val in steps if s_type == 'node']
                # Remove duplicates while preserving order
                seen = set()
                path_sequence = [x for x in path_sequence if not (x in seen or seen.add(x))]
                path_text = " -> ".join(path_sequence)
                st.info(f"**DFS Traversal Order:** {path_text}")

            elif algo_choice == "BFS":
                steps = algo.get_bfs_steps(start_node)
                path_sequence = [val for s_type, val in steps if s_type == 'node']
                path_text = " -> ".join(path_sequence)
                st.info(f"**BFS Traversal Order:** {path_text}")

            elif algo_choice == "Dijkstra":
                steps, dist = algo.get_dijkstra_steps(start_node, end_node)
                if dist != -1: 
                    path_sequence = [val for s_type, val in steps if s_type == 'node']
                    path_text = " -> ".join(path_sequence)
                    st.success(f"**Shortest Path:** {path_text}")
                    st.success(f"**Total Distance:** {dist}")
                else:
                    st.error("No path found.")

            elif "MST" in algo_choice:
                algo_type = "kruskal" if "Kruskal" in algo_choice else "prim"
                steps, w = algo.get_mst_steps(algo_type)
                st.success(f"**MST Total Weight:** {w}")
                
                # FIX: Unpack carefully using 'val' which can be either Node(string) or Edge(tuple)
                # Only when s_type is 'edge', we assume val is (u, v) and format it.
                edges_list = [f"({val[0]},{val[1]})" for s_type, val in steps if s_type == 'edge']
                
                st.info(f"**Edges in MST:** {', '.join(edges_list)}")

            # --- Gather Visualization Data ---
            for s_type, val in steps:
                if s_type == "node":
                    visited_nodes.add(val)
                elif s_type == "edge":
                    visited_edges.add(val)

            # Generate Graph Data
            nodes_data, edges_data = convert_to_agraph(
                G, 
                highlight_nodes=visited_nodes, 
                path_edges=visited_edges, 
                pos_fixed=st.session_state["graph_data"]["pos"]
            )

        else:
            # Idle State (No calculation yet)
            nodes_data, edges_data = convert_to_agraph(
                G, 
                pos_fixed=st.session_state["graph_data"]["pos"]
            )

        # Render
        config = Config(
            width=800, 
            height=600, 
            directed=False, 
            physics=True if not st.session_state["graph_data"]["pos"] else False, 
            hierarchical=False
        )
        
        with graph_placeholder.container():
            agraph(nodes=nodes_data, edges=edges_data, config=config)

if __name__ == "__main__":
    main()