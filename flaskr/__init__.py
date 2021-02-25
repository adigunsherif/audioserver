import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from .views import AudioFileCreate, AudioFileList, AudioFileDetail
    
    app.add_url_rule('/', view_func=AudioFileCreate.as_view('audio_file_create'))
    app.add_url_rule('/<string:filetype>/', view_func=AudioFileList.as_view('audio_file_list'))
    app.add_url_rule('/<string:filetype>/<int:fid>', view_func=AudioFileDetail.as_view('audio_file_detail'))

    return app
    