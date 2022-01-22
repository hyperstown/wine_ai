import sys
from wine_ai.utils import print_debug
from wine_ai.engine import WineHelper
from database.init_db import init_now

try:
    from gui.main_window import render_window
except ImportError:
    def render_window(*args, **kwargs):
        print("Could not import PyQt")


def main():
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    # args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    if "--init" in opts or "--init-db" in opts:
        print_debug("Database initialized!")
        init_now()
    elif "--no-gui" in opts:
        engine = WineHelper()
        try:
            engine.reset()
            engine.run()
        except KeyboardInterrupt:
            print("\nExiting...")
    else:
        render_window()


if __name__ == '__main__':
    main()
