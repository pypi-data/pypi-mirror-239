# ansqlite

A python3 module to assist in small sqlite3 database use cases.

## Install

```shell
python3 -m pip install ansqlite
```

## Usage

```python
from ansqlite import Database, Datatype, PrimaryKeyType

tablename = 'tablename'
 
db = Database(
    database_path='/path/to/database/file.db',
    schemas={
        tablename: [
            {
                "name": "timestamp",
                "datatype": Datatype.INTEGER,
                "primary_key": PrimaryKeyType.Descending,
            },
            {
                "name": "value",
                "datatype": Datatype.REAL,
            },            
        ],
        'othertablename': [
            {
                "name": "hash",
                "datatype": Datatype.TEXT,
                "primary_key": PrimaryKeyType.Ascending,
            },
            {
                "name": "text",
                "datatype": Datatype.TEXT,
            },            
        ],        
    }
)

db.insert_data(
    table_name=tablename,
    data=[
        {'timestamp': 1699304400, 'value': 4.496},
        {'timestamp': 1699300800, 'value': 6.812},
        {'timestamp': 1699297200, 'value': 7.847},
        {'timestamp': 1699293600, 'value': 9.548}
    ]
)

db.execute_and_commit(
    sql=f'UPDATE {tablename} SET value=1.00 WHERE timestamp=1699300800;',
    errmsg='Failed to set value'
)

rows = db.execute_and_fetchall(
    sql=f'SELECT * FROM {tablename} where timestamp >= 1699297200 and timestamp < 1699304400 limit 10;',
    errmsg='Failed to retrieve data'
  )

print(rows)
```
