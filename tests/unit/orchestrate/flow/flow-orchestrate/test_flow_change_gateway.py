import pytest

from jina import Flow
from jina.enums import GatewayProtocolType
from tests import random_docs


@pytest.mark.slow
@pytest.mark.parametrize('protocol', ['http', 'websocket', 'grpc'])
@pytest.mark.parametrize('changeto_protocol', ['grpc', 'http', 'websocket'])
def test_change_gateway(protocol, changeto_protocol):
    f = Flow(protocol=protocol).add().add().add(needs='executor1').needs_all()

    with f:
        da = f.post('/', random_docs(10))
        assert len(da) == 10
        with pytest.raises(RuntimeError):
            f.protocol = changeto_protocol


@pytest.mark.parametrize('protocol', ['http', 'websocket', 'grpc'])
def test_get_set_client_gateway_in_flow(protocol):
    f = Flow(protocol=protocol, port=12345)
    assert f.client_args.protocol == GatewayProtocolType.from_string(protocol)
    assert f.gateway_args.protocol == GatewayProtocolType.from_string(protocol)
    assert int(f.client_args.port) == 12345
    assert int(f.gateway_args.port) == 12345
    f._update_network_interface(port=54321)
    assert int(f.client_args.port) == 54321
    assert int(f.gateway_args.port) == 54321
