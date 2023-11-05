import time

def three_dots(delay=1):
    print(".", end="", flush=True, delay=1)
    time.sleep(delay)
    print(".", end="", flush=True)
    time.sleep(delay)
    print(".", end="", flush=True)
    time.sleep(delay)
    print()