from textual.app import ComposeResult
from textual.containers import Vertical
from textual.timer import Timer
from textual.screen import Screen
from textual.widgets import ProgressBar, TextLog


class LoadingScreen(Screen):
    progress_timer: Timer
    def compose(self) -> ComposeResult:
        self.progress_markers = TextLog()
        with Vertical():
            yield self.progress_markers
            yield ProgressBar()
            

    def on_mount(self) -> None:
        """Set up a timer to simulate progess happening."""
        self.progress_timer = self.set_interval(1 / 10, self.make_progress, pause=True)
        self.action_start()

    def make_progress(self) -> None:
        bar = self.query_one(ProgressBar)
        value = bar.percentage
        
        animation = {
            0: {
                "rate": 1,
                "text": "Initializing Operating System"
            },
            0.01: {
                "rate": 0.25,
                "text": "Mounting [nvme01p1, nvme01p2, sda1, sdb1]"
            },
            0.17: {
                "rate": 0.5,
                "text": "Secondary Kernal aperture-zen boot.INIT"
            },
            0.25: {
                "rate": 0.25,
                "text": "Patching CPU Microcode"
            },
            0.30: {
                "rate": 2,
                "text": "Tunneling to ApertureNet"
            },
            0.60: {
                "rate": 0.5,
                "text": "Setting Up Peer2Peer Radio Connections: Logging in as yr-protagonist"
            },
            0.85: {
                "rate": 0.25,
                "text": "Loading File System at /home"
            },
            0.90: {
                "rate": 0.5,
                "text": "Loading Applications"
            }
        }
        
        animation_change = animation.get(value, None)
        if animation_change:
            self.change_rate = animation_change['rate']
            self.progress_markers.write("[borealisBootloader ver0.0.1-alpha-6ecb55] " + animation_change['text'])
        
        bar.advance(self.change_rate)


    def action_start(self) -> None:
        """Start the progress tracking."""
        self.query_one(ProgressBar).update(total=100)
        self.progress_timer.resume()