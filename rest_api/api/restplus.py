import logging
import traceback

from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound


log = logging.getLogger(__name__)

api = Api(version='1.0', title='Library API')

@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.error(message)
    return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.error(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404
