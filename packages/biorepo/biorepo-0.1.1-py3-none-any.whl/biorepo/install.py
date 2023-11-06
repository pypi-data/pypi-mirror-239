import enum
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Union

from rich.progress import Progress, SpinnerColumn, TaskProgressColumn

from biorepo import ui
from biorepo.exception import BioReopException
from biorepo.shell import Shell
from biorepo.source import BaseSource


class RunStatus(enum.Enum):
    SUCCESS = 1
    FAIL = 2
    RUNNING = 3


class Run:
    def __init__(self, shell: Shell, source: BaseSource):
        self.status = RunStatus.RUNNING
        self.shell = shell
        self.source = source

    def install(self, progress: Progress):
        job = progress.add_task(
            f"Installing... [req]{self.source.name}[/]", text="", total=None
        )
        try:
            self.source.create_source()
            self.shell.execute()
            self.status = RunStatus.SUCCESS
            progress.live.console.print(
                f"  [success]{ui.Emoji.SUCC}[/] Install [req]{self.source.name}[/] successful"
            )
        except BioReopException as e:
            self.status = RunStatus.FAIL
            progress.live.console.print(
                f"  [error]{ui.Emoji.FAIL}[/] Install [primary]{self.source.name}[/] failed"
            )
            progress.live.console.print(f"    [error]{e.msg}[/]")
        finally:
            progress.update(job, visible=False)


class Install:
    def __init__(self, nthread: int = 4):
        self.runs: Dict[str, Run] = {}
        self.nthread = nthread

    def create_executor(self):
        return ThreadPoolExecutor(
            min(len(self.runs), self.nthread, multiprocessing.cpu_count())
        )

    def add_run(self, r: Union[Run, List[Run]]):
        if not isinstance(r, list):
            r = [r]
        for run in r:
            self.runs[run.source.name] = run

    def install(self):
        pool = self.create_executor()
        with ui.UI().make_progress(
            " ",
            SpinnerColumn(ui.SPINNER, speed=1, style="primary"),
            "{task.description}",
            "[info]{task.fields[text]}",
            TaskProgressColumn("[info]{task.percentage:>3.0f}%[/]"),
        ) as progress:
            live = progress.live
            live.console.print("")
            for name, run in self.runs.items():
                pool.submit(run.install, progress)
            pool.shutdown(wait=True)

        failed = [
            run for name, run in self.runs.items() if run.status == RunStatus.FAIL
        ]
        if not failed:
            live.console.print(f"{ui.Emoji.POPPER} All complete!")
