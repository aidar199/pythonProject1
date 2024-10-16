from logging import getLogger, basicConfig, DEBUG


logger = getLogger()
basicConfig(level=DEBUG)


if __name__ == '__main__':
    logger.info("Start app")