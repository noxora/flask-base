from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
users = Table('users', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('email', VARCHAR(length=255), nullable=False),
    Column('confirmationTime', DATETIME),
    Column('password', VARCHAR(length=255), nullable=False),
    Column('curr_active', BOOLEAN, nullable=False),
    Column('first_name', VARCHAR(length=40), nullable=False),
    Column('last_name', VARCHAR(length=40), nullable=False),
)

users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('email', Unicode(length=255), nullable=False),
    Column('confirmed_at', DateTime),
    Column('password', String(length=255), nullable=False),
    Column('curr_active', Boolean, nullable=False),
    Column('first_name', String(length=40), nullable=False),
    Column('last_name', String(length=40), nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['users'].columns['confirmationTime'].drop()
    post_meta.tables['users'].columns['confirmed_at'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['users'].columns['confirmationTime'].create()
    post_meta.tables['users'].columns['confirmed_at'].drop()
