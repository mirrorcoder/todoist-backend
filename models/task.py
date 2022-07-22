from extensions import db
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text


class Task(db.Model):
    id = Column(Integer, primary_key=True)
    name_user = Column(String, nullable=False)
    email_user = Column(String, nullable=False)
    desc_task = Column(Text, nullable=False)
    is_edit_admin = Column(Boolean, default=False)
    is_done = Column(Boolean, default=False)

