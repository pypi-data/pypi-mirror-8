# -*- coding: utf-8 -*-
import logging

from pyramid.config import Configurator

log = logging.getLogger(__name__)


def includeme(config):
    log.debug('Including pyramid_restlogging')

    config.add_route(
        'clientlogs',
        '/clientlogs/{logger_name:[\d\w\.:]+}/'
        '{log_level:debug|info|warning|error|critical}',
        request_method='POST',
        )
    config.add_route(
        'clientlogs_batch',
        '/clientlogs/batch',
        request_method='POST',
        )
    # added a new route so that flash-logging clients can use
    # the same URL endpoint for both simple and batch logs
    config.add_route(
        'clientlogs_batch_flexible',
        '/clientlogs/',
        request_method='POST',
        )
    config.scan('pyramid_restlogging.views')
    config.commit()


def main(global_config, **settings):
    # global_config is not used here,  see Paste doc
    config = Configurator(settings=settings)
    config.include(includeme)
    return config.make_wsgi_app()
