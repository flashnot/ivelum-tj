import time
import random
from datetime import datetime
from django.utils import timezone

from task.models import *


def do_somethings(task_id):
    tr = TaskResult.objects.get(pk=task_id)
    if tr:
        rnd = random.randint(0, 60)
        time.sleep(rnd)

        tr.resulted_at = datetime.utcnow().replace(tzinfo=timezone.get_current_timezone())
        tr.status = TASK_STATUS_SUCCESS
        tr.result = 'sleep ' + str(rnd) + ' sec. for dummy input param = ' + tr.input_param
        tr.save()
    return tr.result
