from typing import Any

import attrs

from data_diff_customize.abcs.database_types import TemporalType, ColType_UUID
from data_diff_customize.databases import presto
from data_diff_customize.databases.base import import_helper
from data_diff_customize.databases.base import TIMESTAMP_PRECISION_POS


@import_helper("trino")
def import_trino():
    import trino

    return trino


class Dialect(presto.Dialect):
    name = "Trino"

    def normalize_timestamp(self, value: str, coltype: TemporalType) -> str:
        if coltype.rounds:
            s = f"date_format(cast({value} as timestamp({coltype.precision})), '%Y-%m-%d %H:%i:%S.%f')"
        else:
            s = f"date_format(cast({value} as timestamp(6)), '%Y-%m-%d %H:%i:%S.%f')"

        return (
            f"RPAD(RPAD({s}, {TIMESTAMP_PRECISION_POS + coltype.precision}, '.'), {TIMESTAMP_PRECISION_POS + 6}, '0')"
        )

    def normalize_uuid(self, value: str, coltype: ColType_UUID) -> str:
        return f"TRIM({value})"


@attrs.define(frozen=False, init=False, kw_only=True)
class Trino(presto.Presto):
    dialect = Dialect()
    CONNECT_URI_HELP = "trino://<user>@<host>/<catalog>/<schema>"
    CONNECT_URI_PARAMS = ["catalog", "schema"]

    _conn: Any

    def __init__(self, **kw):
        super().__init__(**kw)
        trino = import_trino()

        if kw.get("schema"):
            self.default_schema = kw.get("schema")

        if kw.get("auth") == "basic":
            kw["auth"] = trino.auth.BasicAuthentication(kw["user"], kw.pop("password"))
            kw["http_scheme"] = "https"
            kw["verify"] = False

        self._conn = trino.dbapi.connect(**kw)
