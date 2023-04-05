import webbrowser


def open_in_browser(url: str):
    webbrowser.open(url, new=2, autoraise=True)
