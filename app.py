import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd


# --------------------------
# Testcase Definitions (with fixed positions)
# --------------------------

TESTCASES = {
    # ---------- DFS / BFS ----------
    "DFS/BFS #1 - Grid 3x3 (start a)": {
        "category": "dfs_bfs",
        "start": "a",
        "nodes": ["a", "b", "c", "d", "e", "f", "g", "h", "i"],
        "edges": [
            ("a", "b", 1),
            ("b", "c", 1),
            ("h", "i", 1),
            ("i", "d", 1),
            ("g", "f", 1),
            ("f", "e", 1),
            ("a", "h", 1),
            ("b", "i", 1),
            ("c", "d", 1),
            ("h", "g", 1),
            ("i", "f", 1),
            ("d", "e", 1),
        ],
        "pos": {
            "a": (-1, 1),
            "b": (0, 1),
            "c": (1, 1),
            "h": (-1, 0),
            "i": (0, 0),
            "d": (1, 0),
            "g": (-1, -1),
            "f": (0, -1),
            "e": (1, -1),
        },
    },

    "DFS/BFS #2 - Double chain (start a)": {
        "category": "dfs_bfs",
        "start": "a",
        "nodes": ["a", "b", "c", "d", "e", "f", "g"],
        "edges": [
            ("a", "b", 1),
            ("b", "g", 1),
            ("g", "f", 1),
            ("f", "a", 1),
            ("b", "c", 1),
            ("c", "e", 1),
            ("b", "f", 1),
            ("g", "c", 1),
            ("c", "d", 1),
            ("d", "e", 1),
            ("e", "g", 1),
            ("f", "e", 1),
        ],
        "pos": {
            "a": (-2, 0),
            "b": (-1, 1),
            "f": (-1, -1),
            "g": (0, 0),
            "c": (1, 1),
            "e": (1, -1),
            "d": (2, 0),
        },
    },

    "DFS/BFS #3 - Complete pentagon (start a)": {
        "category": "dfs_bfs",
        "start": "a",
        "nodes": ["a", "b", "c", "d", "e"],
        "edges": [
            ("a", "b", 1),
            ("a", "c", 1),
            ("a", "d", 1),
            ("a", "e", 1),
            ("b", "c", 1),
            ("b", "d", 1),
            ("b", "e", 1),
            ("c", "d", 1),
            ("c", "e", 1),
            ("d", "e", 1),
        ],
        "pos": {
            "a": (0, 1.3),
            "b": (1, 0.4),
            "c": (0.6, -1),
            "d": (-0.6, -1),
            "e": (-1, 0.4),
        },
    },

    # ปรับใหม่ให้อ่านง่ายและใกล้ของจริงมากขึ้น
    "DFS/BFS #4 - Composite (start a)": {
        "category": "dfs_bfs",
        "start": "a",
        "nodes": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"],
        "edges": [
            ("a", "b", 1),
            ("b", "c", 1),
            ("c", "d", 1),
            ("d", "a", 1),
            ("d", "e", 1),
            ("e", "f", 1),
            ("f", "c", 1),
            ("g", "h", 1),
            ("h", "i", 1),
            ("i", "j", 1),
            ("j", "g", 1),
            ("g", "k", 1),
            ("h", "k", 1),
            ("i", "k", 1),
            ("j", "k", 1),
            ("c", "g", 1),
        ],
        "pos": {
            # ก้อนซ้าย: สองสี่เหลี่ยมซ้อนกัน
            "a": (0, 2),
            "b": (2, 2),
            "c": (2, 0),
            "d": (0, 0),
            "e": (0, -2),
            "f": (2, -2),
            # ก้อนขวา: สี่เหลี่ยม + จุดกลาง
            "g": (6, 2),
            "h": (8, 2),
            "i": (8, -2),
            "j": (6, -2),
            "k": (7, 0),
        },
    },

    # ---------- Dijkstra ----------
    "Dijkstra #1 - a to e": {
        "category": "dijkstra",
        "start": "a",
        "target": "e",
        "nodes": ["a", "b", "c", "d", "e"],
        "edges": [
            ("a", "b", 4),
            ("a", "c", 2),
            ("b", "c", 1),
            ("b", "d", 5),
            ("c", "d", 8),
            ("c", "e", 10),
            ("d", "e", 2),
        ],
        "pos": {
            "a": (0, 0),
            "b": (2, 1),
            "c": (2, -1),
            "d": (4, 1),
            "e": (4, -1),
        },
    },

    # ปรับ layout ให้เป็นรูปเพนทากอน a ซ้าย, b บน, c ล่าง, e กลาง, d ขวา
    "Dijkstra #2 - a to d": {
        "category": "dijkstra",
        "start": "a",
        "target": "d",
        "nodes": ["a", "b", "c", "d", "e"],
        "edges": [
            ("a", "b", 6),
            ("a", "c", 2),
            ("b", "c", 7),
            ("b", "e", 5),
            ("c", "d", 3),
            ("c", "e", 1),
            ("e", "d", 2),
        ],
        "pos": {
            "a": (0, 0),
            "b": (2, 2),
            "c": (2, -2),
            "e": (4, 0),
            "d": (6, 0),
        },
    },

    # ปรับ layout ให้เป็นสองสามเหลี่ยมชนกัน (ทางบน/ทางล่าง) a→f
    "Dijkstra #3 - a to f": {
        "category": "dijkstra",
        "start": "a",
        "target": "f",
        "nodes": ["a", "b", "c", "d", "e", "f"],
        "edges": [
            ("a", "b", 10),
            ("a", "c", 5),
            ("b", "c", 3),
            ("b", "d", 2),
            ("c", "e", 9),
            ("d", "e", 4),
            ("d", "f", 6),
            ("e", "f", 7),
        ],
        "pos": {
            "a": (0, 0),
            "b": (2, 2),
            "c": (2, -2),
            "d": (4, 2),
            "e": (4, -2),
            "f": (6, 0),
        },
    },

    # รูป S-A-B-D-T ด้านบน, S-C-F-E-T ด้านล่าง
    "Dijkstra #4 - S to T": {
        "category": "dijkstra",
        "start": "S",
        "target": "T",
        "nodes": ["S", "A", "C", "B", "D", "F", "E", "T"],
        "edges": [
            ("S", "A", 3),
            ("S", "C", 2),
            ("A", "B", 3),
            ("C", "B", 6),
            ("B", "D", 4),
            ("C", "F", 7),
            ("D", "E", 2),
            ("F", "E", 5),
            ("D", "T", 3),
            ("E", "T", 6),
        ],
        "pos": {
            "S": (0, 0),
            "A": (2, 2),
            "C": (2, -2),
            "B": (4, 0),
            "D": (6, 2),
            "F": (6, -2),
            "E": (8, 0),
            "T": (10, 0),
        },
    },

    # ---------- MST ----------
    "MST #1 - double diamond": {
        "category": "mst",
        "nodes": ["a", "b", "c", "d", "e", "f", "g"],
        "edges": [
            ("a", "b", 2),
            ("a", "f", 3),
            ("f", "b", 3),
            ("f", "e", 2),
            ("e", "d", 4),
            ("c", "d", 5),
            ("b", "c", 3),
            ("b", "g", 3),
            ("c", "g", 4),
            ("f", "g", 5),
            ("e", "g", 3),
            ("c", "e", 5),
        ],
        "pos": {
            "a": (-2, 0),
            "b": (-1, 1),
            "f": (-1, -1),
            "g": (0, 0),
            "c": (1, 1),
            "e": (1, -1),
            "d": (2, 0),
        },
    },

    "MST #2 - K5 with weights": {
        "category": "mst",
        "nodes": ["a", "b", "c", "d", "e"],
        "edges": [
            ("a", "b", 3),
            ("a", "c", 9),
            ("a", "d", 8),
            ("a", "e", 4),
            ("b", "c", 5),
            ("b", "d", 5),
            ("b", "e", 3),
            ("c", "d", 6),
            ("c", "e", 8),
            ("d", "e", 1),
        ],
        "pos": {
            "a": (0, 1.3),
            "b": (1, 0.4),
            "c": (0.6, -1),
            "d": (-0.6, -1),
            "e": (-1, 0.4),
        },
    },

    "MST #3 - rectangle + center": {
        "category": "mst",
        "nodes": ["a", "b", "c", "d", "e"],
        "edges": [
            ("a", "b", 1),
            ("b", "c", 2),
            ("c", "d", 3),
            ("d", "a", 2),
            ("a", "e", 3),
            ("b", "e", 2),
            ("c", "e", 4),
            ("d", "e", 1),
        ],
        "pos": {
            "a": (0, 1),
            "b": (2, 1),
            "c": (2, -1),
            "d": (0, -1),
            "e": (1, 0),
        },
    },

    "MST #4 - house": {
        "category": "mst",
        "nodes": ["a", "b", "c", "d", "e"],
        "edges": [
            ("b", "c", 3),
            ("c", "d", 3),
            ("d", "e", 1),
            ("e", "b", 3),
            ("b", "a", 1),
            ("e", "a", 2),
            ("b", "d", 4),
            ("c", "e", 2),
        ],
        "pos": {
            "b": (0, 0),
            "c": (0, -1.5),
            "d": (2, -1.5),
            "e": (2, 0),
            "a": (1, 1.5),
        },
    },
}


