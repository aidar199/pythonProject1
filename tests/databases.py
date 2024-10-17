import unittest

from database.main import database_main, User, Address, TypeAddress, engine
from sqlalchemy.orm import Session
from sqlalchemy import select


class testDatabase(unittest.TestCase):
    def test_select(self):
        self.assertIsNone(database_main())
    def test_add(self):
        user_1 = User(
            name="User 1",
            fullname="User 1 full",
            addresses=[
                Address(
                    type=TypeAddress.email,
                    address="user@mail.local"
                ),
                Address(
                    type=TypeAddress.telephone,
                    address="8(800)-000-00-00"
                ),
                Address(
                    type=TypeAddress.physical,
                    address="Russian Federation, RB"
                )
            ]
        )
        user_2 = User(
            name="User 2"
        )
        with Session(engine) as session:
            session.add_all([user_1, user_2])
            self.assertIsNone(session.commit())

    def test_select(self):
        session = Session(engine)
        user_stmt = select(User).where(User.name.in_(['users', 'user 1']))
        for user in session.scalars(user_stmt):
            self.assertIsInstance(user, User)
            stmt = (
                select(Address)
                .join(Address.user)
                .where(User.id == user.id)
                .where(Address.type == TypeAddress.email)
            )
            email = session.scalars(stmt).one()
            self.assertIsInstance(email, Address)

    def test_delete(self):
        session = Session(engine)
        user_stmt = select(User).where(User.name == 'User 1')
        user = session.scalars(user_stmt).one()
        session.commit()
        self.assertIsNone(session.delete(user))

    def test_select_all(self):

        # <editor-fold desc="Description">
        """session = Session(engine)
        stmt = select(User).where()
        for user in session.scalars(stmt):
            self.assertIsInstance(user, User)
        stmt = select(Address).where()
        for address in session.scalars(stmt):
            self.assertIsInstance(address, Address)
        """
        # </editor-fold>
        pass


if __name__ == '__main__':
    unittest.main()