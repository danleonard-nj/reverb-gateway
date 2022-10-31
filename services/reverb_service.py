from clients.reverb_client import ReverbClient
from framework.logger.providers import get_logger
from models.requests import GetOrdersRequest

logger = get_logger(__name__)


class ReverbService:
    def __init__(self, container):
        self.client: ReverbClient = container.resolve(ReverbClient)

    async def get_orders(
        self,
        request: GetOrdersRequest
    ):
        logger.info(f'Get orders: {request.to_dict()}')

        orders = await self.client.get_orders(
            page_number=request.page_number)

        return orders