# --------------------------
# Graph Algorithm Class
# --------------------------

class GraphAlgorithms:
    def __init__(self, graph: nx.Graph):
        self.G = graph

    def dfs_spanning_tree(self, start_node):
        tree = nx.dfs_tree(self.G, source=start_node)
        order = list(tree.nodes())
        tree_edges = list(tree.edges())
        return order, tree_edges

    def bfs_spanning_tree(self, start_node):
        tree = nx.bfs_tree(self.G, source=start_node)
        order = list(tree.nodes())
        tree_edges = list(tree.edges())
        return order, tree_edges

    def dijkstra_shortest_path(self, source, target):
        path_nodes = nx.dijkstra_path(self.G, source, target, weight="weight")
        total_weight = nx.dijkstra_path_length(self.G, source, target, weight="weight")
        path_edges = list(zip(path_nodes[:-1], path_nodes[1:]))
        return path_nodes, total_weight, path_edges

    def prim_mst(self):
        mst = nx.minimum_spanning_tree(self.G, algorithm="prim", weight="weight")
        edges = list(mst.edges(data=True))
        edge_pairs = [(u, v) for (u, v, _) in edges]
        total_weight = sum(d.get("weight", 1.0) for (_, _, d) in edges)
        return edge_pairs, total_weight

    def kruskal_mst(self):
        mst = nx.minimum_spanning_tree(self.G, algorithm="kruskal", weight="weight")
        edges = list(mst.edges(data=True))
        edge_pairs = [(u, v) for (u, v, _) in edges]
        total_weight = sum(d.get("weight", 1.0) for (_, _, d) in edges)
        return edge_pairs, total_weight


