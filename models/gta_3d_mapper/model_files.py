import pathlib

class ModelFile:
    def __init__(self):
        self.filedff: pathlib.Path
        self.filetxd: pathlib.Path
        self.is_a_model: bool
