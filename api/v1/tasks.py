import enum
from flask import request
from flask_mico import ApiView, validator
from flask_mico.conf import settings
from flask_mico.error import AppError
from celery.result import AsyncResult
from redis import Redis

from core.errors import APIErrorStausCode
from core.field_schema import TASKS_GET_SCHEMA
from core.cookcelery.tasks import webhunt_scan
from core.common.redis_pool import get_redis_connection
from core.common.utils import plain2md5, is_url


class TaskStatus(enum.Enum):
    succ = "success"
    fail = "failed"
    running = "running"


def gen_tmp_taskid(target: str) -> str:
    return "#%s" % plain2md5(target)


def process_target(target: str) -> str:
    return target.strip().strip("/")


def excluded_domain(url: str) -> bool:
    i_domains = ("gov.cn", "baidu.com", "qq.com", "aliyun.com", "alipay.com")
    for i in i_domains:
        if i in url:
            return True
    return False


class Tasks(ApiView):

    @validator(TASKS_GET_SCHEMA, in_params=True)
    def get(self):
        isnotfound = False
        target = process_target(request.args.get("target"))
        retry = bool(request.args.get("retry", None))
        if not is_url(target):
            raise AppError(APIErrorStausCode.NOT_URL)
        try:
            r = get_redis_connection(
                settings.CeleryConfig.CELERY_RESULT_BACKEND)
            taskid = r.get(gen_tmp_taskid(target))
        except:
            raise AppError(APIErrorStausCode.DATABASE_ERR)
        # create scan task
        if not taskid:
            isnotfound = True
            taskid = self.create_task(target, r)

        task_r = AsyncResult(taskid)
        # retry task
        if task_r.successful() and (retry and not isnotfound):
            task_r = self.retry_task(target, r)
        # return task info
        if task_r.failed():
            # 清除 失败/撤销 的任务
            task_r.forget()
            return self.on_success(data={"status": TaskStatus.fail.value})
        if task_r.successful():
            return self.on_success(data={"status": TaskStatus.succ.value,
                                         "result": task_r.result,
                                         "done_at": task_r.date_done})
        return self.on_success(data={"status": TaskStatus.running.value})

    @staticmethod
    def create_task(target: str, r: Redis) -> str:
        if excluded_domain(target):
            raise AppError(APIErrorStausCode.EXCLUDED_DOMAIN)
        t = webhunt_scan.delay(target, request.user_agent.string)
        try:
            r.set(gen_tmp_taskid(target), t.id,
                  ex=settings.CeleryConfig.CELERY_TASK_RESULT_EXPIRES)
        except:
            raise AppError(APIErrorStausCode.DATABASE_ERR)
        return t.id

    @staticmethod
    def retry_task(target: str, r: Redis) -> AsyncResult:
        try:
            r.delete(gen_tmp_taskid(target))
        except:
            raise AppError(APIErrorStausCode.DATABASE_ERR)
        taskid = Tasks.create_task(target, r)
        return AsyncResult(taskid)
