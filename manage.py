from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app
from app.ext.database.flask_sqlalchemy import db

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.run()