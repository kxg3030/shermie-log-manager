import datetime
import os
import time
import traceback

import yaml
from rich import box
from rich.console import Console
from rich.progress import Progress
from rich.style import Style
from rich.table import Table

from LogWatch.Log import Log


class LogFileInfo(object):
    filepath: str = ""
    filesize: int = 0
    createdAt: str = ""

    def __init__(self, filepath: str, filesize: int, createdAt: str):
        self.filesize = filesize
        self.filepath = filepath
        self.createdAt = createdAt


class LogWatch(object):
    config: dict = None
    deadtime: int = 0
    console: Console = None

    def __init__(self):
        self.console = Console()

    """
    读取配置参数
    """

    def LoadOption(self):
        handle = open("./config.yaml", encoding="utf-8", mode="r")
        config = yaml.load(handle, Loader=yaml.FullLoader)
        handle.close()
        self.config = config

    """
    程序入口
    """

    def Run(self):
        self.LoadOption()
        # 循环处理每个项目的日志文件
        for key, app in enumerate(self.config["application"]):
            try:
                fileList: list = []
                self.ListFile(app["path"], fileList)
                if len(fileList) <= 0:
                    continue
                self.ShowTable(app["name"], fileList)
            except Exception as e:
                Log.Instance().logger.error("删除{0}日志失败：{1}".format(app["name"], e))
                Log.Instance().logger.error(traceback.format_exc())

    """
    获取日志过期时间
    """

    def DeadTime(self):
        duration = datetime.datetime.now() - datetime.timedelta(days=int(self.config["deadtime"]))
        return int(time.mktime(duration.timetuple()))

    """
    获取文件夹下所有的过期日志文件
    """

    def ListFile(self, filepath: str, allFileList: list):
        self.deadtime = self.DeadTime()
        fileList = os.listdir(filepath)
        for key, val in enumerate(fileList):
            fullpath = os.path.join(filepath, val)
            if os.path.isdir(fullpath):
                self.ListFile(fullpath, allFileList)
            if os.path.isfile(fullpath):
                extension = os.path.splitext(fullpath)[-1]
                if extension != self.config["extension"]:
                    continue
                stat = os.stat(fullpath)
                if stat.st_ctime < self.deadtime:
                    allFileList.append(
                            LogFileInfo(filepath=fullpath, filesize="{:.2f}KB".format(stat.st_size / 1024),
                                        createdAt=time.strftime("%Y-%m-%d %H:%M:%S",
                                                                time.localtime(int(stat.st_ctime)))
                                        )
                    )
        return allFileList

    """
    展示待处理文件的表格
    """

    def ShowTable(self, appName: str, fileList: list = None):
        table = Table(title=appName, box=box.SQUARE)
        table.add_column("文件大小", justify="center", style="cyan", no_wrap=True)
        table.add_column("文件名", style="cyan", justify="center")
        table.add_column("创建时间", justify="center", style="green")
        for _, file in enumerate(fileList):
            table.add_row(str(file.filesize), file.filepath, str(file.createdAt), style=Style())
        self.console.print(table)
        progress = Progress()
        with progress:
            for n in progress.track([f.filepath for k, f in enumerate(fileList)], description="进度", total=len(fileList)):
                os.remove(n)
                basedir = os.path.dirname(n)
                if len(os.listdir(basedir)) <= 0 :
                    os.remove(basedir)
                Log.Instance().logger.info("删除:{0}".format(n))
                time.sleep(0.1)
