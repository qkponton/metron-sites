from typing import Dict

import pytest
from werkzeug.exceptions import NotFound

from metron_sites.apis.v1 import machine
from metron_sites.controllers.machine_controller import MachineController
from metron_sites.core.exception import BadRequestError, DbError

MODULE_PATH = "metron_sites.controllers.machine_controller"


@pytest.fixture(name="db_controller")
def db_controller_fixt(mocker):
    return mocker.patch(f"{MODULE_PATH}.DbController")


@pytest.fixture(name="machine_type_controller")
def machine_type_fixt(mocker):
    return mocker.patch(f"{MODULE_PATH}.MachineTypeController")


@pytest.fixture(name="site_controller")
def site_controller_fixt(mocker):
    return mocker.patch(f"{MODULE_PATH}.SiteController")


@pytest.fixture(name="machine_model")
def machine_fixt(mocker):
    return mocker.patch(f"{MODULE_PATH}.Machine")


@pytest.mark.unit
class TestCreateMachine:

    @staticmethod
    def test_machine_returned(db_controller, machine_type_controller, site_controller, machine_model, machine_body, fake_uuid):
        assert MachineController.create(name=machine_body.get("name"),
                                        power=machine_body.get("power"),
                                        site_id=machine_body.get("site"),
                                        machine_type_name="any") == machine_model.return_value
        machine_type_controller.get_by.assert_called_once_with("any")
        site_controller.get.assert_called_once_with(fake_uuid)
        site_controller.check_quota.assert_called_once_with(site_controller.get.return_value, 10)
        machine_model.assert_called_once_with(machine_name="printer", machine_power=10,
                                              machine_type_id=machine_type_controller.get_by.return_value.machine_type_id, site_id=fake_uuid)
        db_controller.insert.assert_called_once_with(machine_model.return_value)

    @staticmethod
    def test_machine_when_failed_to_insert(db_controller, machine_type_controller, site_controller, machine_model, machine_body, fake_uuid):
        db_controller.insert.side_effect = DbError("any")
        assert MachineController.create(name=machine_body.get("name"),
                                        power=machine_body.get("power"),
                                        site_id=machine_body.get("site"),
                                        machine_type_name="any") == db_controller.get_by.return_value
        machine_type_controller.get_by.assert_called_once_with("any")
        site_controller.get.assert_called_once_with(fake_uuid)
        site_controller.check_quota.assert_called_once_with(site_controller.get.return_value, 10)
        machine_model.assert_called_once_with(machine_name="printer", machine_power=10,
                                              machine_type_id=machine_type_controller.get_by.return_value.machine_type_id, site_id=fake_uuid)
        db_controller.insert.assert_called_once_with(machine_model.return_value)
        db_controller.get_by.assert_called_once_with(machine_model, machine_name="printer", site_id=fake_uuid,
                                                     machine_type_id=machine_type_controller.get_by.return_value.machine_type_id)

    @staticmethod
    def test_bad_request_when_not_found(machine_type_controller, machine_body):
        machine_type_controller.get_by.side_effect = NotFound
        with pytest.raises(BadRequestError):
            MachineController.create(name=machine_body.get("name"), power=machine_body.get("power"), site_id=machine_body.get("site"),
                                     machine_type_name="any")


@pytest.mark.unit
class TestDeleteMachine:

    @staticmethod
    def test_machine_deleted(db_controller, machine_model, fake_uuid):
        assert MachineController.delete(fake_uuid) is None
        db_controller.delete.assert_called_once_with(machine_model, fake_uuid)


@pytest.mark.unit
class TestGetMachine:

    @staticmethod
    def test_machine_returned(db_controller, machine_model, fake_uuid):
        assert MachineController.get(fake_uuid) == db_controller.get.return_value
        db_controller.get.assert_called_once_with(machine_model, fake_uuid)


@pytest.mark.unit
class TestListMachine:

    @staticmethod
    def test_machine_list_returned(db_controller, machine_model):
        assert MachineController.list() == list(db_controller.list.return_value)
        db_controller.list.assert_called_once_with(table=machine_model)


@pytest.mark.unit
class TestUpdateMachine:

    @staticmethod
    def test_machine_returned(db_controller, machine_model, machine_body, fake_uuid):
        assert MachineController.update(fake_uuid, name=machine_body.get("name"),
                                        power=machine_body.get("power")) == db_controller.update.return_value
        db_controller.update.assert_called_once_with(machine_model, fake_uuid, machine_name=machine_body.get("name"),
                                                     machine_power=machine_body.get("power"))

    @staticmethod
    def test_update_without_power(db_controller, machine_model, machine_body, fake_uuid):
        assert MachineController.update(fake_uuid, name=machine_body.get("name")) == db_controller.update.return_value
        db_controller.update.assert_called_once_with(machine_model, fake_uuid, machine_name=machine_body.get("name"))

    @staticmethod
    def test_update_without_name(db_controller, machine_model, machine_body, fake_uuid):
        assert MachineController.update(fake_uuid, power=machine_body.get("power")) == db_controller.update.return_value
        db_controller.update.assert_called_once_with(machine_model, fake_uuid, machine_power=machine_body.get("power"))

    @staticmethod
    def test_update_without_attributes(db_controller, machine_model, fake_uuid):
        assert MachineController.update(fake_uuid,) == db_controller.update.return_value
        db_controller.update.assert_called_once_with(machine_model, fake_uuid)

    @staticmethod
    def test_bad_request_when_db_error(db_controller, machine_model, machine_body, fake_uuid):
        db_controller.update.side_effect = DbError("any")
        with pytest.raises(BadRequestError):
            MachineController.update(fake_uuid, name=machine_body.get("name"), power=machine_body.get("power"))
        db_controller.update.assert_called_once_with(machine_model, fake_uuid, machine_name=machine_body.get("name"),
                                                     machine_power=machine_body.get("power"))
