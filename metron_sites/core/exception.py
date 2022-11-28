class SiteError(Exception):
    """
    Application-specific exception class
    """
    status_code = 400

    def __init__(self, message, details=None, status_code=None, payload=None):
        """
        """
        Exception.__init__(self)
        self.message = message
        self.details = details
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload


class BadRequestError(SiteError):
    status_code = 400


class ConflictError(SiteError):
    status_code = 409


class ForbiddenError(SiteError):
    status_code = 403


class NotFoundError(SiteError):
    status_code = 404


class InternalError(SiteError):
    status_code = 500


class DbOperationalError(SiteError):
    status_code = 500


class DbError(SiteError):
    status_code = 500


class SiteQuotaError(SiteError):
    status_code = 400
