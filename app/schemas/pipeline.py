from typing import List

from pydantic import BaseModel, ConfigDict


class Node(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str


class Edge(BaseModel):
    model_config = ConfigDict(extra="ignore")
    source: str
    target: str


class PipelineRequest(BaseModel):
    nodes: List[Node]
    edges: List[Edge]


class PipelineResponse(BaseModel):
    num_nodes: int
    num_edges: int
    is_dag: bool
