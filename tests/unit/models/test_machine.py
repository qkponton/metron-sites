import pytest

from metron_sites.models.machine import Machine


@pytest.fixture(name="site")
def site_fixt(mocker):
    return mocker.MagicMock()


@pytest.fixture(name="machine_type")
def machine_type_fixt(mocker):
    return mocker.MagicMock()


@pytest.mark.unit
class TestMachineModel:

    @staticmethod
    def test_model_as_dict(machine_body, site, machine_type, fake_uuid):
        machine = Machine(machine_id=fake_uuid, machine_name=machine_body.get("name"),
                          machine_power=machine_body.get("power"), site_id=machine_body.get("site"),
                          machine_type_id=machine_body.get("type"))
        machine.site = site
        machine.machine_type = machine_type
        assert machine.to_dict() == dict(id=fake_uuid, name="printer", power=10, site=site.site_name,
                                         type=machine_type.machine_type_name)
