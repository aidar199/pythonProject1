from typing import Optional, List
import enum
from logging import getLogger


from sqlalchemy import String, ForeignKey, create_engine
from sqlalchemy.orm import (DeclarativeBase, Mapped,
                            mapped_column, relationship, Session)


logger = getLogger(__name__)
engine = create_engine("sqlite:///base.db")


class TypeAddress(enum.Enum):
    email: bool = True
    telephone: bool = True
    physical: bool = True


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")
    type: Mapped["TypeAddress"]
    address: Mapped[str] = mapped_column(String(500))

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, type={self.type!r}, address={self.address})"

def database_main() -> None:
    logger.debug("create metadata")
    Base.metadata.create_all(engine)