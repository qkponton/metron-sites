from metron_sites.controllers.site_controller import SiteController
from metron_sites.core.exception import BadRequestError


def create_site(body: dict):
    """
    creates site
    :param body:
    :return:
    """
    try:
        return dict(site=SiteController.create(name=body["name"], power=body["power"])), 201
    except KeyError as error:
        raise BadRequestError(error) from error


def delete_site(site_id: str):
    """
    deletes site
    :param site_id:
    :return:
    """
    SiteController.delete(site_id)
    return None, 204


def get_site(site_id: str):
    """
    shows site
    :param site_id:
    :return:
    """
    return dict(site=SiteController.get(site_id))


def list_site():
    """
    lists sites
    :return:
    """
    return dict(sites=SiteController.list())


def update_site(site_id: str, body: dict):
    """
    update site
    :param site_id:
    :param body:
    :return:
    """
    return dict(site=SiteController.update(site_id, name=body.get("name"), power=body.get("power")))
