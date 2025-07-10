import webview
from SQLite import SQLite


if __name__ == "__main__":
    
    win = webview.create_window(
        title="Excel Toolkit",
        url="Excel_Toolkit.html",
        text_select=True,
        width=1000,
        height=800,
        js_api=SQLite(),
    )
    
    webview.settings["OPEN_DEVTOOLS_IN_DEBUG"] = False
    webview.start(debug=True)