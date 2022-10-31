from clients.reverb_client import ReverbClient
from framework.auth.wrappers.azure_ad_wrappers import azure_ad_authorization
from framework.handlers.response_handler_async import response_handler
from models.order import ShipOrderRequest
from models.requests import GetOrdersRequest
from quart import Blueprint, request
from services.reverb_service import ReverbService

reverb_bp = Blueprint('reverb_bp', __name__)


@reverb_bp.route('/api/orders', methods=['GET'], endpoint='get_orders')
@response_handler
@azure_ad_authorization(scheme='read')
async def get_orders(container):
    reverb_service: ReverbService = container.resolve(
        ReverbService)

    order_request = GetOrdersRequest(
        request=request)

    orders = await reverb_service.get_orders(
        request=order_request)

    return orders


@reverb_bp.route('/api/orders/<order>', methods=['GET'], endpoint='get_order')
@response_handler
@azure_ad_authorization(scheme='read')
async def get_order(container, order):
    reverb_client: ReverbClient = container.resolve(ReverbClient)

    order = await reverb_client.get_order(
        order_number=order)

    return {'order': order}


@reverb_bp.route('/api/orders/<order>/tracking', methods=['POST'], endpoint='add_tracking')
@response_handler
@azure_ad_authorization(scheme='write')
async def add_tracking(container, order):
    reverb_client: ReverbClient = container.resolve(
        ReverbClient)

    body = await request.get_json()
    order_request = ShipOrderRequest(
        data=body)

    order = await reverb_client.add_tracking(
        order_number=order,
        request=order_request)

    return {'order': order}
