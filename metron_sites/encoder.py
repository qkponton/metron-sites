import six
from connexion.apps.flask_app import FlaskJSONEncoder
from sqlalchemy.ext.declarative import DeclarativeMeta

from metron_sites.controllers.db_controller import DbController


class JSONEncoder(FlaskJSONEncoder):
    include_nulls = False

    def default(self, o):
        """

        :param o: object to jsonify
        :return:
        """
        if isinstance(o.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            return o.to_dict()
        if isinstance(o, DbController.database.Model):
            dikt = {}
            for attr, _ in six.iteritems(o.swagger_types):
                value = getattr(o, attr)
                if value is None and not self.include_nulls:
                    continue
                attr = o.attribute_map[attr]
                dikt[attr] = value
            return dikt
        return FlaskJSONEncoder.default(self, o)
