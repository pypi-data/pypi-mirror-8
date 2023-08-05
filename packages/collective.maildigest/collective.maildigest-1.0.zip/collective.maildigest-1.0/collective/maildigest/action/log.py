from collective.maildigest import logger

from collective.maildigest.action import BaseAction


class Log(BaseAction):

    def execute(self, portal, storage, subscriber, info):
        logger.info("%s digest info for %s : %s", storage.key, subscriber[1], info)