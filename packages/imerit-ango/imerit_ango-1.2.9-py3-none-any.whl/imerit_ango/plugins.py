import os
import time
import boto3
import queue
import logging
import datetime
import requests
import socketio
from io import BytesIO
from typing import Callable, Tuple
from apscheduler.schedulers.background import BackgroundScheduler

from imerit_ango.plugin_logger import PluginLogger
from imerit_ango.sdk import SDK

try:
    import asyncio
except ImportError:
    import trollius as asyncio

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)


class Plugin(socketio.ClientNamespace):

    def __init__(self, id: str, secret: str, callback: Callable):
        super().__init__('/plugin')
        self.id = id
        self.secret = secret
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.heartbeat, 'interval', seconds=60)
        self.scheduler.start()
        self.logger = logging.getLogger("plugin")
        self.logger.setLevel(LOGLEVEL)
        self.callback = callback
        self.loop = asyncio.get_event_loop()

    def on_connect(self):
        self.heartbeat()
        self.logger.warning("Connected")

    def on_disconnect(self):
        self.logger.warning("Disconnected")
        _connect(self, self.client.connection_url)

    def heartbeat(self):
        try:
            self.emit('heartbeat', {"id": self.id, "secret": self.secret})
        except Exception as e:
            self.logger.critical(e)
            os._exit(1)
        self.logger.info("Heartbeat at %s" % str(time.time()))

    def on_plugin(self, data):
        data["logger"] = self._get_logger(data)
        data["batches"] = data.get('tags', [])
        response = {
            "response": self.callback(**data),
            "session": data.get("session", "")
        }
        self.emit('response', response)

    def _get_logger(self, data):
        org_id = data.get("orgId", "")
        run_by = data.get("runBy", "")
        session = data.get("session", "")
        logger = PluginLogger("logger", self.id, org_id, run_by, session, self)
        return logger

    def start(self):
        asyncio.get_event_loop().run_forever()


class ExportResponse:
    def __init__(self, file: BytesIO, file_name: str = "export.json", storage_id: str = None, bucket: str = None):
        self.file = file
        self.file_name = file_name
        self.storage_id = storage_id
        self.bucket = bucket


class ExportPlugin(Plugin):

    def __init__(self, id: str, secret: str, callback: Callable[[str, dict], Tuple[str, BytesIO]],
                 host="https://imeritapi.ango.ai", version: str = "v2"):
        super().__init__(id, secret, callback)
        self.host = host
        self.version = version

    def on_plugin(self, data):
        """
        :param data: {project_id: str, assignees: List[str] = None, completed_at: List[datetime.datetime] = None,
               updated_at: List[datetime.datetime = None, tags: List[str] = None}
        :return:
        """
        completed_at = None
        updated_at = None
        project_id = data.get('projectId')
        logger = super()._get_logger(data)
        api_key = data.get('apiKey')
        sdk = SDK(api_key=api_key, host=self.host)

        if data.get("completed_at", None):
            completed_at = [datetime.datetime.fromisoformat(data.completed_at[0]),
                            datetime.datetime.fromisoformat(data.completed_at[1])]
        if data.get("updated_at", None):
            updated_at = [datetime.datetime.fromisoformat(data.updated_at[0]),
                          datetime.datetime.fromisoformat(data.updated_at[1])]

        try:
            (json_export, num_lines) = sdk.exportV3(project_id, batches=data.get('batches', None),
                                                    stage=data.get('stage', None), export_format="ndjson")
            data["numTasks"] = num_lines
        except Exception as e:
            logger.error(f"Error calling sdk.export: {e}")
            return

        data["jsonExport"] = json_export
        data["logger"] = logger

        resp = self.callback(**data)

        if resp.storage_id:
            storage = sdk.get_storages(resp.storage_id)
            s3 = boto3.client('s3', region_name=storage.get('region'), aws_access_key_id=storage.get("publicKey"),
                              aws_secret_access_key=storage.get("privateKey"))
            signed_url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': resp.bucket, 'Key': resp.file_name},
                ExpiresIn=3600
            )
            upload_url = s3.generate_presigned_url(
                'put_object',
                Params={'Bucket': resp.bucket, 'Key': resp.file_name},
                ExpiresIn=3600
            )
        else:
            file_name = project_id + '/exports/' + resp.file_name
            upload_url = sdk._get_upload_url(file_name)
            signed_url = sdk._get_signed_url(upload_url)

        try:
            upload_resp = requests.put(upload_url, data=resp.file.getvalue())
            upload_resp.raise_for_status()
        except requests.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            logger.error(f"Other error occurred: {err}")
        else:
            response = {
                "export": True,
                "response": signed_url,
                "session": data.get("session", "")
            }
            self.emit('response', response)


class ModelPlugin(Plugin):
    def __init__(self, id: str, secret: str, callback: Callable, host="https://imeritapi.ango.ai", concurrency=1):
        super().__init__(id, secret, callback)
        self.host = host
        self.concurrency = concurrency
        self.queue = queue.Queue()

    async def work(self):
        while True:
            data = self.queue.get()
            data["batches"] = data.get('tags', [])
            api_key = data.get('apiKey')
            task_id = data.get('taskId')
            sdk = SDK(api_key=api_key, host=self.host)
            answer = self.callback(**data)
            sdk._annotate(task_id, answer)

    def on_plugin(self, data):
        workflow = data.get('workflow')
        if not workflow:
            return super().on_plugin(data)
        self.queue.put(data)

    def start(self):
        tasks = [self.work() for i in range(self.concurrency)]
        future = asyncio.gather(*tasks)
        self.loop.run_until_complete(future)


class FileExplorerPlugin(Plugin):
    def __init__(self, id: str, secret: str, callback: Callable):
        super().__init__(id, secret, callback)


class BatchModelPlugin(Plugin):
    def __init__(self, id: str, secret: str, callback: Callable):
        super().__init__(id, secret, callback)


class InputPlugin(Plugin):
    def __init__(self, id: str, secret: str, callback: Callable):
        super().__init__(id, secret, callback)


class MarkdownPlugin(Plugin):
    def __init__(self, id: str, secret: str, callback: Callable):
        super().__init__(id, secret, callback)


def _connect(plugin, host):
    try:
        sio = socketio.Client(logger=logging.getLogger("plugin"), reconnection=False)
        sio.register_namespace(plugin)
        sio.connect(host, namespaces=["/plugin"], transports=["websocket"], wait=True)
    except Exception as e:
        logging.getLogger().critical(e)
        os._exit(1)


def run(plugin, host="https://plugin.imerit.ango.ai"):
    _connect(plugin, host)
    try:
        plugin.start()
    except (KeyboardInterrupt, SystemExit):
        logging.getLogger().warning("Plugin Stopped")
        os._exit(1)
