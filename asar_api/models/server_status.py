from ..extensions import db


class ServerStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # train
    training_status = db.Column(db.Boolean, nullable=False)  # True: runing / False: idle
    training_result = db.Column(db.Integer, nullable=False)  # -1: unknown / 0: fail / 1: success
    training_message = db.Column(db.String, nullable=True)
    training_project = db.Column(db.String, nullable=True)
    training_time = db.Column(db.DateTime, nullable=True)
    # load
    loaded_status = db.Column(db.Boolean, nullable=False)  # True: runing / False: idle
    loaded_result = db.Column(db.Integer, nullable=False)  # -1: unknown / 0: fail / 1: success
    loaded_message = db.Column(db.String, nullable=True)
    loaded_project = db.Column(db.String, nullable=True)
    loaded_time = db.Column(db.DateTime, nullable=True)

    @classmethod
    def init(cls):
        if ServerStatus.query.first() is None:
            status = ServerStatus(training_status=False,
                                  training_result=-1,
                                  loaded_status=False,
                                  loaded_result=-1)
            db.session.add(status)
            db.session.commit()
        else:
            status = ServerStatus.query.first()
            status.training_status = False
            status.loaded_status = False
            db.session.commit()
