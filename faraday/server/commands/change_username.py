import sys
import click

from faraday.server.web import get_app
from faraday.server.models import User, db


def change_username(current_username, new_username):
    with get_app().app_context():
        if user := User.query.filter_by(username=current_username).first():
            print(f"\nThe user named {current_username} will be changed to {new_username}.")
            confirm = click.prompt("Do you want to continue? (y/n)")
            print("")

            if confirm == "y":
                user.username = new_username
                db.session.add(user)
                db.session.commit()
                print(f"Username {current_username} changed to {new_username}")
            else:
                print("Username not changed.")

        else:
            print(f"\nERROR: User {current_username} was not found in Faraday's Database.")
            sys.exit(1)


# I'm Py3
