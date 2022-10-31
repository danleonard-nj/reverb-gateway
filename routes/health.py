from quart import Blueprint, request

from framework.logger.providers import get_logger

logger = get_logger(__name__)

health_bp = Blueprint('health_bp', __name__)


@health_bp.route('/api/health/alive', endpoint='alive')
def alive(container):
    return {'status': 'ok'}, 200


@health_bp.route('/api/health/ready', endpoint='ready')
def ready(container):
    return {'status': 'ok'}, 200
