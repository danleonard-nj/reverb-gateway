from unittest.mock import Mock
from framework.middleware.authorization import AuthMiddleware
from framework.dependency_injection.container import Dependency, DependencyType
from utilities.provider import ContainerProvider


def inject_test_dependency(_type, instance):
    container = ContainerProvider.get_container()
    container._container[_type] = Dependency(
        _type=_type,
        reg_type=DependencyType.SINGLETON,
        instance=instance)


def inject_mock_middleware():
    auth_middleware = Mock()
    auth_middleware.validate_access_token = Mock(
        return_value=True)

    inject_test_dependency(
        _type=AuthMiddleware,
        instance=auth_middleware)
