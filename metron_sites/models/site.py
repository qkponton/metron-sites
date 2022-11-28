import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID

from metron_sites.controllers.db_controller import DbController


class Site(DbController.database.Model):
    __table_args__ = {"schema": "metron"}
    __tablename__ = "site"
    site_id = DbController.database.Column(UUID(as_uuid=True), primary_key=True,
                                           server_default=sqlalchemy.text("uuid_generate_v4()"), )
    site_name = DbController.database.Column(DbController.database.String, unique=True, nullable=False, )
    site_power = DbController.database.Column(DbController.database.Integer, unique=True, nullable=False, )
    machines = DbController.database.relationship("Machine", backref="site", cascade="all,delete")

    def to_dict(self) -> dict:
        """
        cast model to dictionary
        :return:
        """
        return dict(id=self.site_id, name=self.site_name, power=self.site_power)
