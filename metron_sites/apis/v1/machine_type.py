from metron_sites.controllers.machine_type_controller import MachineTypeController


def list_machine_types():
    """
    lists allowed machine types
    :return:
    """
    return dict(machine_types=MachineTypeController.list())
