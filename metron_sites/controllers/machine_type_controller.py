from typing import List

from metron_sites.controllers.db_controller import DbController
from metron_sites.core.exception import DbError
from metron_sites.core.logger import ApiLogger
from metron_sites.core.singleton import Singleton
from metron_sites.models.machine_type import MachineType
from metron_sites.settings import ApiSettings


class MachineTypeController(metaclass=Singleton):

    @staticmethod
    def get_by(name) -> MachineType:
        """
        Get machine type by its name
        :param name:
        :return:
        """
        return DbController.get_by(MachineType, machine_type_name=name)

    @staticmethod
    def list() -> List[str]:
        """
        list existing machine types
        :return:
        """
        return [machine_type.machine_type_name for machine_type in DbController.list(table=MachineType)]

    @staticmethod
    def setup_machine_types(app):
        """
        Ensure default machine types are in DB
        :param app:
        :return:
        """
        with app.app_context():
            for machine_type in ApiSettings.default_machine_types:
                try:
                    DbController.insert(MachineType(machine_type_name=machine_type))
                except DbError as error:
                    ApiLogger().get_logger().warning(error)
