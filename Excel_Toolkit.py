from json import load
import webview


class Api:
    def __init__(this):
        with open("Excel_Toolkit.json", "r", encoding="utf-8") as file:
            this.data = load(file)
        this.level_1 = list(this.data.keys())
        this.level_2 = {}
        this.level_3 = {}

    def get_data(this):
        return this.data

    def get_level_1(this):
        return this.level_1

    def get_level_2(this, key="文本"):
        data = this.data[key].items()
        this.level_2 = {k: v["synopsis"] for k, v in data}
        return this.level_2

    def get_level_3(this, key="文本"):
        data = this.data[key].items()
        this.level_3 = {k: v["data"] for k, v in data}
        return this.level_3


if __name__ == "__main__":
    win = webview.create_window(
        title="Excel Toolkit",
        url="Excel_Toolkit.html",
        js_api=Api(),
    )
    webview.start(
        debug=True,
    )
    