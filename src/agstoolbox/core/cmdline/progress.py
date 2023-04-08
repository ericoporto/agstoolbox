from __future__ import annotations  # for python 3.8
import sys

# progress bar logic extracted from 'progress' module from Georgios Verigakis
# we are using a very simplified version to work in most terminals (in win, and linux, ...)


class ProgressBar:
    if sys.platform.startswith('win'):
        phases = (' ', '▌', '█')
    else:
        phases = (' ', '▏', '▎', '▍', '▌', '▋', '▊', '▉', '█')

    def __init__(self, l_text: str, r_text: str, max_value: int, unit: str = '', width: int = 32):
        self.max: int = max_value
        self.width: int = width
        self.progress: float = 0.0
        self.l_text: str = l_text
        self.r_text: str = r_text
        self.unit = unit

    def update(self, current_value: int, total_size: int):
        self.max = total_size
        self.progress: float = current_value / self.max
        filled_len = self.width * self.progress
        nfull: int = int(filled_len)
        phase: int = int((filled_len - nfull) * len(self.phases))
        nempty: int = self.width - nfull

        bar: str = self.phases[-1] * nfull
        current: str = self.phases[phase] if phase > 0 else ''
        empty: str = ' ' * max(0, nempty - len(current))
        line = f"{current_value}/{self.max} {self.unit} |{bar}{current}{empty}|"

        sys.stdout.write('\r' + self.l_text + line + self.r_text)
        sys.stdout.flush()

    def finish(self):
        self.progress = self.max
        sys.stdout.write('\n')
        sys.stdout.flush()