# --------------------------
# Helper Functions
# --------------------------

def init_session_state():
    if "nodes" not in st.session_state:
        st.session_state["nodes"] = []
    if "edges" not in st.session_state:
        st.session_state["edges"] = []
    if "testcase_meta" not in st.session_state:
        st.session_state["testcase_meta"] = {}


def build_graph():
    G = nx.Graph()
    for n in st.session_state["nodes"]:
        G.add_node(n)
    for e in st.session_state["edges"]:
        u = e["u"]
        v = e["v"]
        w = e["weight"]
        G.add_edge(u, v, weight=w)
    return G


def load_testcase_graph(test_name: str):
    case = TESTCASES.get(test_name)
    if not case:
        st.warning(f"Testcase '{test_name}' not found.")
        return

    st.session_state["nodes"] = [str(n) for n in case["nodes"]]
    st.session_state["edges"] = [
        {"u": str(u), "v": str(v), "weight": float(w)}
        for (u, v, w) in case["edges"]
    ]
    st.session_state["testcase_meta"] = {
        "name": test_name,
        "category": case.get("category"),
        "start": case.get("start"),
        "target": case.get("target"),
        "pos": case.get("pos"),
    }


def draw_graph(G, highlight_edges=None, highlight_nodes=None, title=None, pos=None):
    if highlight_edges is None:
        highlight_edges = []
    if highlight_nodes is None:
        highlight_nodes = []

    if pos is not None and set(pos.keys()) == set(G.nodes()):
        pos_used = pos
    else:
        pos_used = nx.spring_layout(G, seed=42)

    highlight_edge_set = {frozenset((u, v)) for (u, v) in highlight_edges}
    highlight_node_set = set(highlight_nodes)

    fig, ax = plt.subplots(figsize=(7, 5))
    if title:
        ax.set_title(title, color="white")
    ax.set_axis_off()

    fig.patch.set_facecolor("#0e1117")
    ax.set_facecolor("#0e1117")

    all_nodes = list(G.nodes())
    base_nodes = [n for n in all_nodes if n not in highlight_node_set]

    if base_nodes:
        nx.draw_networkx_nodes(
            G,
            pos_used,
            nodelist=base_nodes,
            node_color="#1f78b4",
            node_size=700,
            ax=ax,
        )

    if highlight_node_set:
        nx.draw_networkx_nodes(
            G,
            pos_used,
            nodelist=list(highlight_node_set),
            node_color="#e31a1c",
            node_size=800,
            ax=ax,
        )

    all_edges = list(G.edges())
    base_edges = [e for e in all_edges if frozenset(e) not in highlight_edge_set]

    if base_edges:
        nx.draw_networkx_edges(
            G,
            pos_used,
            edgelist=base_edges,
            width=1.5,
            edge_color="#aaaaaa",
            ax=ax,
        )

    if highlight_edge_set:
        nx.draw_networkx_edges(
            G,
            pos_used,
            edgelist=[tuple(e) for e in highlight_edge_set],
            width=3,
            edge_color="#ff7f00",
            ax=ax,
        )

    nx.draw_networkx_labels(G, pos_used, font_color="white", font_size=10, ax=ax)

    edge_labels = {(u, v): f"{d.get('weight', 1)}" for (u, v, d) in G.edges(data=True)}
    nx.draw_networkx_edge_labels(
        G,
        pos_used,
        edge_labels=edge_labels,
        font_color="white",
        ax=ax,
    )

    return fig


