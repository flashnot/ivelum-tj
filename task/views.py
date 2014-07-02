import random

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView

from rq import Connection, Queue
from rq.job import Job, Status
from redis import Redis

from task.models import *
from task.serializers import TaskResultSerializer
from task.worker import do_somethings

HTTP_422_UNPROCESSABLE_ENTITY = 422

def index(request):
    """
    Action for index page
    """
    return TemplateResponse(request, 'index.html', {'isAuth': request.user.is_authenticated()})


class TaskResultIndex(ListCreateAPIView):
    """
    List all users task, or create a new task.
    """
    queryset = None
    serializer_class = TaskResultSerializer

    def pre_save(self, obj):
        obj.user = self.request.user
        # use simple logic to choose worker for current task
        workers = self.request.user.worker.all()
        worker_index = random.randint(0, len(workers) - 1)
        obj.worker = workers[worker_index]

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = TaskResult.objects.filter(user=self.request.user)
        return self.queryset

    def post(self, request, format=None):
        if not request.user.worker.all():
            return Response(
                {'result': 'error', 'detail': 'not attracted any workers'},
                status=HTTP_422_UNPROCESSABLE_ENTITY
            )

        #redis_conn = Redis()

        # obtain and prepare input data from post request data:
        #data = request.DATA.dict()
        data = {}
        input_param = request.POST.getlist('input_param', '')
        if input_param:
            if type(input_param) == list:
                input_params = input_param
            else:
                input_params = [input_param]
            #data.pop('input_param', None)
        else:
            input_params = request.POST.getlist('input_param[]')
            #data.pop('input_param[]', None)

        # create tasks:
        errors = []
        task_ids = []
        if input_params:
            for i in xrange(len(input_params)):
                if not input_params[i]:
                    continue
                data['input_param'] = input_params[i]

                serializer = TaskResultSerializer(data=data)
                if serializer.is_valid():
                    self.pre_save(obj=serializer.object)
                    try:
                        serializer.save()
                        task_ids.append(serializer.data['id'])

                        # start job
                        try:
                            redis_conn = Redis(serializer.object.worker.host, serializer.object.worker.port)
                            q = Queue(WORKER_LEVEL_CHOICES[serializer.object.worker.level].lower(), connection=redis_conn)
                            job = q.enqueue(do_somethings, serializer.data['id'])
                            tr = TaskResult.objects.get(pk=serializer.data['id'])
                            tr.job = str(job.id)
                            tr.save()
                        except Exception, e:
                            tr = TaskResult.objects.get(pk=serializer.data['id'])
                            tr.status = TASK_STATUS_ERROR
                            tr.result = str(e)
                            tr.save()
                            errors.append(str(e))

                    except Exception, e:
                        errors.append(str(e))
                else:
                    errors.append(serializer.errors)

        # return result:
        if task_ids:
            if errors:
                ret = {'result': 'success_with_errors', 'details': errors}
            else:
                ret = {'result': 'success'}
            ret['task_ids'] = task_ids
            ret_status = status.HTTP_201_CREATED
        else:
            if not errors:
                errors.append('invalid input parametrs')
            ret = {'result': 'error', 'details': errors}
            ret_status = status.HTTP_400_BAD_REQUEST

        return Response(ret, status=ret_status)


class TaskResultDetail(APIView):
    """
    Information about task
    """
    scenario = 'full'

    def is_job_failed(self, task_result):
        job_is_failed = False

        try:
            redis_conn = Redis(task_result.worker.host, task_result.worker.port)
            job = Job.fetch(task_result.job, connection=redis_conn)
        except Exception, e:
            job_is_failed = True

        if not job_is_failed and job.is_failed:
            job_is_failed = True

        return job_is_failed


    def get(self, request, pk, format=None):
        try:
            tr = TaskResult.objects.get(pk=pk, user=request.user)
        except TaskResult.DoesNotExist:
            raise Http404

        # check job is failure
        if tr.status == TASK_STATUS_WAIT:
            if self.is_job_failed(tr):
                tr.status = TASK_STATUS_ERROR
                tr.save()

        serializer = TaskResultSerializer(tr)
        resp = serializer.data

        if self.scenario == 'status' or self.scenario == 'result':
            resp = {'id': resp['id'], 'status': resp['status'], 'result': resp['result']}

        resp['status'] = TASK_STATUS_CHOICES[resp['status']]

        return Response(resp)