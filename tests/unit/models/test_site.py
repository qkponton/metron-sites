import pytest

from metron_sites.models.site import Site


@pytest.mark.unit
class TestSiteModel:

    @staticmethod
    def test_model_as_dict(site_body, fake_uuid):
        site = Site(site_id=fake_uuid, site_name=site_body.get("name"), site_power=site_body.get("power"))
        assert site.to_dict() == dict(id=fake_uuid, name="paris-east", power=100)
