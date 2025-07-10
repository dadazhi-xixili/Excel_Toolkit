import webview
from SQLite import SQLite

if __name__ == "__main__":
    try :
        api = SQLite()
        win = webview.create_window(
            title="Excel Toolkit",
            url="Excel_Toolkit.html",
            text_select=True,
            width=1000,
            height=800,
            js_api=api,
        )

        webview.settings["OPEN_DEVTOOLS_IN_DEBUG"] = False
        webview.start(debug=True)
    except Exception as e:
        print(f"发生未知错误: {e}")
    finally:
        if api:
            api.close()