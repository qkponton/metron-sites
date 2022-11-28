import connexion
from flask import redirect
from werkzeug.exceptions import default_exceptions

from metron_sites import encoder
from metron_sites.controllers.db_controller import DbController
from metron_sites.controllers.machine_type_controller import MachineTypeController
from metron_sites.core.exception_handler import exception_handler
from metron_sites.settings import ApiSettings

SWAGGER_FILES = [dict(base_path='/api/v1', file='swagger.yaml')]


def main():
    """

    :return:
    """
    app = connexion.App(__name__, specification_dir='./swagger/', options=dict(swagger_url='documentation'))
    app.app.json_encoder = encoder.JSONEncoder
    setup_connexion_routes(app)
    setup_exception_handlers(app)
    setup_flask_routes(app.app)
    DbController.setup_app(app.app)
    DbController.create_table(app.app)
    MachineTypeController.setup_machine_types(app.app)
    app.run(port=8000)


def setup_connexion_routes(connexion_app: connexion.App):
    """
    setup connexion routes

    :param connexion_app:
    :return:
    """
    for swagger in SWAGGER_FILES:
        connexion_app.add_api(swagger.get('file'), base_path=swagger.get('base_path'), validate_responses=True,
                              arguments=dict(CONFIG=getattr(ApiSettings(), 'swagger_config',
                                                            dict(title='Metron Sites'))),
                              pythonic_params=True)


def setup_exception_handlers(connexion_app: connexion.App):
    """Initialize all exceptions handling."""
    for exception in default_exceptions:
        connexion_app.app.register_error_handler(exception, exception_handler)

    connexion_app.add_error_handler(Exception, exception_handler)


def setup_flask_routes(flask_app):
    """
    flask routes

    :param flask_app:
    :return:
    """
    @flask_app.route('/')
    @flask_app.route('/documentation')
    @flask_app.route('/documentation/')
    @flask_app.route('/v1/ui/')
    @flask_app.route('/api/v1/ui/')
    def documentation_root():
        return redirect(SWAGGER_FILES[0].get('base_path') + '/documentation/')


if __name__ == '__main__':
    main()
