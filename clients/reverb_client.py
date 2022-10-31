from framework.clients.http_client import HttpClient
from framework.configuration.configuration import Configuration
from framework.logger.providers import get_logger
from framework.serialization.utilities import serialize
from framework.validators.nulls import not_none
from models.order import Order, ShipOrderRequest
from models.shipengine import ShipEngineShipment, ShipEngineShipmentDetail
from utilities.helpers import select

from clients.identity_client import IdentityClient

logger = get_logger(__name__)


class ReverbClient:
    def __init__(self, container=None):
        self.__configuration: Configuration = container.resolve(
            Configuration)
        self.__identity_client: IdentityClient = container.resolve(
            IdentityClient)

        self.__api_key = self.__configuration.reverb.get('api_key')
        self.__base_url = self.__configuration.reverb.get('base_url')
        self.__ship_engine_gateway_url = self.__configuration.ship_engine.get(
            'gateway_base_url')

        self.__http_client: HttpClient = container.resolve(HttpClient)

    def __get_headers(
        self
    ) -> dict:
        return {
            'Authorization': f'Bearer {self.__api_key}'
        }

    async def get_order(
        self,
        order_number: str
    ) -> Order:
        logger.info(f'Get reverb order: {order_number}')

        response = await self.__http_client.get(
            url=f'{self.__base_url}/my/orders/selling/{order_number}',
            headers=self.__get_headers(),
            timeout=None)

        content = response.json()
        logger.info(f'Response status: {response.status_code}')
        logger.info(f'Response content: {serialize(content)}')

        return Order(content)

    async def __get_gateway_headers(
        self
    ) -> dict:
        logger.info('Fetching gateway token')

        token = await self.__identity_client.get_token(
            client_name='reverb-gateway-api')

        logger.info(f'Gateway token: {token}')
        return {
            'Authorization': f'Bearer {token}'
        }

    def validate_create_shipment(
        self,
        order: Order,
        shipment: ShipEngineShipment
    ):
        if order.paid_date is None:
            raise Exception('Order has not been paid')

        if order.shipping_address is None:
            raise Exception('Order shipping address cannot be null')

        not_none(order.shipping_address.city, 'city')
        not_none(order.shipping_address.state_code, 'state_code')
        not_none(order.shipping_address.street_address, 'street_address')
        not_none(order.shipping_address.postal_code, 'postal_code')
        not_none(order.shipping_address.country_code, 'country_code')
        not_none(order.shipping_address.phone_number, 'phone_number')
        not_none(order.shipping_address.recipient, 'recipient')

        if shipment.weight is None or shipment.weight == 0:
            raise Exception('Invalid shipment weight')

        if (shipment.insurance_provider == 'carrier'
            and float(shipment.insured_value or 0)
                < float(order.subtotal or 0)):
            raise Exception(
                'Shipment insured value must be greater than or equal to the order subtotal')

        return True

    async def create_shipengine_shipment(
        self,
        order_number,
        shipment_detail: dict
    ):
        order = await self.get_order(
            order_number=order_number)

        logger.info(f'Order: {serialize(order.to_dict())}')

        detail = ShipEngineShipmentDetail(
            data=shipment_detail)

        logger.info(f'Order: {serialize(shipment_detail)}')
        shipment = ShipEngineShipment(
            order=order,
            shipment_detail=detail)

        logger.info('Validating shipment request')
        self.validate_create_shipment(
            order=order,
            shipment=shipment)

        logger.info(
            f'Create shipment request: {serialize(shipment)}')

        endpoint = f'{self.__ship_engine_gateway_url}/api/shipment'
        headers = await self.__get_gateway_headers()

        logger.info(f'Endpoint: {endpoint}')
        logger.info(f'Headers: {serialize(headers)}')

        response = await self.__http_client.post(
            url=endpoint,
            json=shipment.to_dict(),
            headers=headers,
            timeout=None)

        if response.status_code != 200:
            raise Exception(f'Failed to create shipment: {response.text}')

        return {
            'shipment': shipment.to_dict(),
            'response': response.json()
        }

    async def get_orders(
        self,
        page_number
    ):
        logger.info('Fetching Reverb orders')

        response = await self.__http_client.get(
            f'{self.__base_url}/my/orders/selling/all?per_page=50&page={page_number}',
            headers=self.__get_headers(),
            timeout=None)

        logger.info(f'Response status code: {response.status_code}')

        content = response.json()
        total_pages = content.get('total_pages')

        orders = select(
            _iter=content.get('orders'),
            func=lambda x: Order(data=x))

        return {
            'orders': orders,
            'page_number': int(page_number),
            'total_pages': total_pages
        }

    async def add_tracking(
        self,
        order_number,
        request: ShipOrderRequest
    ):
        logger.info(f'Add tracking to order: {order_number}')
        logger.info(f'Request: {serialize(request.to_dict())}')

        response = await self.__http_client.post(
            f'{self.__base_url}/my/orders/selling/{order_number}/ship',
            json=request.to_json(),
            headers=self.__get_headers(),
            timeout=None)

        logger.info(f'Status: {response.status_code}')

        if response.status_code != 201:
            raise Exception(f'Failed to add tracking: {response.text}')

        return response.json()
