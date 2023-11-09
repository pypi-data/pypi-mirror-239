import json
import sqlite3
from pydantic import BaseModel, create_model
from typing import Dict, List
from ansqlite.schema import TableColumn, PrimaryKeyType
from ansqlite.utils import trace


class Database:
    def __init__(
        self,
        database_path: str,
        schemas: Dict[str, List[TableColumn]] = {},
        debug: bool = False
    ):
        super().__init__()
        self.debug = debug
        self.schemas: Dict[str, List[TableColumn]] = {}
        self.models: Dict[str, BaseModel] = {}

        try:
            self.dbconn = sqlite3.connect(database_path)
        except Exception as e:
            trace('Failed to open database', e)
            self.dbconn = None

        for k, v in schemas.items():
            self.init_table(table_name=k, table_schema=v)

    def init_table(self, table_name: str, table_schema: List[TableColumn]) -> bool:
        schema = []
        model_entries = {}
        for col in table_schema:
            x = TableColumn.model_validate(col)
            not_nullable = x.nullable is False
            s = [
                x.name,
                x.datatype.name
            ]
            if (x.primary_key is not None):
                s.append('PRIMARY KEY DESC' if x.primary_key ==
                         PrimaryKeyType.Descending else 'PRIMARY KEY')
            else:
                if not_nullable:
                    s.append('NOT NULL')
            schema.append(' '.join(s))
            model_entries[x.name] = (
                x.datatype.value, ... if not_nullable else None)

        self.models[table_name] = create_model(table_name, **model_entries)

        try:
            cur = self.dbconn.cursor()
            cur.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(schema)});")
            self.schemas[table_name] = table_schema

        except Exception as e:
            trace('Failed to initialize table', e)
            self.dbconn = None

    def check_connection(self) -> bool:
        return self.dbconn is not None

    def get_connection(self) -> sqlite3.Connection:
        print('dbconn', self.dbconn is not None)
        return self.dbconn

    def insert_data(
        self,
        table_name: str,
        data: List[BaseModel],
    ) -> None:
        if len(data) < 1:
            return

        if self.debug:
            print(
                f'Save data to table {table_name}: {json.dumps(data, indent=2)}')

        schema = self.schemas[table_name] if table_name in self.schemas else None
        if schema is None:
            raise Exception(
                f'Table {table_name} has not been initialized; saving data failed')

        model = self.models[table_name]

        cols = model.model_validate(data[0]).model_dump().keys()
        rowdata = [tuple(model.model_validate(row).model_dump().values())
                   for row in data]

        try:
            cur = self.dbconn.cursor()
            cur.executemany(
                f"INSERT OR IGNORE INTO {table_name} ({', '.join(cols)}) VALUES ({', '.join('?'*len(cols))})", rowdata)
            self.dbconn.commit()
        except Exception as e:
            trace('Failed to save data', e)
            raise e

    def execute_and_fetchall(self, sql: str, errmsg: str) -> List[Dict] | None:
        try:
            cur = self.dbconn.cursor()
            res = cur.execute(sql)
            rows = res.fetchall()
            cols = [description[0] for description in cur.description]
            data = [dict(zip(cols, row)) for row in rows]
            return data
        except Exception as e:
            trace(errmsg, e)
            raise e

    def execute_and_commit(self, sql: str, errmsg: str) -> None:
        try:
            cur = self.dbconn.cursor()
            cur.execute(sql)
            self.dbconn.commit()
        except Exception as e:
            trace(errmsg, e)
            raise e
