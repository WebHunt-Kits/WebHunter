import json
import subprocess
from typing import Callable, Dict, List, Optional

from celery.utils.log import get_task_logger

from core.common.utils import execute_cmd
from core.cookcelery.app import application

logger = get_task_logger("cookcelery.tasks")


@application.task(bind=True)
def webhunt_scan(self, url: str, user_agent: str, timeout_sec=60*5) -> Optional[List]:
    results = []
    cmd = ("./thirdparty/WebHunt/webhunt", "scan",
           "-u", url, "-a", "-U", user_agent)
    logger.info("Executing task id %s, webhunt cmd %s", self.request.id, cmd)
    try:
        execute_cmd(cmd, timeout_sec, results.append)
    except subprocess.TimeoutExpired as err:
        raise self.retry(exc=err, countdown=5, max_retries=3)
    for line in results:
        line = line.strip().strip("\n")
        if not line.startswith("[{"):
            continue
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            logger.info("webhunt data: %s json decodeError", line)
    return None
