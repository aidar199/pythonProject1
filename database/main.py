from typing import Optional, List
import enum
from logging import getLogger

from sqlalchemy import String, ForeignKey, create_engine, select
from sqlalchemy.dialects.postgresql import array
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


def create_user(name: str, list_addresses, fullname: str = '') -> None:
    with Session(engine) as session:
        session.add(
            User(
                name=name,
                fullname=fullname,
                addresses=list_addresses
            )
        )
        session.commit()
        logger.debug('Add user: %s', name)


def add_addresses(address: str, type_address: TypeAddress) -> Address:
    return Address(
        type=type_address,
        address=address
    )


def select_user_one(name: str) -> (User, List[Address]):
    session = Session(engine)
    stmt = select(User).where(User.name == name)
    user = session.scalars(stmt).one()
    stmt = select(Address).where(Address.user_id == user.id)
    list_address = [address for address in session.scalars(stmt)]
    return user, list_address
