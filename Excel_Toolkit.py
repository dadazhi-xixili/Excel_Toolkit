import webview
from SQLite import SQLite

class api(SQLite):
    def __init__(self):
        pass
    def update_content(self):
        pass
    def del_all(self):
        pass
    
if __name__ == "__main__":
    
    win = webview.create_window(
        title="Excel Toolkit",
        url="Excel_Toolkit.html",
        text_select=True,
        width=1000,
        height=800,
        js_api=api(),
    )
    
    webview.settings["OPEN_DEVTOOLS_IN_DEBUG"] = False
    webview.start(debug=True)