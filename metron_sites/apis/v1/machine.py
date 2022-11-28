from metron_sites.controllers.machine_controller import MachineController
from metron_sites.core.exception import BadRequestError


def create_machine(body: dict):
    """
    creates machine
    :param body:
    :return:
    """
    try:
        return dict(machine=MachineController.create(name=body["name"], power=body["power"], site_id=body["site"],
                                                     machine_type_name=body["type"])), 201
    except KeyError as error:
        raise BadRequestError(error) from error


def delete_machine(machine_id):
    """
    deleted machine
    :param machine_id:
    :return:
    """
    MachineController.delete(machine_id)
    return None, 204


def get_machine(machine_id):
    """
    shows machine
    :param machine_id:
    :return:
    """
    return dict(machine=MachineController.get(machine_id))


def list_machine():
    """
    lists machines
    :return:
    """
    return dict(machines=MachineController.list())


def update_machine(machine_id: str, body: dict):
    """
    updates machine
    :param machine_id:
    :param body:
    :return:
    """
    return dict(machine=MachineController.update(machine_id, name=body.get("name"), power=body.get("power")))
