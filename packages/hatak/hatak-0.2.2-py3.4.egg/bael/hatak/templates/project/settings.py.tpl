def make_settings(settings, paths):
    settings['jinja2.directories'] = '{{settings["package:name"]}}:templates'
    settings['debug'] = False
    settings['authentication_debug'] = False
    settings['session.type'] = 'file'
    settings['session.key'] = 'needtochangethis'
    settings['session.secret'] = 'needtochangethistoo'
    settings['session.cookie_on_exception'] = True

    paths['session.data_dir'] = ["%(data)s", 'sessions', 'data']
    paths['session.lock_dir'] = ["%(data)s", 'sessions', 'lock']

    paths['data'] = 'data'
    paths['frontend'] = ['%(data)s', 'frontend.ini']
    paths['logging:config'] = '%(frontend)s'
    paths['tests_yaml'] = ['%(project_path)s', 'tests', 'cases.yml']
    # ----------------------------------------
    # This is example postgresql configuration
    # ----------------------------------------
    # settings['db:url'] = (
    #     '%(db:type)s://%(db:login)s:%(db:password)s@%(db:host)s:%(db:port)s'
    #     '/%(db:db)s')
    # settings['db:type'] = 'postgresql'
    # settings['db:login'] = 'develop'
    # settings['db:password'] = 'develop'
    # settings['db:host'] = 'localhost'
    # settings['db:port'] = '5432'
    # settings['db:db'] = '{{settings["package:name"]}}_develop'
    paths['sqlite_db'] = ["%(data)s", 'database.db']
    settings['db:url'] = 'sqlite:///%(sqlite_db)s' % paths

    paths['alembic:versions'] = 'alembic'
    paths['alembic:ini'] = ['%(data)s', 'alembic.ini']
