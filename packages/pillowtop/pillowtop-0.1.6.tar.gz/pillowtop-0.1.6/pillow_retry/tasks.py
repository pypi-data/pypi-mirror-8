import json
from celery.task import task
import sys
from django.conf import settings
from dimagi.utils.couch.cache import cache_core
from pillow_retry.models import PillowError
from pillowtop.utils import import_pillow_string, get_pillow_by_name


@task
def process_pillow_retry(error_doc_id):
    # Redis error logged in get_redis_client
    try:
        client = cache_core.get_redis_client()
    except cache_core.RedisClientError:
        return

    # Prevent more than one task from processing this error, just in case
    # it got enqueued twice.
    lock = client.lock(
        "pillow-retry-processing-%s" % error_doc_id,
        timeout=settings.PILLOW_RETRY_PROCESSING_LOCK_TIMEOUT*60
    )

    if lock.acquire(blocking=False):
        try:
            error_doc = PillowError.objects.get(id=error_doc_id)
        except PillowError.DoesNotExist:
            return

        pillow_class = error_doc.pillow
        try:
            pillow = import_pillow_string(pillow_class)
        except ValueError:
            # all fluff pillows have module path of 'fluff' so can't be imported directly
            _, pillow_class_name = pillow_class.rsplit('.', 1)
            pillow = get_pillow_by_name(pillow_class_name)

        try:
            if not pillow:
                raise ValueError("Could not find pillowtop class '%s'" % pillow_class)
            change = error_doc.change_dict
            if pillow.include_docs:
                change['doc'] = pillow.couch_db.open_doc(change['id'])

            pillow.process_change(change, is_retry_attempt=True)
        except Exception:
            ex_type, ex_value, ex_tb = sys.exc_info()
            error_doc.add_attempt(ex_value, ex_tb)
            error_doc.save()
        else:
            error_doc.delete()
        finally:
            lock.release()





