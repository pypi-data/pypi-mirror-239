import traceback


def trace(msg: str, e: Exception):
    print(traceback.format_exception(e))
    print(f"{msg}; {e}")
