from logging import getLogger, basicConfig, DEBUG

from database.main import (database_main, add_addresses, TypeAddress, create_user,
                           select_user_one, add_address)

logger = getLogger()
basicConfig(level=DEBUG)


def create_users():
    create_user(
        "User",
        [
            add_addresses('user@mail.local', TypeAddress.email),
            add_addresses('9(999)999-99-99', TypeAddress.telephone),
        ],
        'User full name'
    )


def select_users():
    user, list_addresses = select_user_one('User')
    print(user, list_addresses)


def update_addresses():
    addresses = [
        add_addresses(
            address='Russian Federation',
            type_address=TypeAddress.physical
        )
    ]
    add_address('User', addresses)


if __name__ == '__main__':
    logger.info("Start app")
    database_main()
    # create_users()
    update_addresses()
    select_users()
