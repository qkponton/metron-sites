from typing import Dict

import pytest

from metron_sites.apis.v1 import site
from metron_sites.core.exception import BadRequestError

MODULE_PATH = "metron_sites.apis.v1.site"


@pytest.fixture(name="site_controller")
def site_controller_fixt(mocker):
    return mocker.patch(f"{MODULE_PATH}.SiteController")


@pytest.mark.unit
class TestCreateSite:

    @staticmethod
    def test_dict_returned(site_controller, site_body):
        assert site.create_site(site_body) == (dict(site=site_controller.create.return_value), 201)
        site_controller.create.assert_called_once_with(name="paris-east", power=100)

    @staticmethod
    @pytest.mark.usefixtures("site_controller")
    def test_bad_request_on_missing(site_body: Dict):
        site_body.pop("power")
        with pytest.raises(BadRequestError):
            site.create_site(site_body)


@pytest.mark.unit
class TestDeleteSite:

    @staticmethod
    def test_none_returned(site_controller, fake_uuid):
        assert site.delete_site(fake_uuid) == (None, 204)
        site_controller.delete.assert_called_once_with(fake_uuid)


@pytest.mark.unit
class TestGetSite:

    @staticmethod
    def test_dict_returned(site_controller, fake_uuid):
        assert site.get_site(fake_uuid) == dict(site=site_controller.get.return_value)
        site_controller.get.assert_called_once_with(fake_uuid)


@pytest.mark.unit
class TestListSite:

    @staticmethod
    def test_dict_returned(site_controller):
        assert site.list_site() == dict(sites=site_controller.list.return_value)
        site_controller.list.assert_called_once_with()


@pytest.mark.unit
class TestUpdateSite:

    @staticmethod
    def test_dict_returned(site_controller, fake_uuid, site_body):
        assert site.update_site(fake_uuid, site_body) == dict(site=site_controller.update.return_value)
        site_controller.update.assert_called_once_with(fake_uuid, name="paris-east", power=100)
