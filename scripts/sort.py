import sys
import subprocess
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    screen = Console()


def init():
    if len(sys.argv) == 1:
        screen.print("Error: You must enter inputs!", style="red")
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("With the sort command you can sort numbers or letters.", style="green")
    elif len(sys.argv) >= 2 and sys.argv[1] != "-h":
        digit_type = True

        for inp in sys.argv[1:]:
            if not inp.isdigit():
                digit_type = False

        if digit_type:
            inputs_list = sorted(map(int, sys.argv[1:]))
            inputs_list = map(str, inputs_list)
            screen.print(', '.join(inputs_list))
        else:
            screen.print(', '.join(sorted(sys.argv[1:])))


if __name__ == "__main__":
    init()
