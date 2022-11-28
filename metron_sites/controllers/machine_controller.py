from typing import List

from werkzeug.exceptions import NotFound

from metron_sites.controllers.db_controller import DbController
from metron_sites.controllers.machine_type_controller import MachineTypeController
from metron_sites.controllers.site_controller import SiteController
from metron_sites.core.exception import BadRequestError, DbError
from metron_sites.models.machine import Machine


class MachineController:

    @staticmethod
    def create(name: str, power: int, machine_type_name: str, site_id: str) -> Machine:
        """
        creates machine
        :param name:
        :param power:
        :param machine_type_name:
        :param site_id:
        :return: machine
        :raise: BadRequestError
        """
        try:
            machine_type = MachineTypeController.get_by(machine_type_name)
            site = SiteController.get(site_id)
        except NotFound as error:
            raise BadRequestError(str(error)) from error
        SiteController.check_quota(site, power)
        machine = Machine(machine_name=name, machine_power=power, machine_type_id=machine_type.machine_type_id,
                          site_id=site_id)
        try:
            DbController.insert(machine)
        except DbError:
            machine = DbController.get_by(Machine, machine_name=name, site_id=site_id,
                                          machine_type_id=machine_type.machine_type_id)
        return machine

    @staticmethod
    def delete(machine_id: str) -> None:
        """
        delete machine
        :param machine_id:
        :return: None
        """
        DbController.delete(Machine, machine_id)

    @staticmethod
    def get(machine_id: str) -> Machine:
        """
        Gets machine
        :param machine_id:
        :return: Machine
        """
        return DbController.get(Machine, machine_id)

    @staticmethod
    def list() -> List[Machine]:
        """
        lists existing machines
        :return:
        """
        return list(DbController.list(table=Machine))

    @staticmethod
    def update(machine_id: str, name: str = None, power: int = None) -> Machine:
        """
        updates machine
        :param machine_id:
        :param name:
        :param power:
        :return: Machine
        :raise: BadRequestError
        """
        attributes = {}
        if name is not None:
            attributes["machine_name"] = name
        if power is not None:
            attributes["machine_power"] = power
        try:
            return DbController.update(Machine, machine_id, **attributes)
        except DbError as error:
            raise BadRequestError("invalid data", details=f"{error}") from error
