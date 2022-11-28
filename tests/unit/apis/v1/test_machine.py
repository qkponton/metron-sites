from typing import Dict

import pytest

from metron_sites.apis.v1 import machine
from metron_sites.core.exception import BadRequestError

MODULE_PATH = "metron_sites.apis.v1.machine"


@pytest.fixture(name="machine_controller")
def machine_controller_fixt(mocker):
    return mocker.patch(f"{MODULE_PATH}.MachineController")


@pytest.mark.unit
class TestCreateMachine:

    @staticmethod
    def test_dict_returned(machine_controller, machine_body, fake_uuid):
        assert machine.create_machine(machine_body) == (dict(machine=machine_controller.create.return_value), 201)
        machine_controller.create.assert_called_once_with(name="printer", power=10, site_id=fake_uuid,
                                                          machine_type_name=fake_uuid)

    @staticmethod
    @pytest.mark.usefixtures("machine_controller")
    def test_bad_request_on_missing(machine_body: Dict):
        machine_body.pop("type")
        with pytest.raises(BadRequestError):
            machine.create_machine(machine_body)


@pytest.mark.unit
class TestDeleteMachine:

    @staticmethod
    def test_none_returned(machine_controller, fake_uuid):
        assert machine.delete_machine(fake_uuid) == (None, 204)
        machine_controller.delete.assert_called_once_with(fake_uuid)


@pytest.mark.unit
class TestGetMachine:

    @staticmethod
    def test_dict_returned(machine_controller, fake_uuid):
        assert machine.get_machine(fake_uuid) == dict(machine=machine_controller.get.return_value)
        machine_controller.get.assert_called_once_with(fake_uuid)


@pytest.mark.unit
class TestListMachine:

    @staticmethod
    def test_dict_returned(machine_controller):
        assert machine.list_machine() == dict(machines=machine_controller.list.return_value)
        machine_controller.list.assert_called_once_with()


@pytest.mark.unit
class TestUpdateMachine:

    @staticmethod
    def test_dict_returned(machine_controller, fake_uuid, machine_body):
        assert machine.update_machine(fake_uuid, machine_body) == dict(machine=machine_controller.update.return_value)
        machine_controller.update.assert_called_once_with(fake_uuid, name="printer", power=10)
