from logging import getLogger, basicConfig, DEBUG


from database.main import database_main


logger = getLogger()
basicConfig(level=DEBUG)


if __name__ == '__main__':
    logger.info("Start app")
    database_main()