def add_node_ui():
    st.subheader("Add Node")
    with st.form("add_node_form", clear_on_submit=True):
        node_label = st.text_input("Node label (e.g., A, 1, X)", key="node_label")
        submitted = st.form_submit_button("Add Node")
        if submitted:
            label = node_label.strip()
            if not label:
                st.warning("Node label cannot be empty.")
            elif label in st.session_state["nodes"]:
                st.warning(f"Node '{label}' already exists.")
            else:
                st.session_state["nodes"].append(label)
                st.success(f"Added node '{label}'.")


def add_edge_ui():
    st.subheader("Add Edge (Weighted)")
    nodes = st.session_state["nodes"]

    with st.form("add_edge_form", clear_on_submit=True):
        if nodes:
            col1, col2 = st.columns(2)
            with col1:
                source = st.selectbox("Source", nodes, key="edge_source_select")
            with col2:
                target = st.selectbox("Target", nodes, key="edge_target_select")
        else:
            source = st.text_input("Source", key="edge_source_input")
            target = st.text_input("Target", key="edge_target_input")

        weight = st.number_input(
            "Weight", min_value=0.0, value=1.0, step=1.0, key="edge_weight_input"
        )
        submitted = st.form_submit_button("Add Edge")

        if submitted:
            source = str(source).strip()
            target = str(target).strip()

            if not source or not target:
                st.warning("Source and Target cannot be empty.")
                return

            if not nodes:
                for n in [source, target]:
                    if n not in st.session_state["nodes"]:
                        st.session_state["nodes"].append(n)

            updated_existing = False
            for e in st.session_state["edges"]:
                if {e["u"], e["v"]} == {source, target}:
                    e["weight"] = float(weight)
                    updated_existing = True
                    st.info(f"Updated weight of edge {source} - {target} to {weight}.")
                    break

            if not updated_existing:
                st.session_state["edges"].append(
                    {"u": source, "v": target, "weight": float(weight)}
                )
                st.success(f"Added edge {source} - {target} (w = {weight}).")


