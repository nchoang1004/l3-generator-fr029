"""Node và cạnh của graph (SPEC mục 5.2).

Graph không phải nguồn dữ liệu mới. Nó là cùng dữ liệu trong IAM, trình bày theo
dạng node và cạnh. Không được thêm bất cứ thứ gì không có nguồn gốc trong IAM.
"""

from typing import Literal

from pydantic import BaseModel

from l3gen.models.iam import SourceLocation

NodeType = Literal[
    "Module", "Class", "Function", "Route", "Entity", "ExternalHost", "Unresolved"
]
EdgeType = Literal[
    "calls", "imports", "inherits", "exposes", "reads_writes", "calls_external"
]


class GraphNode(BaseModel):
    id: str
    type: NodeType
    label: str
    location: SourceLocation | None


class GraphEdge(BaseModel):
    source_id: str
    target_id: str
    type: EdgeType
    resolved: bool


class RepositoryGraph(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]
