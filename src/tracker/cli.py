import argparse

from .database import (
    init_db,
    add_application,
    get_all_applications,
    update_status,
    delete_application,
)
from .models import Application, Status


def build_parser():
    parser = argparse.ArgumentParser(prog="tracker", description="Job application tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_p = subparsers.add_parser("add", help="Add an application")
    add_p.add_argument("company")
    add_p.add_argument("title")
    add_p.add_argument("--url", default=None)
    add_p.add_argument("--notes", default=None)

    subparsers.add_parser("list", help="List all applications")

    status_p = subparsers.add_parser("status", help="Change an application's status")
    status_p.add_argument("id", type=int)
    status_p.add_argument("new_status", choices=[s.value for s in Status])

    delete_p = subparsers.add_parser("delete", help="Delete an application")
    delete_p.add_argument("id", type=int)

    return parser


def main():
    args = build_parser().parse_args()
    init_db()

    if args.command == "add":
        app = Application(args.company, args.title, job_url=args.url, notes=args.notes)
        new_id = add_application(app)
        print(f"Added application #{new_id}")

    elif args.command == "list":
        applications = get_all_applications()
        if not applications:
            print("No applications yet.")
        for a in applications:
            print(f"#{a.id}  {a.company} - {a.title}  [{a.status.value}]")

    elif args.command == "status":
        if update_status(args.id, Status(args.new_status)):
            print(f"Updated application #{args.id} to {args.new_status}")
        else:
            print(f"Application #{args.id} not found")

    elif args.command == "delete":
        if delete_application(args.id):
            print(f"Deleted application #{args.id}")
        else:
            print(f"Application #{args.id} not found")