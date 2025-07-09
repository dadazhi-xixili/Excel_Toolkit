from json import load
import webview
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
    webview.settings['OPEN_DEVTOOLS_IN_DEBUG'] = False
    webview.start(debug=True)
