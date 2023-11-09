import pyfiglet
from rich import print
from typer import Typer

from taskforceagents import __description__ as DESCRIPTION
from taskforceagents import __title__ as NAME
from taskforceagents import __version__ as VERSION
from taskforceagents.config import load_config


def banner():
    return pyfiglet.figlet_format(NAME.replace("_", " ").title(), font="slant").rstrip()


app = Typer(help=f"{(NAME or '').replace('_', ' ').title()} CLI")


@app.command()
def info():
    """Prints info about the package"""
    print(f"{banner()}\n")
    print(f"{NAME}: {DESCRIPTION}")
    print(f"Version: {VERSION}\n")
    print(load_config())


@app.command()
def main():
    """Main Function"""
    print(f"{banner()}\n")
    print(
        "This is your default command-line interface.  Feel free to customize it as you see fit.\n"
    )
