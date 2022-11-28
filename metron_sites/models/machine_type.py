import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID

from metron_sites.controllers.db_controller import DbController


class MachineType(DbController.database.Model):
    __table_args__ = {"schema": "metron"}
    __tablename__ = "machine_type"
    machine_type_id = DbController.database.Column(UUID(as_uuid=True), primary_key=True,
                                                   server_default=sqlalchemy.text("uuid_generate_v4()"), )
    machine_type_name = DbController.database.Column(DbController.database.String, unique=True, nullable=False, )
    machines = DbController.database.relationship("Machine", backref="machine_type", cascade="all,delete")

    def to_dict(self) -> dict:
        """
        cast model to dictionary
        :return:
        """
        return dict(id=self.machine_type_id, name=self.machine_type_name)
