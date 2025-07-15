import sqlite3
import threading


class SQLite:
    def __init__(self):
        self.本地 = threading.local()
        self._init_db()

    def _init_db(self):
        """Initialize thread-local database connection"""
        if not hasattr(self.本地, "连接"):
            self.本地.连接 = sqlite3.connect(
                "Excel_Toolkit.db", check_same_thread=False
            )
            self.本地.连接.row_factory = sqlite3.Row
            self.本地.游标 = self.本地.连接.cursor()
            self.本地.游标.execute("PRAGMA foreign_keys = ON")

    def _get_cursor(self):
        """Get thread-local cursor"""
        if not hasattr(self.本地, "游标"):
            self._init_db()
        return self.本地.游标

    def commit(self):
        """提交更改到数据库"""
        self.本地.连接.commit()
        return self

    def close(self):
        """关闭数据库连接"""
        if hasattr(self.本地, "连接"):
            self.本地.连接.close()
            del self.本地.连接
            del self.本地.游标

    def all(self):
        """获取全部数据"""
        游标 = self._get_cursor()
        游标.execute("SELECT * FROM 内容")
        return [dict(x) for x in 游标.fetchall()]

    def del_all(self):
        """清空内容"""
        游标 = self._get_cursor()
        游标.execute("DELETE FROM 内容")

    def insert(self, 数据列表: list[tuple]):
        """批量插入数据"""
        游标 = self._get_cursor()
        游标.executemany(
            "INSERT INTO 内容(id,level1,level2,info,content,markdown) VALUES (?,?,?,?,?,?)",
            数据列表,
        )

    def get(self, keyword, search_content=True, search_info=True, search_level2=True):
        """关键词搜索（任意指定列包含关键字即返回）"""
        if not keyword:
            return 
        conditions = []
        params = []
        search_pattern = f"%{keyword}%"
        column_conditions = [
            (search_content, "markdown"),
            (search_info, "info"),
            (search_level2, "level2")
        ]
        
        for should_search, column in column_conditions:
            if should_search:
                conditions.append(f"{column} LIKE ?")
                params.append(search_pattern)
        if not conditions:
            return 
        sql = f"""
        SELECT * 
        FROM 内容 
        WHERE {' OR '.join(conditions)}
        """
        cursor = self._get_cursor()
        cursor.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_by_menu(self, level1=None, level2=None):
        """按菜单条件查询"""
        sql = "SELECT * FROM 内容 WHERE 1=1"
        params = []

        if level1 is not None:
            sql += " AND level1=?"
            params.append(level1)
        if level2 is not None:
            sql += " AND level2=?"
            params.append(level2)

        游标 = self._get_cursor()
        游标.execute(sql, params)
        return dict(游标.fetchall()[0])

    def get_level1(self) -> list[dict]:
        """获取所有一级菜单(去重)"""
        游标 = self._get_cursor()
        游标.execute("""
            SELECT MIN(id) as id, level1 
            FROM 内容 
            GROUP BY level1 
            ORDER BY id ASC
                   """)
        return [dict(x) for x in 游标.fetchall()]

    def get_level2(self, 一级菜单) -> list[dict]:
        """获取指定一级菜单下的所有二级菜单项"""
        游标 = self._get_cursor()
        游标.execute(
            "SELECT * FROM 内容 WHERE level1=? GROUP BY level2 ORDER BY id ASC",
            (一级菜单,)
        )
        return [dict(x) for x in 游标.fetchall()]
