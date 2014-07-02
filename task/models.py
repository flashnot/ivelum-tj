from django.db import models
from django.conf import settings

WORKER_LEVEL_HIGH = 'h'
WORKER_LEVEL_NORMAL = 'd'
WORKER_LEVEL_LOW = 'l'
WORKER_LEVEL_CHOICES = {
    WORKER_LEVEL_HIGH: 'High',
    WORKER_LEVEL_NORMAL: 'Default',
    WORKER_LEVEL_LOW: 'Low',
}


class Worker(models.Model):
    """
    Worker parameters model
    """
    host = models.CharField(max_length=15, blank=False, default='127.0.0.1')
    port = models.CharField(max_length=5, blank=False, default='6379')
    level = models.CharField(max_length=1, blank=False, choices=WORKER_LEVEL_CHOICES.items())

    def __unicode__(self):
        return "{0}:{1} - {2}".format(self.host, self.port, WORKER_LEVEL_CHOICES[self.level])

TASK_STATUS_WAIT = 'w'
TASK_STATUS_SUCCESS = 's'
TASK_STATUS_ERROR = 'e'
TASK_STATUS_CHOICES = {
    TASK_STATUS_WAIT: 'Wait',
    TASK_STATUS_SUCCESS: 'Success',
    TASK_STATUS_ERROR: 'Error',
}


class TaskResult(models.Model):
    """
    Model for store worker job result
    """
    status = models.CharField(max_length=1, blank=False, choices=TASK_STATUS_CHOICES.items(), default=TASK_STATUS_WAIT)
    input_param = models.TextField()
    result = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='task_results')
    created_at = models.DateTimeField(auto_now_add=True)
    resulted_at = models.DateTimeField(blank=True, null=True)
    worker = models.ForeignKey(Worker, related_name='task_results_w')
    job = models.CharField(max_length=128, blank=True, null=True)