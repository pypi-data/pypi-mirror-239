from pathlib import Path
import yaml
from time import sleep
from datetime import datetime
from threading import Thread
from sys import argv
import logging

log = logging.getLogger('CellTasker')
log.addHandler(logging.StreamHandler())


root_path = Path(argv[0]).parent

config_path = (root_path / 'cell_config.yml')
with open(config_path, encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    register_path = Path(config['register_path'])
    update_path = Path(config['update_path'])
if 'boot_cmd' not in config or not config['boot_cmd']:
    log.info('No boot_cmd found, creating a default boot_cmd for you.')
    default_bat = root_path / 'cell_run.bat'
    if not default_bat.exists() or not default_bat.is_file():
        log.info('No default bat file found, creating a default bat file for you.')
        with open(default_bat, 'w', encoding='utf-8') as f:
            f.write('@echo This is a default bat file created by cell module, you should change it for booting your cell instance.\n')
    cmd = f'cd {root_path.absolute()} && start cmd /K {default_bat.absolute()}'
    config['boot_cmd'] = cmd
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, encoding='utf-8', allow_unicode=True)


class Cell(Thread):
    def __init__(self, name, timerange, interval) -> None:
        super().__init__()
        self.name = f'cell_{name}'
        self.timerange = timerange
        self.interval = interval
        self.status = 'init'

    @property
    def timestamp(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def change_status(self, status):
        self.status = status

    def register(self):
        if register_path.exists() and register_path.is_file():
            raise Exception('register_path should be a directory')
        register_path.mkdir(parents=True, exist_ok=True)
        with open(register_path / f'{self.name}.yml', 'w', encoding='utf-8') as f:
            yaml.dump({
                'name': self.name,
                'timerange': self.timerange,
                'interval': self.interval,
                'register_path': config['register_path'],
                'update_path': config['update_path'],
                'boot_cmd': config['boot_cmd']
            }, f, encoding='utf-8', allow_unicode=True)

    def update(self):
        if update_path.exists() and update_path.is_file():
            raise Exception('update_path should be a directory')
        update_path.mkdir(parents=True, exist_ok=True)
        update_file = update_path / (self.name + '_sta.yml')
        with open(update_file, 'w', encoding='utf-8') as f:
            yaml.dump({
                'status': self.status,
                'timestamp': self.timestamp
            }, f, encoding='utf-8', allow_unicode=True)

    def run(self):
        while True:
            self.update()
            if self.status in ['done', 'audo_done', 'error']:
                break
            sleep(self.interval)


seen = set()


def task(name, timerange, interval):
    if name in seen:
        raise Exception(f'{name} has been registered')
    seen.add(name)
    cell = Cell(name, timerange, interval)

    def decorator(func):
        def wrapper(*args, **kwargs):
            cell.register()
            cell.start()
            kwargs.update(change_status=cell.change_status)
            try:
                t = Thread(name=f'main_{name}', target=func, args=args, kwargs=kwargs)
                t.start()
                t.join()
                if cell.status != 'done':
                    cell.status = 'audo_done'
            except Exception as e:
                log.error(f'Error in main_{name}: {e.with_traceback()}')
                cell.status = 'error'
            cell.join()
        return wrapper
    return decorator
