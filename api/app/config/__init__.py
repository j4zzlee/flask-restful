__author__ = 'gia'


def add_configs(application):
    application.config.from_object('config.default')
    application.config.from_object('config.production')

    try:
        # only get configs from local if exists
        application.config.from_object('config.local')
    except ImportError:
        pass

    return application
