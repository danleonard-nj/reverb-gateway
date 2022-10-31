
from framework.logger.providers import get_logger
from quart import Quart

from routes.health import health_bp
from routes.reverb import reverb_bp
from routes.shipengine import shipengine_bp
from utilities.provider import add_container_hook
from framework.serialization.serializer import configure_serializer

logger = get_logger(__name__)

app = Quart(__name__)

configure_serializer(app)

app.register_blueprint(health_bp)
app.register_blueprint(reverb_bp)
app.register_blueprint(shipengine_bp)

add_container_hook(app)


if __name__ == '__main__':
    app.run(debug=True, port='5088')
