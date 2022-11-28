import logging

import connexion
from flask_testing import TestCase
from werkzeug.exceptions import default_exceptions

from metron_sites.controllers.db_controller import DbController
from metron_sites.controllers.machine_type_controller import MachineTypeController
from metron_sites.core.exception_handler import exception_handler
from metron_sites.encoder import JSONEncoder


class TestIntegration(TestCase):

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')

        app = connexion.App(__name__, specification_dir='../../metron_sites/swagger/')
        app.app.json_encoder = JSONEncoder
        app.add_api('swagger.yaml', pythonic_params=True)
        app.app.config['TESTING'] = True
        app.app.config['WTF_CSRF_ENABLED'] = False
        DbController.setup_app(app.app)

        DbController.database.init_app(app.app)
        for exception in default_exceptions:
            app.app.register_error_handler(exception, exception_handler)

        app.add_error_handler(Exception, exception_handler)
        self.my_app = app
        return app.app

    def setUp(self):
        DbController.database.create_all()
        MachineTypeController.setup_machine_types(self.my_app.app)
        # DbController.setup_app(self.app)

    def tearDown(self):

        DbController.database.session.remove()
        DbController.database.drop_all()
