import pytest

from metron_sites.models.machine_type import MachineType


@pytest.fixture(name="site")
def site_fixt(mocker):
    return mocker.MagicMock()


@pytest.fixture(name="machine_type")
def machine_type_fixt(mocker):
    return mocker.MagicMock()


@pytest.mark.unit
class TestMachineTypeModel:

    @staticmethod
    def test_model_as_dict(fake_uuid):
        machine_type = MachineType(machine_type_id=fake_uuid, machine_type_name="any")
        assert machine_type.to_dict() == dict(id=fake_uuid, name="any")
