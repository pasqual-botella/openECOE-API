#  Copyright (c) 2020 Miguel Hernandez University of Elche
#  This file is part of openECOE-API.
#
#       openECOE-API is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#
#       openECOE-API is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with openECOE-API.  If not, see <https://www.gnu.org/licenses/>.
import os

from flask import current_app
from sqlalchemy.sql import func

from app.jobs import rq
from app.model import db


class Job(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    complete = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, server_default=func.now())
    finished = db.Column(db.DateTime, nullable=True)
    file = db.Column(db.UnicodeText, nullable=True)

    def rq_job(self):
        try:
            _q = rq.get_queue()
            _rq_job = _q.fetch_job(self.id)
        except Exception:
            return None
        return _rq_job

    @property
    def progress(self):
        _job = self.rq_job()

        if _job is not None:
            _progress = _job.meta.get("progress", 0)
        else:
            _progress = 100

        return _progress

    def del_job_file(self):
        """Delete file attached if exist"""
        if self.file:
            try:
                os.remove(
                    os.path.join(
                        os.path.dirname(current_app.instance_path),
                        current_app.config.get("DEFAULT_ARCHIVE_ROUTE"),
                        self.file,
                    )
                )
            except Exception as e:
                current_app.logger.info(
                    "File %s attached to job not found. %s" % (self.file, str(e))
                )
