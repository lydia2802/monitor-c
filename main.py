"""Entry point for the phone/NIK tracking CLI.

The application code lives in the pegasus/ package; this thin wrapper keeps
`python main.py` working from the repository root.
"""

from pegasus.main import main
from pegasus.utils.helpers import handle_exception, handle_keyboard_interrupt

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        handle_keyboard_interrupt()
    except Exception as e:
        handle_exception(e)
