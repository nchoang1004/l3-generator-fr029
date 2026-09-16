"""Mô hình type/callable và operation của thư viện ngoài, có version cố định."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CallableModel:
    symbol: str
    kind: str
    returns: str | None = None
    returns_runtime: bool = False
    returns_symbol: str | None = None


@dataclass(frozen=True)
class TypeModel:
    symbol: str
    bases: tuple[str, ...] = ()
    methods: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class OperationModel:
    symbol: str
    operation: str
    positional: dict[str, int] = field(default_factory=dict)
    keywords: dict[str, str] = field(default_factory=dict)
    http_method: str | None = None


class SemanticRegistry:
    """Tra cứu O(1) theo symbol đầy đủ; không dò lần lượt mọi adapter."""

    version = "builtin-semantics-v1"

    def __init__(self) -> None:
        self.callables: dict[str, CallableModel] = {}
        self.types: dict[str, TypeModel] = {}
        self.operations: dict[str, OperationModel] = {}

    def add_type(self, model: TypeModel) -> None:
        self.types[model.symbol] = model
        self.callables[model.symbol] = CallableModel(model.symbol, "class", model.symbol)

    def add_callable(self, model: CallableModel) -> None:
        self.callables[model.symbol] = model

    def add_operation(self, model: OperationModel) -> None:
        self.operations[model.symbol] = model

    def method(self, type_symbol: str, name: str) -> str | None:
        return self._method(type_symbol, name, set())

    def _method(self, type_symbol: str, name: str, seen: set[str]) -> str | None:
        if type_symbol in seen:
            return None
        seen.add(type_symbol)
        model = self.types.get(type_symbol)
        if model is None:
            return None
        if name in model.methods:
            return model.methods[name]
        for base in model.bases:
            found = self._method(base, name, seen)
            if found:
                return found
        return None


def builtin_registry() -> SemanticRegistry:
    registry = SemanticRegistry()
    registry.add_type(TypeModel(
        "sqlalchemy.orm.Session",
        methods={name: f"sqlalchemy.orm.Session.{name}" for name in ("query", "get", "add", "delete", "merge", "commit", "flush", "rollback")},
    ))
    registry.add_callable(CallableModel("sqlalchemy.orm.sessionmaker", "function", returns_symbol="sqlalchemy.orm.Session"))
    for symbol in ("sqlalchemy.orm.DeclarativeBase", "sqlalchemy.orm.DeclarativeBaseNoMeta", "sqlmodel.SQLModel"):
        registry.add_type(TypeModel(symbol))
    for symbol in ("sqlalchemy.orm.declarative_base", "sqlalchemy.ext.declarative.declarative_base"):
        registry.add_callable(CallableModel(symbol, "function", returns_symbol="sqlalchemy.orm.DeclarativeBase"))
    for symbol in ("sqlalchemy.Column", "sqlalchemy.ForeignKey", "sqlalchemy.orm.mapped_column", "sqlalchemy.orm.relationship", "sqlmodel.Field", "sqlmodel.Relationship"):
        registry.add_callable(CallableModel(symbol, "function"))

    route_methods = {
        method: f"fastapi.routing.APIRouter.{method}"
        for method in ("get", "post", "put", "delete", "patch", "head", "options", "trace")
    }
    router_methods = {
        **route_methods,
        "include_router": "fastapi.routing.APIRouter.include_router",
        "add_api_route": "fastapi.routing.APIRouter.add_api_route",
    }
    registry.add_type(
        TypeModel(
            "starlette.applications.Starlette",
            methods={"mount": "starlette.applications.Starlette.mount"},
        )
    )
    registry.add_type(TypeModel("fastapi.routing.APIRouter", methods=router_methods))
    registry.add_type(
        TypeModel(
            "fastapi.FastAPI",
            bases=("starlette.applications.Starlette",),
            methods={name: f"fastapi.FastAPI.{name}" for name in router_methods},
        )
    )
    registry.add_type(TypeModel("fastapi.APIRouter", bases=("fastapi.routing.APIRouter",)))
    registry.add_type(TypeModel("fastapi.applications.FastAPI", bases=("fastapi.FastAPI",)))
    registry.add_type(TypeModel("starlette.staticfiles.StaticFiles"))
    registry.add_type(TypeModel("starlette.routing.Route"))

    registry.add_type(
        TypeModel(
            "httpx.Client",
            methods={verb: f"httpx.Client.{verb}" for verb in _HTTP_METHODS},
        )
    )
    registry.add_type(
        TypeModel(
            "httpx.AsyncClient",
            methods={verb: f"httpx.AsyncClient.{verb}" for verb in _HTTP_METHODS},
        )
    )
    registry.add_type(
        TypeModel(
            "requests.Session",
            methods={verb: f"requests.Session.{verb}" for verb in _HTTP_METHODS},
        )
    )
    for library in ("httpx", "requests"):
        for verb in _HTTP_METHODS:
            registry.add_callable(CallableModel(f"{library}.{verb}", "function"))

    registry.add_callable(CallableModel("builtins.getattr", "function", returns_runtime=True))
    registry.add_callable(CallableModel("importlib.import_module", "function", returns_runtime=True))

    for method in ("get", "post", "put", "delete", "patch", "head", "options", "trace"):
        registry.add_operation(
            OperationModel(
                f"fastapi.routing.APIRouter.{method}",
                "RegisterDecorator",
                positional={"path": 0},
                keywords={"path": "path"},
                http_method=method.upper(),
            )
        )
    registry.add_operation(
        OperationModel(
            "fastapi.routing.APIRouter.include_router",
            "AttachRouter",
            positional={"child": 0},
            keywords={"child": "router", "prefix": "prefix"},
        )
    )
    registry.add_operation(
        OperationModel(
            "starlette.applications.Starlette.mount",
            "MountApplication",
            positional={"path": 0, "child": 1},
            keywords={"child": "app", "path": "path"},
        )
    )
    registry.add_operation(
        OperationModel(
            "fastapi.routing.APIRouter.add_api_route",
            "RegisterEndpoint",
            positional={"path": 0, "endpoint": 1},
            keywords={"path": "path", "endpoint": "endpoint", "methods": "methods"},
        )
    )
    # FastAPI chuyển việc đăng ký tới router bên trong, nhưng chỉ kế thừa Starlette.
    # Bảng ý nghĩa vẫn giữ symbol của phương thức trên class sở hữu nó.
    for name in router_methods:
        operation = registry.operations.get(f"fastapi.routing.APIRouter.{name}")
        if operation:
            registry.add_operation(OperationModel(
                f"fastapi.FastAPI.{name}", operation.operation,
                operation.positional, operation.keywords, operation.http_method,
            ))
    return registry


_HTTP_METHODS = ("get", "post", "put", "delete", "patch", "head", "options", "request")
