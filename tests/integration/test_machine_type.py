from __future__ import absolute_import

import json

import pytest

from tests.integration.test_integration import TestIntegration


@pytest.mark.integration
class TestMachineType(TestIntegration):
    """MachineTypeController integration test stubs"""

    def test_list_allowed_machine_types(self):
        """Test case for get_user_by_name

        Get operands
        """
        response = self.client.open('/machine-types', method='GET')
        assert response.status_code == 200
        assert json.loads(response.data.decode()) == dict(machine_types=["chiller", "compressor", "furnace", "rolling mill"])
