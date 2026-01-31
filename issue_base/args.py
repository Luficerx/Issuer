import argparse as ap
from .core import IssueManager

Parser = ap.ArgumentParser(
    prog="Issue",
    description="Creates and list issues present in current directory."
    )

Parser.add_argument("-n", action="store_true", help="Create a new issue.") 
Parser.add_argument("-l", action="store_true", help="List all issues available.")
Parser.add_argument("-D", action="store_true", help="Remove all issues that are closed.")
Parser.add_argument("-id", type=str, help="List id by it's id if available.", nargs="?")
Parser.add_argument("-d", type=str, help="Remove issue by id.")
Parser.add_argument("-u", type=int, help="List issues by their urgence if >= to -u/-urge.")
Parser.add_argument("-U", type=int, help="List issues by their urgence if == to -U/-URGE.")
Parser.add_argument("-c", nargs="+", help="A list of id's used to close issues if they exist.")