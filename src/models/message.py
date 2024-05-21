from sqlalchemy.orm import Mapped, mapped_column
import os 
import sys 

sys.path.append(os.path.join(sys.path[0][:-6]))

from connect_db import Base

class Table_id(Base): 
    __tablename__ = "last_id"
    id: Mapped[int] = mapped_column(primary_key=True)
    last_message_id: Mapped[int]