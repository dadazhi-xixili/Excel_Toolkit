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
        游标.execute("SELECT * FROM 内容表")
        return 游标.fetchall()

    def del_all(self):
        """清空内容表"""
        游标 = self._get_cursor()
        游标.execute("DELETE FROM 内容表")

    def insert(self, 数据列表):
        """批量插入数据"""
        游标 = self._get_cursor()
        游标.executemany(
            "INSERT INTO 内容表 (一级菜单, 二级菜单, 概述, 内容) VALUES (?, ?, ?, ?)",
            数据列表,
        )

    def get(self, 关键字, search_content=True, search_summary=False) -> list[dict]:
        """关键词搜索"""
        if not 关键字:
            return []

        conditions = []
        params = [f"%{关键字}%"]

        if search_content:
            conditions.append("内容 LIKE ?")
        if search_summary:
            conditions.append("概述 LIKE ?")

        if not conditions:
            return []

        sql = f"SELECT * FROM 内容表 WHERE {' OR '.join(conditions)}"
        游标 = self._get_cursor()
        游标.execute(sql, params)
        return [
            {"level1": x[0], "level2": x[1], "info": x[2], "content": x[3]}
            for x in 游标.fetchall()
        ]

    def update_content(self, 一级菜单, 二级菜单, 新内容, immediate_commit=False):
        """更新指定菜单的内容"""
        游标 = self._get_cursor()
        游标.execute(
            "UPDATE 内容表 SET 内容=? WHERE 一级菜单=? AND 二级菜单=?",
            (新内容, 一级菜单, 二级菜单),
        )
        if immediate_commit:
            self.commit()
        return 游标.rowcount

    def get_by_menu(self, 一级菜单=None, 二级菜单=None) -> dict:
        """按菜单条件查询"""
        sql = "SELECT * FROM 内容表 WHERE 1=1"
        params = []

        if 一级菜单:
            sql += " AND 一级菜单=?"
            params.append(一级菜单)
        if 二级菜单:
            sql += " AND 二级菜单=?"
            params.append(二级菜单)

        游标 = self._get_cursor()
        游标.execute(sql, params)
        return dict(zip(["level1", "level2", "info", "content"], 游标.fetchall()[0]))

    def get_level1(self) -> list[str]:
        """获取所有一级菜单(去重)"""
        游标 = self._get_cursor()
        游标.execute("SELECT DISTINCT 一级菜单 FROM 内容表 ORDER BY 一级菜单")
        return [row[0] for row in 游标.fetchall()]

    def get_level2(self, 一级菜单) -> list[dict]:
        """获取指定一级菜单下的所有二级菜单项"""
        游标 = self._get_cursor()
        游标.execute(
            "SELECT 一级菜单, 二级菜单, 概述 FROM 内容表 WHERE 一级菜单=? GROUP BY 二级菜单",
            (一级菜单,),
        )
        return [{"level1": x[0], "level2": x[1], "info": x[2]} for x in 游标.fetchall()]

    def __enter__(self):
        """支持with语句"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出with语句时自动关闭连接"""
        self.close()
