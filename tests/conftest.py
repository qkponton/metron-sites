import pytest


@pytest.fixture(name="fake_uuid")
def fake_uuid_fxt():
    return "49a49c94-3623-4b23-b40e-194b0f8fa84c"


@pytest.fixture(name="machine_body")
def machine_body_fixt(fake_uuid):
    return dict(name="printer", power=10, site=fake_uuid, type=fake_uuid)


@pytest.fixture(name="site_body")
def site_body_fixt(fake_uuid):
    return dict(name="paris-east", power=100)
