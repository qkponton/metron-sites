import pytest

from metron_sites.apis.v1 import machine_type

MODULE_PATH = "metron_sites.apis.v1.machine_type"


@pytest.fixture(name="machine_type_controller")
def machine_type_controller_fixt(mocker):
    return mocker.patch(f"{MODULE_PATH}.MachineTypeController")


@pytest.mark.unit
class TestListMachineTypes:

    @staticmethod
    def test_dict_returned(machine_type_controller):
        assert machine_type.list_machine_types() == dict(machine_types=machine_type_controller.list.return_value)
        machine_type_controller.list.assert_called_once_with()
