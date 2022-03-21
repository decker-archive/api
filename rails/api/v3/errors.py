import json


class Error(Exception):
    status_code = 500

    def _to_json(self):
        return json.dumps({'message': f'{self.status_code}: {self.args[0]}', 'code': 0})

class Forbidden(Error):
    status_code = 403

class NotFound(Error):
    status_code = 404

class InvalidData(Error):
    status_code = 400

class Unauthorized(Error):
    status_code = 401
