from quart import Quart, request

from framework.dependency_injection.container import Container
from framework.dependency_injection.provider import ProviderBase
from framework.configuration.configuration import Configuration
from framework.abstractions.abstract_request import RequestContextProvider

from clients.identity_client import IdentityClient
from clients.reverb_client import ReverbClient
from services.reverb_service import ReverbService

from framework.auth.configuration import AzureAdConfiguration
from framework.auth.azure import AzureAd
from framework.clients.http_client import HttpClient


class AdRole:
    READ = 'Reverb.Read'
    WRITE = 'Reverb.Write'


def configure_azure_ad(container):
    configuration = container.resolve(Configuration)

    # Hook the Azure AD auth config into the service
    # configuration
    ad_auth: AzureAdConfiguration = configuration.ad_auth
    azure_ad = AzureAd(
        tenant=ad_auth.tenant_id,
        audiences=ad_auth.audiences,
        issuer=ad_auth.issuer)

    azure_ad.add_authorization_policy(
        name='read',
        func=lambda t: AdRole.READ in t.get('roles'))

    azure_ad.add_authorization_policy(
        name='write',
        func=lambda t: AdRole.WRITE in t.get('roles'))

    return azure_ad


class ContainerProvider(ProviderBase):
    @classmethod
    def configure_container(cls):
        container = Container()
        container.add_singleton(Configuration)
        container.add_singleton(IdentityClient)
        container.add_singleton(HttpClient)

        container.add_factory_singleton(
            _type=AzureAd,
            factory=configure_azure_ad)

        container.add_singleton(ReverbClient)
        container.add_singleton(ReverbService)
        return container.build()


def add_container_hook(app: Quart):
    def inject_container():
        RequestContextProvider.initialize_provider(
            app=app)
        if request.view_args != None:
            request.view_args['container'] = ContainerProvider.get_container()

    app.before_request_funcs.setdefault(
        None, []).append(
            inject_container)
