from json import load
import webview
import sqlite3


class SQLite:
    def __init__(self):
        self.连接 = sqlite3.connect("Excel_Toolkit.db")
        self.游标 = self.连接.cursor()

    def commit(self):
        """提交更改"""
        self.连接.commit()

    def close(self):
        """关闭连接"""
        self.连接.close()

    def all(self) -> list[tuple[str, str, str, str]]:
        """获取全部数据"""
        self.游标.execute("SELECT * FROM 内容表")
        return self.游标.fetchall()

    def del_all(self):
        """清空表"""
        self.游标.execute("DELETE FROM 内容表")

    def insert(self, 数据列表: list[tuple[str, str, str, str]]):
        """批量插入数据"""
        self.游标.executemany("INSERT INTO 内容表 VALUES (?,?,?,?)", 数据列表)

    def get(
        self, 关键字, 搜索内容=True, 搜索概述=False
    ) -> list[tuple[str, str, str, str]]:
        """关键词搜索"""
        if not 关键字:
            return []

        conditions = []
        params = [f"%{关键字}%"]

        if 搜索内容:
            conditions.append("内容 LIKE ?")
        if 搜索概述:
            conditions.append("概述 LIKE ?")

        if not conditions:
            return []

        sql = f"SELECT * FROM 内容表 WHERE {' OR '.join(conditions)}"
        self.游标.execute(sql, params)
        return self.游标.fetchall()

    def update_content(self, 一级菜单, 二级菜单, 新内容, 立刻更新=False) -> int:
        """按菜单组合更新内容"""
        self.游标.execute(
            "UPDATE 内容表 SET 内容=? WHERE 一级菜单=? AND 二级菜单=?",
            (新内容, 一级菜单, 二级菜单),
        )
        if 立刻更新:
            self.commit()
        return self.游标.rowcount

    def get_by_menu(self, 一级菜单="", 二级菜单="") -> list[tuple[str, str, str, str]]:
        """按菜单查询"""
        sql = "SELECT * FROM 内容表 WHERE 1=1"
        params = []

        if 一级菜单:
            sql += " AND 一级菜单=?"
            params.append(一级菜单)
        if 二级菜单:
            sql += " AND 二级菜单=?"
            params.append(二级菜单)

        self.游标.execute(sql, params)
        return self.游标.fetchall()

    def get_level1(self) -> list[str]:
        """获取所有不重复的一级菜单列表"""
        self.游标.execute("SELECT DISTINCT 一级菜单 FROM 内容表 ORDER BY 一级菜单")
        return [row[0] for row in self.游标.fetchall()]

    def get_level2(self, 一级菜单) -> list[tuple[str, str]]:
        """
        根据一级菜单获取所有二级菜单及其概述
        返回格式: [(二级菜单1, 概述1), (二级菜单2, 概述2), ...]
        """
        self.游标.execute(
            "SELECT DISTINCT 二级菜单, 概述 FROM 内容表 WHERE 一级菜单=? ORDER BY 二级菜单",
            (一级菜单,),
        )
        return self.游标.fetchall()


class Api:
    def __init__(this):
        with open("Excel_Toolkit.json", "r", encoding="utf-8") as file:
            this.data = load(file)

    def get_content(this, path):
        with open(path, "r", encoding="utf-8") as file:
            return file.read()


if __name__ == "__main__":
    win = webview.create_window(
        title="Excel Toolkit",
        url="Excel_Toolkit.html",
        text_select=True,
        width=1000,
        height=800,
        js_api=Api(),
        # frameless=True,
        # easy_drag=True,
    )
    webview.settings["OPEN_DEVTOOLS_IN_DEBUG"] = False
    webview.start(debug=True)
