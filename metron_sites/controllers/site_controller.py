from typing import Any, Dict, List

from metron_sites.controllers.db_controller import DbController
from metron_sites.core.exception import BadRequestError, DbError, SiteQuotaError
from metron_sites.core.singleton import Singleton
from metron_sites.models.site import Site


class SiteController(metaclass=Singleton):

    @staticmethod
    def check_quota(site, power) -> None:
        """
        checks if site has enough quota for new power

        :param site:
        :param power:
        :return: None
        :raise: SiteQuotaError
        """
        consumed_power = sum(machine.machine_power for machine in site.machines)
        if site.site_power < consumed_power + power:
            raise SiteQuotaError(f"Quota exceed on site: {consumed_power + power - site.site_power + 1} additional needed")

    @staticmethod
    def create(name: str, power: int) -> Site:
        """"
        creates new site
        :param name:
        :param power:
        :return: site
        """
        site = Site(site_name=name, site_power=power)
        try:
            DbController.insert(site)
        except DbError:
            site = DbController.get_by(Site, site_name=name)
        return site

    @staticmethod
    def delete(site_id: str) -> None:
        """
        deletes site
        :param site_id:
        :return: None
        """
        DbController.delete(Site, site_id)

    @staticmethod
    def get(site_id: str) -> Site:
        """
        Get site
        :param site_id:
        :return: site
        """
        return DbController.get(Site, site_id)

    @staticmethod
    def list() -> List[Site]:
        """
        Lists existing sites
        :return:
        """
        return list(DbController.list(table=Site))

    @staticmethod
    def update(site_id: str, name: str = None, power: int = None) -> Site:
        """
        updates site
        :param site_id:
        :param name:
        :param power:
        :return:
        :raise: BadRequestError
        """
        attributes: Dict[str, Any] = {}
        if name is not None:
            attributes["site_name"] = name
        if power is not None:
            attributes["site_power"] = power
        try:
            return DbController.update(Site, site_id, **attributes)
        except DbError as error:
            raise BadRequestError("invalid data", details=f"{error}") from error
