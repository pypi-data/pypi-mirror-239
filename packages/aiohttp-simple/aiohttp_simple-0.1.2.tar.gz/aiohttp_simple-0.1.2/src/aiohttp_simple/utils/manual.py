import shutil
from pathlib import Path


class ManualHelper:
    def __init__(self):
        self.data_path = Path(__file__).parent.joinpath("../data")

    def init_config(self, aimPath=None):
        aimPath = aimPath or "./config"
        aimPath = Path(aimPath)
        shutil.copytree(self.data_path.joinpath("config"), aimPath)

    def example(self, aimPath=None):
        aimPath = aimPath or "./example.py"
        aimPath = Path(aimPath)
        shutil.copyfile(self.data_path.joinpath("example.py"), aimPath)
