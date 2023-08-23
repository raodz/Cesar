import sqlite3
import pandas as pd


def db_to_df(db: str):
    conn = sqlite3.connect(db)

    sql_query = pd.read_sql_query(
        """
                                   SELECT
                                   *
                                   FROM History
                                   """,
        conn,
    )

    df = pd.DataFrame(
        sql_query,
        columns=["txt", "shift", "direction", "shifted_txt", "time_of_crypting"],
    )
    return df


def df_to_db(df: pd.DataFrame, db: str):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute(
        "CREATE TABLE IF NOT EXISTS History(id INTEGER PRIMARY KEY, txt TEXT "
        "NOT NULL, shift INTEGER, direction TEXT, shifted_txt TEXT NOT NULL, "
        "time_of_crypting DATETIME);"
    )
    conn.commit()

    df.to_sql("History", conn, if_exists="replace", index=False)

    c.execute(
        """
    SELECT * FROM History
              """
    )
