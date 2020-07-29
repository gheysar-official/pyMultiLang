try:
    import sqlite3
except ImportError:
    raise ImportError('missing sqlite3')


class SqliteConnection:
    def __init__(self, file_path, **options):
        self.file_path = file_path
        self.connection_options = options
        self.conn = sqlite3.connect(file_path, **options)

    def get_cur(self):
        if self.is_closed():
            self.conn = sqlite3.connect(self.file_path, **self.connection_options)
        return self.conn.cursor()

    def is_closed(self):
        try:
            self.conn.execute("SELECT 1")
            return False
        except sqlite3.ProgrammingError as e:
            return True

    def execute_query(self, query, args=None):
        cur = self.get_cur()
        if args:
            cur.execute(query, args)
        else:
            cur.execute(query)
        self.conn.commit()
        cur.close()
