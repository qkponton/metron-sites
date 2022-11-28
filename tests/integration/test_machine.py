from __future__ import absolute_import

import json
from unittest.mock import ANY

import pytest

from tests.integration.test_integration import TestIntegration


@pytest.mark.integration
class TestMachine(TestIntegration):
    """MachineController integration test stubs"""
    fake_uuid = "49a49c94-3623-4b23-b40e-194b0f8fa84c"

    def test_list_empty(self):
        response = self.client.get("/machine")
        assert response.status_code == 200
        assert json.loads(response.data.decode()) == dict(machines=[])

    def test_400_when_unknown_site(self):
        response = self.client.post("/machine", json=dict(name="printer", power=10, type="chiller", site=10))
        assert response.status_code == 400
        response = self.client.post("/machine", json=dict(name="printer", power=10, type="chiller", site=TestMachine.fake_uuid))
        assert response.status_code == 400

    def test_400_when_unknown_type(self):
        # Create site
        response = self.client.post("/site", json=dict(name="paris-test", power=100))
        assert response.status_code == 201
        site = json.loads(response.data.decode())
        response = self.client.post("/machine", json=dict(name="printer", power=10, type="chill", site=site.get("site").get("id")))
        assert response.status_code == 400

    def test_nominal_scenario(self):
        # Create site
        response = self.client.post("/site", json=dict(name="paris-test", power=100))
        assert response.status_code == 201
        site = json.loads(response.data.decode())
        # Create machine
        response = self.client.post("/machine", json=dict(name="printer", power=10, type="chiller", site=site.get("site").get("id")))
        assert response.status_code == 201
        machine = json.loads(response.data.decode())
        assert machine == dict(machine=dict(id=ANY, name="printer", site="paris-test", power=10, type="chiller")), machine
        # List all machines
        response = self.client.get("/machine")
        assert response.status_code == 200
        machines = json.loads(response.data.decode())
        assert machines == dict(machines=[dict(id=ANY, name="printer", site="paris-test", power=10, type="chiller")]), machines
        # Get machine
        response = self.client.get(f"/machine/{machine.get('machine').get('id')}")
        assert response.status_code == 200
        assert json.loads(response.data.decode()) == dict(machine=dict(id=ANY, name="printer", site="paris-test", power=10, type="chiller"))
        # Update machine
        response = self.client.put(f"/machine/{machine.get('machine').get('id')}", json=dict(power=11, name="radio"))
        assert response.status_code == 200
        machine = json.loads(response.data.decode())
        assert machine == dict(machine=dict(id=ANY, name="radio", site="paris-test", power=11, type="chiller"))
        response = self.client.put(f"/machine/{machine.get('machine').get('id')}", json=dict(type="compressor"))
        assert response.status_code == 200
        machine = json.loads(response.data.decode())
        assert machine == dict(machine=dict(id=ANY, name="radio", site="paris-test", power=11, type="chiller")), machine
        response = self.client.put(f"/machine/{machine.get('machine').get('id')}", json=dict(type="compress"))
        assert response.status_code == 200
        # Create existing machine
        response = self.client.post("/machine", json=dict(name="radio", power=11, type="chiller", site=site.get("site").get("id")))
        machine = json.loads(response.data.decode())
        assert machine == dict(machine=dict(id=ANY, name="radio", site="paris-test", power=11, type="chiller"))
        # Delete machine
        response = self.client.delete(f"/machine/{machine.get('machine').get('id')}")
        assert response.status_code == 204
        # List all machines
        response = self.client.get("/machine")
        assert response.status_code == 200
        assert json.loads(response.data.decode()) == dict(machines=[])
        # Get machine
        response = self.client.get(f"/machine/{machine.get('machine').get('id')}")
        assert response.status_code == 404
        # Create machine
        response = self.client.post("/machine", json=dict(name="printer", power=10, type="chiller", site=site.get("site").get("id")))
        machine = json.loads(response.data.decode())
        self.client.delete(f"/site/{site.get('site').get('id')}")
        response = self.client.get(f"/machine/{machine.get('machine').get('id')}")
        assert response.status_code == 404
