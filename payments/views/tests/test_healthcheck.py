import mock
from alchemy_mock.mocking import AlchemyMagicMock

from payments.views import Healthcheck


class TestHealthcheck:
    def test_status_OK(self, mocker):
        session = AlchemyMagicMock()
        expected = {'status': 'OK'}

        response = Healthcheck.status(session)

        session.execute.assert_called_once_with("SELECT 1")
        assert response == expected
