from datetime import datetime
import duckdb

DB_PATH = '/Users/hrikshit/duckdb/markets/na/sp500.db'

def load_sp500(table_name='history', start_date='2020-01-01', end_date=datetime.today().date()):
    with duckdb.connect(DB_PATH) as con:
        qry = f"select * from {table_name} where Date between '{start_date}' and '{end_date}'"
        history = con.execute(qry).df()
        return history