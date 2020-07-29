from ..datasources.SqliteSource import SqliteConnection


class Session:
    def __init__(
            self,
            database_path: str
    ):
        self.db_path = database_path
        self.db = SqliteConnection(database_path)

    def add_new_lang(self, lang_title: str, lang_code: str):
        query = "insert into languages(language_code,language_title) values (?,?)"
        cur = self.db.get_cur()
        cur.execute(query, (lang_code.upper(), lang_title.capitalize()))
        self.db.conn.commit()
        cur.close()

    def add_new_string(self, lang_code: str, key: str, value: str):
        query = "insert into strings(language_id,key,value) values (?,?,?)"
        languages = self.get_languages(key='code')
        language = languages.get(lang_code.upper())
        lang_id = language['id']
        cur = self.db.get_cur()
        cur.execute(query, (lang_id, key, value))
        self.db.conn.commit()
        cur.close()

    def get_languages(self, key='id'):
        if key == 'id':
            key = 0
        elif key == 'code':
            key = 1
        else:
            raise KeyError('key "%s" not found, id and code are available', key)
        query = "select id, language_code, language_title from languages"
        cur = self.db.get_cur()
        cur.execute(query)
        res = cur.fetchall()
        return {lang[key]: {'id': lang[0], 'code': lang[1], 'title': lang[2]} for lang in res}
