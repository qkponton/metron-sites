import os
from typing import Iterable, Union

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from werkzeug.exceptions import NotFound

from metron_sites.core.exception import DbError, DbOperationalError
from metron_sites.core.singleton import Singleton


class DbController(metaclass=Singleton):

    database = SQLAlchemy()

    @staticmethod
    def _commit() -> None:
        """
        secure commit to rollback in case of db issue
        :return: None
        :raise: DbError, DbOperationalError
        """
        try:
            DbController.database.session.commit()
        except OperationalError as error:
            raise DbOperationalError("Internal DB Operational Error", details=f"{error}") from error
        except SQLAlchemyError as error:
            DbController.database.session.rollback()
            raise DbError("Internal DB Error", details=f"{error}") from error

    @staticmethod
    def create_table(app):
        """
        creates DB tables
        :param app:
        :return:
        """
        with app.app_context():
            DbController.database.create_all()

    @staticmethod
    def delete(table, resource_id) -> None:
        """
        Generic delete resource. No exception returned in case of NotFound
        :param table:
        :param resource_id:
        :return: None
        """
        try:
            resource = DbController.get(table, resource_id)
        except NotFound:
            return
        DbController.database.session.delete(resource)
        DbController._commit()

    @staticmethod
    def get(table, resource_id):
        """
        Generic get resource by its id
        :param table:
        :param resource_id:
        :return: model resource
        """
        return DbController.database.get_or_404(table, resource_id)

    @staticmethod
    def get_by(table, **filters):
        """
        Get resource by filters
        :param table:
        :param filters:
        :return:
        """
        return DbController.database.one_or_404(getattr(table, "query").filter_by(**filters))

    @staticmethod
    def insert(resources: Union[Iterable, str]):
        """
        Generic insert resource
        :param resources:
        :return:
        """
        method = 'add_all' if isinstance(resources, Iterable) and not isinstance(resources, str) else 'add'
        getattr(DbController.database.session, method)(resources)
        DbController._commit()

    @staticmethod
    def list(table):
        """
        Generic list resources of table
        :param table:
        :return:
        """
        return DbController.database.session.execute(DbController.database.select(table)).scalars()

    @staticmethod
    def set_attribute(resource, **attributes):
        """
        Set attributes on resource
        :param resource:
        :param attributes:
        :return:
        """
        for name, value in attributes.items():
            if value is not None:
                setattr(resource, name, value)

    @staticmethod
    def setup_app(app):
        """
        setup DB connexion settings
        :param app:
        :return:
        """
        uri = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PWD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
        app.config['SQLALCHEMY_DATABASE_URI'] = uri
        DbController.database.init_app(app)

    @staticmethod
    def update(table, resource_id, **attributes):
        """
        Generic update resource
        :param table:
        :param resource_id:
        :param attributes:
        :return:
        """
        resource = DbController.get(table, resource_id)
        DbController.set_attribute(resource, **attributes)
        DbController._commit()
        return resource
