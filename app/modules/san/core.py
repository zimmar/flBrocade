from app.model import Switch


class San(object):

    def __init__(self):
        self._service = None

    def init_app(self, app, db):
        self.app = app
        self.db = db

    def get_id(self):
        raise NotImplementedError

    def _create_service(self):
        raise NotImplementedError

    def get_service(self):
        if not self._service:
            self._service = self._create_service()
        return self._service


class SanSwitch(San):

    def __init__(self):
        super(San, self).__init__()
        self.appname = "psSan"
        self.switch = None
        self.conn = None

    def connect(self, name):
        if self.switch is not None:
            self.switch.close()

        self.switch = self.db.session.query(Switch).filter_by(Switch.name == name).first()

        try:
            self.conn.connect(self.switch.ip,
                              username=self.switch.username,
                              password=self.switch.password,
                              timeout=60)
        except Exception as e:
            self.conn = -1

        return self.conn

    def execute(self, cmd):
        stdin, stdout, stderr = self.conn.exec_command(cmd)
        error = stderr.read()
        result = stdout.readlines()

        if error:
            error = error.decode("US-ASCII")
            print("Error %s" % error)
            result =- 1

        return result
