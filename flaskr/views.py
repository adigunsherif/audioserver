from flask import make_response, jsonify, abort, request
from flask.views import MethodView
from flaskr.db import get_db


def table_exists(db, filetype):
    """ Helper function to check if table exists. """
    filetype_exists = db.execute(
        "SELECT name FROM sqlite_master WHERE type IN ('table','view') AND name = ? UNION ALL SELECT name FROM sqlite_temp_master WHERE type IN ('table','view') ORDER BY 1", (filetype,)
    ).fetchall()
    
    if filetype_exists:
        return True
    abort(400, "Invalid table name")


def get_columns(db, filetype):
    """ Helper functions to get the columns in a table """
    return db.execute(
        "PRAGMA table_info({})".format(filetype)
    ).fetchall()


class AudioFileDetail(MethodView):
    """ Show a single item and allow update and delete """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = get_db()

    def get(self, filetype, fid):
        table_exists(self.db, filetype)
        query = self.db.execute(
            'SELECT * FROM {} WHERE id = ?'.format(filetype), (fid,)
        ).fetchone()
        if query is None:
            abort(400, 'Invalid request')
        elif query is not None:
            columns = get_columns(self.db, filetype)
            post = {column['name']: query[column['name']] for column in columns}
            return make_response(jsonify(post), 200)
        else:
            abort(500, 'Internal Server Error')
        

    def delete(self, filetype, fid):
        table_exists(self.db, filetype)
        query = self.db.execute(
            'SELECT * FROM {} WHERE id = ?'.format(filetype), (fid,)
        ).fetchone()
        if query is None:
            abort(400, 'Invalid request')
        elif query is not None:
            db = self.db
            db.execute('DELETE FROM {} WHERE id = ?'.format(filetype), (fid,))
            db.commit()
            return make_response(jsonify("Successfully Deleted"), 200)
        else:
            abort(500, 'Internal Server Error')


    def put(self, filetype, fid):
        table_exists(self.db, filetype)
        item = self.db.execute(
            'SELECT * FROM {} WHERE id = ?'.format(filetype), (fid,)
        ).fetchone()
        if item is None:
            abort(400, 'Invalid request')
        elif item is not None:
            db = self.db
            filetype = request.get_json(force=True).get('audioFileType')
            if not filetype:
                abort(400, 'audioFileType is required.')

            metadata = request.get_json(force=True).get('audioFileMetadata')
            if not metadata:
                abort(400, 'audioFileMetadata is required.')
                
            table_exists(db, filetype)
            columns = get_columns(db, filetype)

            data = ''
            
            for key, val in metadata.items():
                data += f"{key} = '{val}', "

            db.execute(
                'UPDATE {} SET {} WHERE id = ?'.format(filetype, data[:-2]), (fid,)
            )
            db.commit()
            return make_response("success", 200)
        else:
            abort(500, 'Internal Server Error')


class AudioFileList(MethodView):
    """ Show list and allow creating a new audio file """
    def get(self, filetype):
        db = get_db()
        table_exists(db, filetype)
        query = db.execute(
            'SELECT * FROM {}'.format(filetype)
        ).fetchall()
        columns = get_columns(db, filetype)
        
        posts = []
        for row in query:
            post = {column['name']: row[column['name']] for column in columns}
            posts.append(post)
        return make_response(jsonify(posts), 200)


class AudioFileCreate(MethodView):
    def post(self):
        db = get_db()
        filetype = request.get_json(force=True).get('audioFileType')
        if not filetype:
            abort(400, 'audioFileType is required.')

        metadata = request.get_json(force=True).get('audioFileMetadata')
        if not metadata:
            abort(400, 'audioFileMetadata is required.')
            
        table_exists(db, filetype)
        columns = get_columns(db, filetype)

        meta_keys = [key for key in metadata.keys()]
        column_keys = [column['name'] for column in columns]
        meta_keys.sort()
        column_keys.sort()
        
        if meta_keys == column_keys:
            meta_values = [metadata[key] for key in meta_keys]
            cols = tuple(column_keys)
            vals = tuple(meta_values)
            db.execute(
                'INSERT INTO {} {} VALUES {}'.format(filetype, cols, vals),
            )
            db.commit()
            return make_response("success", 200)
        else:
            abort(400, "Incomplete Metadata")

        
        
        

