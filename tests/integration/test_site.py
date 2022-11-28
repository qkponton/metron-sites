from __future__ import absolute_import

import json
from unittest.mock import ANY

import pytest

from tests.integration.test_integration import TestIntegration


@pytest.mark.integration
class TestSite(TestIntegration):
    """SiteController integration test stubs"""

    def test_list_empty(self):
        """Test case for get_user_by_name

        Get operands
        """
        response = self.client.get("/site")
        assert response.status_code == 200
        assert json.loads(response.data.decode()) == dict(sites=[])

    def test_nominal_scenario(self):
        """Test case for get_user_by_name

        Get operands
        """
        # Create site
        response = self.client.post("/site", json=dict(name="paris-test", power=100))
        assert response.status_code == 201
        site = json.loads(response.data.decode())
        assert site == dict(site=dict(id=ANY, name="paris-test", power=100))
        # List all sites
        response = self.client.get("/site")
        assert response.status_code == 200
        assert json.loads(response.data.decode()) == dict(sites=[dict(id=ANY, name="paris-test", power=100)])
        # Get site
        response = self.client.get(f"/site/{site.get('site').get('id')}")
        assert response.status_code == 200
        assert json.loads(response.data.decode()) == dict(site=dict(id=ANY, name="paris-test", power=100))
        # Update site
        response = self.client.put(f"/site/{site.get('site').get('id')}", json=dict(power=110))
        assert response.status_code == 200
        site = json.loads(response.data.decode())
        assert site == dict(site=dict(id=ANY, name="paris-test", power=110))
        # Delete site
        response = self.client.delete(f"/site/{site.get('site').get('id')}")
        assert response.status_code == 204
        # List all sites
        response = self.client.get("/site")
        assert response.status_code == 200
        assert json.loads(response.data.decode()) == dict(sites=[])
        # Get site
        response = self.client.get(f"/site/{site.get('site').get('id')}")
        assert response.status_code == 404
