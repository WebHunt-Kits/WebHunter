"""commands
Example:
    
    import click
    
    @click.command()
    def hello():
        '''hello'''
        print("hello")


Usage:

    # in settings
    COMMANDS = [
        ...
        'api.commands.hello'
        ...
    ]
"""
import click
from flask.cli import with_appcontext

from core.extensions import db


@click.command()
@with_appcontext
def init_db():
    """init models
    """
    db.create_all()
