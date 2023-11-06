import logging

from prometheus_client import pushadd_to_gateway

from prometheus_client_utils.push_clients.base import BasePushClient

logger = logging.getLogger('prometheus_client_utils')


class PushGatewayClient(BasePushClient):
    async def push(self):
        logger.debug(f'Started pushing "{self.__class__.__name__}"')

        pushadd_to_gateway(self.address, self.job, self.registry)
