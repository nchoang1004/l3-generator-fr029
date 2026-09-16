"""Node và cạnh của graph (SPEC mục 5.2).

Graph không phải nguồn dữ liệu mới. Nó là cùng dữ liệu trong IAM, trình bày theo
dạng node và cạnh. Không được thêm bất cứ thứ gì không có nguồn gốc trong IAM.
"""

from typing import Literal

from pydantic import BaseModel, Field

from l3gen.models.iam import SourceLocation

NodeType = Literal[
    "Module",
    "Application",
    "Class",
    "Function",
    "Route",
    "Entity",
    "ExternalHost",
    "Unresolved",
]
EdgeType = Literal[
    "calls",
    "imports",
    "inherits",
    "constructs",
    "exposes",
    "registers",
    "mounts",
    "reads",
    "writes",
    "reads_writes",
    "calls_external",
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
    fact_ids: list[str] = Field(default_factory=list)
    locations: list[SourceLocation] = Field(default_factory=list)


class ApplicationBoundary(BaseModel):
    id: str
    status: Literal["candidate", "unknown"]
    application_node_id: str | None = None
    entrypoint_file: str | None = None
    evidence: list[str] = Field(default_factory=list)
    reason: str


class RepositoryGraph(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]
    application_boundaries: list[ApplicationBoundary] = Field(default_factory=list)
