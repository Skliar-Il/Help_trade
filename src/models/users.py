from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text
from typing import Annotated
import datetime
import os 
import sys
 
 
sys.path.append(os.path.join(sys.path[0][:-6]))

from connect_db import Base

class Table_Users(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    tg_id: Mapped[int]
    tg_teg: Mapped[str]
    create_time: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    