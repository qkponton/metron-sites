import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID

from metron_sites.controllers.db_controller import DbController


class Machine(DbController.database.Model):
    __table_args__ = {"schema": "metron"}
    __tablename__ = "machine"
    machine_id = DbController.database.Column(UUID(as_uuid=True), primary_key=True,
                                              server_default=sqlalchemy.text("uuid_generate_v4()"), )
    machine_name = DbController.database.Column(DbController.database.String, unique=True, nullable=False, )
    machine_power = DbController.database.Column(DbController.database.Integer, unique=True, nullable=False, )
    site_id = DbController.database.Column(UUID(as_uuid=True), DbController.database.ForeignKey('metron.site.site_id'))
    machine_type_id = DbController.database.Column(UUID(as_uuid=True),
                                                   DbController.database.ForeignKey('metron.machine_type.machine_type_id'))

    def to_dict(self) -> dict:
        """
        cast model to dictionary
        :return:
        """
        return dict(id=self.machine_id, name=self.machine_name, power=self.machine_power, site=self.site.site_name,
                    type=self.machine_type.machine_type_name)
