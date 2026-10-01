"""A small ASCII cat shown as Catscii's startup banner."""

_CYAN = "\x1b[36m"
_RESET = "\x1b[0m"

CAT_BANNER = (
    f"{_CYAN}"
    "\n /\\_/\\\n( o.o ) Catscii\n > ^ <  turn any image into ASCII art\n"
    f"{_RESET}"
)


def print_banner():
    print(CAT_BANNER)
