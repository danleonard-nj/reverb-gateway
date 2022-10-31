from clients.reverb_client import ReverbClient
from framework.auth.wrappers.azure_ad_wrappers import azure_ad_authorization
from framework.handlers.response_handler_async import response_handler
from quart import Blueprint, request

shipengine_bp = Blueprint('shipengine_bp', __name__)


@shipengine_bp.route('/api/shipengine/shipments/<order>', methods=['POST'], endpoint='create_shipment')
@response_handler
@azure_ad_authorization(scheme='write')
async def create_shipment(container, order):
    reverb_client: ReverbClient = container.resolve(ReverbClient)

    body = await request.get_json()

    shipment = await reverb_client.create_shipengine_shipment(
        order_number=order,
        shipment_detail=body)

    return {'shipment': shipment}
