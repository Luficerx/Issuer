from datetime import datetime
from typing import Any
from pathlib import Path

import argparse, os
import json

class _StaticBase():
    def __init_subclass__(cls, **kwargs):
        for key, value in cls.__dict__.items():
            if callable(value) and not key.startswith('_'):
                setattr(cls, key, classmethod(value))

class Issue():
    def __init__(self, name: str, info: str | None, date: Any, urge: int = 0, closed: bool = False):
        self.name = name
        self.info = info
        self.date = date
        self.urge = urge
        self.closed = closed

    def display(self):
        print(f"{self.name} - '{self.date}'")
        print(f"    INFO: {self.info}")
        if self.closed:
            print(f"    STATUS: CLOSED")
        else:
            print(f"    URGE: {self.urge}°")
            print(f"    STATUS: OPEN")

    def __repr__(self) -> str:
        return f'"{self.name}" "{self.info}" "{self.date}" [{self.urge}] [{self.closed}]'

class IssueManager(_StaticBase):
    base_dir: str | None = None
    issues = {}

    def new_issue(self, **kwargs):
        print("** Creating a new issue **")

        try:
            levels = 4
            name = input("Name: ").strip()

            if name in self.issues:
                yn = input(f"Issue with name {name} already exists, Override? [Y/n] default: Y").strip().lower()

                if not yn or "y" == yn or "yes" == yn:
                    return

                if (not yn == "n") or (not yn == "no"):
                    print(f"Unknown value: {yn}, Cancelling operation.")
                    raise KeyboardInterrupt

            info = input("Info: ").strip()
            urge = input("Urge: ").strip()

            try:
                urge = int(urge)
            
            except:
                urge = 0

            for i in range(levels):
                print("\033[1A\033[K", end="")

            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.issues[date] = Issue(name, info, date, urge)

            print(f"** A new issue written to file '{date}.is' was created. **")
            print()
            self.issues[date].display()

            self.update_issues_dir()
        
        except KeyboardInterrupt as e:
            print("\nOperation cancelled.")

    def list_issues(self) -> list[Issue]:
        issues = list(self.issues.values())
        if issues:
            for issue in sorted(issues, key=lambda i: i.urge, reverse=True):
                issue.display()
        else:
            print("There are no issues available.")

    def set_base_dir(self, path: str):
        self.base_dir = path

    def list_issues_by_urge(self, urge: int) -> list[Issue]:
        for issue in self.issues.values():
            if issue.urge >= urge:
                issue.display()

    def match_issues_by_urge(self, urge: int) -> list[Issue]:
        for issue in self.issues.values():
            if issue.urge == urge:
                issue.display()

    def list_issues_by_id(self, id: int):
        try:
            print(f"** Searching by id **")
            issue = self.issues.get(id, None)

            if issue is not None:
                for i in range(2):
                    print("\033[1A\033[K", end="")

                issue.display()

            else:
                print(f"No issue file with id {id} found.")
        
        except KeyboardInterrupt as e:
            print("\nOperation cancelled.")

    def update_issues_dir(self):
        os.makedirs(self.issuesdir(), exist_ok=True)

        for (key, issue) in self.issues.items():
            filename = self.issuesdir().joinpath(key + ".is")
            with open(filename, "w+") as fl:
                fl.write(json.dumps(issue.__dict__))

    def load_issues_from_dir(self):
        if self.issuesdir().is_dir():
            for file in self.issuesdir().rglob("*"):
                if file.name.endswith(".is"):
                    with open(file, "r") as fl:
                        data = json.load(fl)
                        self.issues[file.stem] = Issue(**data)

    def close_issues(self, keys):
        closed_issues = []

        for key in keys:
            issue = self.issues.get(key, None)
            if issue is not None:
                issue.closed = True
                closed_issues.append(issue.name)
        
        if closed_issues:
            print(f"The following issues were closed: {closed_issues}")
        
        self.update_issues_dir()
    
    def delete_issue_by_id(self, id: str):
        if self.issuesdir().is_dir():
            for file in self.issuesdir().rglob("*"):
                if file.stem == id:
                    os.remove(file)
                    self.issues.pop(id)

                    break

    def delete_closed_issues(self):
        to_delete = [key for (key, issue) in self.issues.items() if issue.closed]

        if self.issuesdir().is_dir():
            for todel in to_delete:
                for file in self.issuesdir().rglob("*"):
                    if file.stem == todel:
                        os.remove(file)
                            
                self.issues.pop(todel)

    def issuesdir(self) -> Path:
        return Path(self.base_dir, "issues")