from typing import Dict

import pytest
from werkzeug.exceptions import NotFound

from metron_sites.apis.v1 import site
from metron_sites.controllers.site_controller import SiteController
from metron_sites.core.exception import BadRequestError, DbError, SiteQuotaError
from metron_sites.models.machine import Machine
from metron_sites.models.site import Site

MODULE_PATH = "metron_sites.controllers.site_controller"


@pytest.fixture(name="db_controller")
def db_controller_fixt(mocker):
    return mocker.patch(f"{MODULE_PATH}.DbController")


@pytest.fixture(name="site_model")
def site_fixt(mocker):
    return mocker.patch(f"{MODULE_PATH}.Site")


@pytest.mark.unit
class TestCheckQuota:

    @staticmethod
    def test_no_exception_when_enough_quota(site_body, fake_uuid):
        site = Site(site_id=fake_uuid, site_name=site_body.get("name"), site_power=site_body.get("power"))
        machine = Machine(machine_id=fake_uuid, machine_name="printer", machine_power=10, site_id=fake_uuid, machine_type_id=fake_uuid)
        site.machines = [machine] * 3
        SiteController.check_quota(site, 10)

    @staticmethod
    def test_exception_when_not_enough_quota(site_body, fake_uuid):
        site = Site(site_id=fake_uuid, site_name=site_body.get("name"), site_power=site_body.get("power"))
        machine = Machine(machine_id=fake_uuid, machine_name="printer", machine_power=10, site_id=fake_uuid, machine_type_id=fake_uuid)
        site.machines = [machine] * 100
        with pytest.raises(SiteQuotaError):
            SiteController.check_quota(site, 10)


@pytest.mark.unit
class TestCreateSite:

    @staticmethod
    def test_site_returned(db_controller, site_model, site_body, fake_uuid):
        assert SiteController.create(name=site_body.get("name"), power=site_body.get("power")) == site_model.return_value
        site_model.assert_called_once_with(site_name="paris-east", site_power=100)
        db_controller.insert.assert_called_once_with(site_model.return_value)

    @staticmethod
    def test_site_when_failed_to_insert(db_controller, site_model, site_body, fake_uuid):
        db_controller.insert.side_effect = DbError("any")
        assert SiteController.create(name=site_body.get("name"), power=site_body.get("power")) == db_controller.get_by.return_value
        site_model.assert_called_once_with(site_name="paris-east", site_power=100)
        db_controller.insert.assert_called_once_with(site_model.return_value)
        db_controller.get_by.assert_called_once_with(site_model, site_name="paris-east")


@pytest.mark.unit
class TestDeleteSite:

    @staticmethod
    def test_site_deleted(db_controller, site_model, fake_uuid):
        assert SiteController.delete(fake_uuid) is None
        db_controller.delete.assert_called_once_with(site_model, fake_uuid)


@pytest.mark.unit
class TestGetSite:

    @staticmethod
    def test_site_returned(db_controller, site_model, fake_uuid):
        assert SiteController.get(fake_uuid) == db_controller.get.return_value
        db_controller.get.assert_called_once_with(site_model, fake_uuid)


@pytest.mark.unit
class TestListSite:

    @staticmethod
    def test_site_list_returned(db_controller, site_model):
        assert SiteController.list() == list(db_controller.list.return_value)
        db_controller.list.assert_called_once_with(table=site_model)


@pytest.mark.unit
class TestUpdateSite:

    @staticmethod
    def test_site_returned(db_controller, site_model, site_body, fake_uuid):
        assert SiteController.update(fake_uuid, name=site_body.get("name"),
                                        power=site_body.get("power")) == db_controller.update.return_value
        db_controller.update.assert_called_once_with(site_model, fake_uuid, site_name=site_body.get("name"),
                                                     site_power=site_body.get("power"))

    @staticmethod
    def test_update_without_power(db_controller, site_model, site_body, fake_uuid):
        assert SiteController.update(fake_uuid, name=site_body.get("name")) == db_controller.update.return_value
        db_controller.update.assert_called_once_with(site_model, fake_uuid, site_name=site_body.get("name"))

    @staticmethod
    def test_update_without_name(db_controller, site_model, site_body, fake_uuid):
        assert SiteController.update(fake_uuid, power=site_body.get("power")) == db_controller.update.return_value
        db_controller.update.assert_called_once_with(site_model, fake_uuid, site_power=site_body.get("power"))

    @staticmethod
    def test_update_without_attributes(db_controller, site_model, fake_uuid):
        assert SiteController.update(fake_uuid,) == db_controller.update.return_value
        db_controller.update.assert_called_once_with(site_model, fake_uuid)

    @staticmethod
    def test_bad_request_when_db_error(db_controller, site_model, site_body, fake_uuid):
        db_controller.update.side_effect = DbError("any")
        with pytest.raises(BadRequestError):
            SiteController.update(fake_uuid, name=site_body.get("name"), power=site_body.get("power"))
        db_controller.update.assert_called_once_with(site_model, fake_uuid, site_name=site_body.get("name"),
                                                     site_power=site_body.get("power"))