def sidebar_graph_controls():
    st.sidebar.header("Graph Input")

    testcase_list = ["None"] + list(TESTCASES.keys())
    chosen = st.sidebar.selectbox("Load Testcase from list", testcase_list)

    if st.sidebar.button("Load Selected Testcase"):
        if chosen != "None":
            load_testcase_graph(chosen)
            st.sidebar.success(f"Loaded {chosen}")
        else:
            st.sidebar.info("Please select a testcase first.")

    if st.sidebar.button("Clear Graph"):
        st.session_state["nodes"] = []
        st.session_state["edges"] = []
        st.session_state["testcase_meta"] = {}
        st.sidebar.success("Graph cleared.")

    st.sidebar.markdown("---")
    st.sidebar.write("You can also build a custom graph in the main panel.")


# --------------------------
# Streamlit App
# --------------------------

def main():
    st.set_page_config(page_title="Graph Algorithms Visualizer", layout="wide")

    init_session_state()
    sidebar_graph_controls()

    st.title("Graph Algorithms Visualizer (Streamlit + NetworkX)")
    st.write(
        "This web app lets you build a weighted graph, visualize it, and run "
        "classic graph algorithms: DFS/BFS spanning tree, Dijkstra shortest path, "
        "and MST (Prim & Kruskal)."
    )

    meta = st.session_state.get("testcase_meta", {})
    if meta.get("name"):
        st.info(
            f"Current testcase: {meta.get('name')} "
            f"(category: {meta.get('category', 'n/a')})"
        )

    left_col, right_col = st.columns([1, 2])

    with left_col:
        st.header("Graph Construction")
        add_node_ui()
        add_edge_ui()

        if st.session_state["nodes"] or st.session_state["edges"]:
            st.subheader("Current Nodes")
            st.write(st.session_state["nodes"])

            st.subheader("Current Edges")
            if st.session_state["edges"]:
                df_edges = pd.DataFrame(st.session_state["edges"])
                st.table(df_edges)
            else:
                st.write("No edges yet.")

    G = build_graph()

    with right_col:
        st.header("Graph Visualization")

        meta = st.session_state.get("testcase_meta", {})
        testcase_pos = meta.get("pos")

        if len(G.nodes) == 0:
            st.info("Add nodes and edges or load a testcase to visualize the graph.")
        else:
            fig = draw_graph(G, title="Current Graph", pos=testcase_pos)
            st.pyplot(fig, use_container_width=True)

        st.header("Algorithms")
        task = st.selectbox(
            "Select Task",
            [
                "Task 1: Spanning Tree Traversal (DFS/BFS)",
                "Task 2: Shortest Path (Dijkstra)",
                "Task 3: Minimum Spanning Tree (Prim/Kruskal)",
            ],
        )

        algo_engine = GraphAlgorithms(G)

        if task.startswith("Task 1"):
            if len(G.nodes) == 0:
                st.warning("Graph is empty. Add nodes and edges first.")
            else:
                st.subheader("Task 1: Spanning Tree Traversal")
                traversal_type = st.radio(
                    "Traversal Algorithm",
                    ["DFS", "BFS"],
                    horizontal=True,
                )

                meta = st.session_state.get("testcase_meta", {})
                recommended_start = meta.get("start")
                nodes_list = list(G.nodes())
                default_index = 0
                if recommended_start in nodes_list:
                    default_index = nodes_list.index(recommended_start)
                    st.caption(
                        f"Recommended start node for this testcase: '{recommended_start}'"
                    )

                start_node = st.selectbox(
                    "Start Node", nodes_list, index=default_index
                )

                if st.button("Run Traversal"):
                    if traversal_type == "DFS":
                        order, tree_edges = algo_engine.dfs_spanning_tree(start_node)
                    else:
                        order, tree_edges = algo_engine.bfs_spanning_tree(start_node)

                    st.success("Traversal order: " + " → ".join(order))
                    fig_traversal = draw_graph(
                        G,
                        highlight_edges=tree_edges,
                        highlight_nodes=order,
                        title=f"{traversal_type} Spanning Tree from '{start_node}'",
                        pos=testcase_pos,
                    )
                    st.pyplot(fig_traversal, use_container_width=True)

        elif task.startswith("Task 2"):
            if len(G.nodes) < 2:
                st.warning("Graph needs at least 2 nodes for shortest path.")
            else:
                st.subheader("Task 2: Shortest Path (Dijkstra)")

                meta = st.session_state.get("testcase_meta", {})
                rec_src = meta.get("start")
                rec_tgt = meta.get("target")

                nodes_list = list(G.nodes())

                def idx_or_zero(x):
                    return nodes_list.index(x) if x in nodes_list else 0

                if rec_src and rec_tgt:
                    st.caption(
                        f"Recommended for this testcase → Start = '{rec_src}', Destination = '{rec_tgt}'"
                    )

                col1, col2 = st.columns(2)
                with col1:
                    source = st.selectbox(
                        "Start Node",
                        nodes_list,
                        index=idx_or_zero(rec_src),
                        key="dij_source",
                    )
                with col2:
                    target = st.selectbox(
                        "Destination Node",
                        nodes_list,
                        index=idx_or_zero(rec_tgt),
                        key="dij_target",
                    )

                if st.button("Run Dijkstra"):
                    if source == target:
                        st.error("Start and destination must be different.")
                    else:
                        try:
                            path_nodes, total_weight, path_edges = (
                                algo_engine.dijkstra_shortest_path(source, target)
                            )
                            st.success(
                                f"Shortest path: {' → '.join(path_nodes)} "
                                f"(total weight = {total_weight})"
                            )
                            fig_path = draw_graph(
                                G,
                                highlight_edges=path_edges,
                                highlight_nodes=path_nodes,
                                title=f"Shortest Path: {source} → {target}",
                                pos=testcase_pos,
                            )
                            st.pyplot(fig_path, use_container_width=True)
                        except nx.NetworkXNoPath:
                            st.error(f"No path exists between '{source}' and '{target}'.")
                        except nx.NodeNotFound as e:
                            st.error(str(e))

        elif task.startswith("Task 3"):
            if len(G.nodes) == 0:
                st.warning("Graph is empty. Add nodes and edges first.")
            elif len(G.nodes) == 1:
                st.warning("Graph needs at least 2 nodes to compute an MST.")
            else:
                st.subheader("Task 3: Minimum Spanning Tree (MST)")
                mst_algo = st.radio(
                    "MST Algorithm",
                    ["Prim's Algorithm", "Kruskal's Algorithm"],
                    horizontal=True,
                )

                if st.button("Run MST"):
                    if mst_algo.startswith("Prim"):
                        mst_edges, total_weight = algo_engine.prim_mst()
                        algo_name = "Prim"
                    else:
                        mst_edges, total_weight = algo_engine.kruskal_mst()
                        algo_name = "Kruskal"

                    st.success(f"{algo_name} MST total weight = {total_weight}")
                    fig_mst = draw_graph(
                        G,
                        highlight_edges=mst_edges,
                        title=f"{algo_name} Minimum Spanning Tree",
                        pos=testcase_pos,
                    )
                    st.pyplot(fig_mst, use_container_width=True)


if __name__ == "__main__":
    main()
