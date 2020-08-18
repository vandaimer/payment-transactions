
class Healthcheck:

    @staticmethod
    def status(db):
        db.execute("SELECT 1")
        return {'status': 'OK'}
