from typing import List

from app.schemas import Edge, Node


def is_dag(nodes: List[Node], edges: List[Edge]) -> bool:
    """
    Returns True if the graph formed by nodes + edges is a
    Directed Acyclic Graph (DAG).

    Uses DFS with a 3-color visited state:
        0 = unvisited
        1 = currently in the recursion stack  ← back edge = cycle
        2 = fully processed
    """

    # ----------------------------------------------------------------
    # DAG check (DFS cycle detection)
    # ----------------------------------------------------------------

    # Build adjacency list
    graph: dict[str, list[str]] = {node.id: [] for node in nodes}
    for edge in edges:
        if edge.source in graph:
            graph[edge.source].append(edge.target)

    state: dict[str, int] = {node.id: 0 for node in nodes}

    def dfs(node_id: str) -> bool:
        state[node_id] = 1  # mark as in-progress
        for neighbor in graph.get(node_id, []):
            if state[neighbor] == 1:
                return False  # back edge found → cycle
            if state[neighbor] == 0 and not dfs(neighbor):
                return False
        state[node_id] = 2  # mark as done
        return True

    return all(dfs(n) for n in graph if state[n] == 0)
