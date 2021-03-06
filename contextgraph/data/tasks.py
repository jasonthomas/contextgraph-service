import json

from contextgraph.config import TESTING
from contextgraph.worker.app import celery_app
from contextgraph.worker.task import BaseTask


if TESTING:
    @celery_app.task(base=BaseTask, bind=True, queue='celery_default')
    def dummy(self):
        self.cache.incr('foo', 2)
        return int(self.cache.get('foo'))

    @celery_app.task(base=BaseTask, bind=True, queue='celery_default')
    def error(self):
        raise ValueError('fail')


@celery_app.task(base=BaseTask, bind=True, queue='celery_default')
def delete(self, user):
    key = ('user_%s' % user).encode('ascii')
    self.cache.delete(key)


@celery_app.task(base=BaseTask, bind=True, queue='celery_default')
def upload(self, user, data):
    key = ('user_%s' % user).encode('ascii')
    self.cache.set(key, json.dumps(data), ex=3600)
