import sqlite3 as sql

db = sql.connect('baze.db')
user = db.cursor()


def baze_start():
    list_of_tables = user.execute("""SELECT name
                                    FROM sqlite_master
                                    WHERE type='table' AND name='pleer';
                                    """).fetchall()

    if list_of_tables == []:
        user.execute('''CREATE TABLE IF NOT EXISTS pleer(
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        time INTEGER
                        )''')
        db.commit()
    else:
        print('Table found!')

def crate_win_list():

    d = user.execute('''SELECT name FROM pleer
                    order by time desc
                    limit 5
                    ''').fetchall()
    # top_pleer = [row['id'] for row in d]

    return d


def add_pleer(name, time):
    info = (f"{name}", time)
    user.execute(f'''INSERT INTO pleer (name, time)
                VALUES (?, ?)''', info)
    db.commit()

