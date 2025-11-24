import streamlit as st
import networkx as nx
from streamlit_agraph import agraph, Node, Edge, Config

# --------------------------
# 1. Testcase Definitions
# --------------------------
SCALE = 200 

TESTCASES = {
    # ----------------------------------------------------
    # (Dijkstra's Shortest Path)
    # ----------------------------------------------------
    "Image Case 1: Start a to e": {
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
    "Image Case 2: Start a to d": {
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
    "Image Case 3: Start a to f": {
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
    "Testcase 4: Weighted Shortest Path": {
        "nodes": ["S", "A", "B", "C", "D", "E", "F", "T"],
        "edges": [
            ("S", "A", 2), ("S", "B", 5), ("S", "C", 3),
            ("A", "B", 2), ("A", "D", 6),
            ("B", "D", 3), ("B", "C", 2), ("B", "F", 6),
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

    # เหลือแค่ Dijkstra ตามที่ต้องการครับ
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
            color = "#006400" # Dark Green (Visited/Path)
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
    st.set_page_config(page_title="Dijkstra Visualizer", layout="wide")
    
    if "graph_data" not in st.session_state:
        st.session_state["graph_data"] = {"nodes": [], "edges": [], "pos": None}
    
    st.title("Dijkstra's Shortest Path Visualizer")
    st.markdown("""
    **Instructions:**
    1. Load a Testcase.
    2. Select Start/End Nodes.
    3. Click 'Calculate Path' to see the shortest route 

[Image of Breadth First Search diagram]
.
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
        st.subheader("Controls")
        # ลบตัวเลือกอื่นออก เหลือแค่ Dijkstra
        algo_choice = st.selectbox("Algorithm", ["Dijkstra"])
        
        start_node = None
        end_node = None
        
        nodes = list(G.nodes())
        if nodes:
            start_node = st.selectbox("Start Node", nodes)
            end_node = st.selectbox("Target Node", nodes, index=len(nodes)-1)
        
        run_btn = st.button("Calculate Path", type="primary")

    with col_graph:
        graph_placeholder = st.empty()
        
        visited_nodes = set()
        visited_edges = set()
        
        if run_btn and nodes:
            algo = GraphAlgorithms(G)
            steps = []
            
            # --- Dijkstra Only ---
            steps, dist = algo.get_dijkstra_steps(start_node, end_node)
            if dist != -1: 
                path_sequence = [val for s_type, val in steps if s_type == 'node']
                path_text = " -> ".join(path_sequence)
                st.success(f"**Shortest Path:** {path_text}")
                st.success(f"**Total Distance:** {dist}")
            else:
                st.error("No path found.")

            # --- Gather Visualization Data ---
            for s_type, val in steps:
                if s_type == "node":
                    visited_nodes.add(val)
                elif s_type == "edge":
                    visited_edges.add(val)

            nodes_data, edges_data = convert_to_agraph(
                G, 
                highlight_nodes=visited_nodes, 
                path_edges=visited_edges, 
                pos_fixed=st.session_state["graph_data"]["pos"]
            )

        else:
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