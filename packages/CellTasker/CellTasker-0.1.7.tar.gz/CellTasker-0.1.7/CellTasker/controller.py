from pathlib import Path
import yaml
from time import sleep
from datetime import datetime, timedelta
from sys import argv
from .pub import TimeRange
import subprocess
import logging

root_path = Path(argv[0]).parent
config_path = (root_path / 'controll_config.yml')
with open(config_path, encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    register_path = Path(config['register_path'])

log = logging.getLogger('CellTasker')
log.addHandler(logging.StreamHandler())


class Controller:
    def __init__(self, interval) -> None:
        self.interval = interval
        self.cell_configs = dict()
        self.time_task = dict()
        self.booting_time = dict()
        self.booting_times = dict()
        self.max_booting_times = 3

    @classmethod
    def check_cell_config(cls, cell_config):
        properties = ['name', 'timerange', 'interval', 'register_path', 'update_path', 'boot_cmd']
        for property in properties:
            if property not in cell_config:
                return False
        return True

    def collect_cells(self):
        for cell in register_path.iterdir():
            if cell.is_file():
                with open(cell, encoding='utf-8') as f:
                    cell_config = yaml.load(f, Loader=yaml.FullLoader)
                    if self.check_cell_config(cell_config):
                        self.cell_configs[cell_config['name']] = cell_config
                    else:
                        log.error(f'Invalid cell config file: {cell}, {cell_config}')
        log.info(f'registered {self.cell_configs}')

    def add_hook(self):
        for name, cell in self.cell_configs.items():
            timerange: TimeRange = cell['timerange']
            self.time_task.setdefault(timerange, []).append(name)

    def is_cell_running(self, name):
        cell_config = self.cell_configs[name]
        update_file = Path(cell_config['update_path']) / f'{name}.yml'
        if not update_file.exists() or not update_file.is_file():
            return False
        with open(update_file, encoding='utf-8') as f:
            updated_info = yaml.load(f, Loader=yaml.FullLoader)
            if 'timestamp' not in updated_info:
                return False
            updated_time = datetime.strptime(updated_info['timestamp'], '%Y-%m-%d %H:%M:%S')
            now = datetime.now()
            if now - updated_time > timedelta(seconds=cell_config['interval']):
                return False
        self.booting_time.pop(name, None)
        return True

    def start_cell(self, name):
        self.booting_times.setdefault(name, 0)
        if self.booting_times[name] > self.max_booting_times:
            log.debug(f'{name} has been booting {self.max_booting_times} times, skip')
            return

        cell_config = self.cell_configs[name]
        if name in self.booting_time \
                and datetime.now() - self.booting_time[name] < timedelta(seconds=3*cell_config['interval']):
            log.debug(f'{name} is booting, skip')
            return
        if self.is_cell_running(name):
            log.debug(f'{name} is running, skip')
            return
        boot_cmd = cell_config['boot_cmd']
        log.info(f'starting {name} with {boot_cmd}')
        subprocess.Popen(boot_cmd, shell=True)
        self.booting_times[name] += 1
        self.booting_time[name] = datetime.now()

    def run(self):
        while True:
            for timerange, names in self.time_task.items():
                timerange = TimeRange.from_str(timerange)
                if datetime.now() in timerange:
                    for name in names:
                        self.start_cell(name)
            sleep(self.interval)
