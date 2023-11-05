from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import threading
from .utils import *

def main():
    threading.Thread(target=block_keyboard).start()
    threading.Thread(target=show_error).start()

if __name__ == "__main__":
    main()