from _typeshed import Incomplete

class SqlDatabase:
    debug: Incomplete
    home: Incomplete
    version: float
    database: Incomplete
    schema: Incomplete
    table: Incomplete
    sql_insert: Incomplete
    sql_query: Incomplete
    dataq: Incomplete
    db_version: Incomplete
    def __init__(self, database: str = ..., schema: Incomplete | None = ..., table: Incomplete | None = ..., insert: Incomplete | None = ..., debug: bool = ...) -> None: ...
    def queue(self, data: dict) -> None: ...
    def insert(self, method: str = ..., index: str = ..., aggregation: str = ...) -> None: ...
    def latest_datapoint(self) -> str: ...
