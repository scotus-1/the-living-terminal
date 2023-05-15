import glob
import sys
from textual.app import App
from screens.WelcomeScreen import WelcomeScreen
from screens.LoadingScreen import LoadingScreen

from textual.screen import Screen
from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Label, Input, MarkdownViewer, DataTable, ListView, ListItem, Switch

class SideBar(Widget):
    def compose(self) -> ComposeResult:
        yield VerticalScroll(
        ListView(
            ListItem(Label("\[directory]")),
            ListItem(Label("\[viewer]")),
            ListItem(Label("\[messenger]")),
            ListItem(Label("\[clock]")),
            ListItem(Label("\[radio]")),
            ListItem(Label("\[help]")),
        ),
        Horizontal(
            Label("TIME:"), Switch(animate=False)
        ),
        Horizontal(
            Label("RF:"), Switch(animate=False)
        ),
        Vertical(Label("ver0.1.0-beta-3"), id="version-label")
        )


class TerminalInput(Widget):
    def compose(self) -> ComposeResult:
        yield Input()


class TopHeader(Widget):
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Label("\[X]", id="title_button"),
            Label("ApertureOS", id="title")
        )


class MainScreen(Screen):
    def compose(self) -> ComposeResult:
        
        yield TopHeader()
        with Horizontal():
            yield SideBar()
            yield Label("Test")
        yield TerminalInput()
        


class TheLivingTerminal(App):
    """A Textual app to manage stopwatches."""
     
    CSS_PATH = list(glob.glob("./css/*.css"))
    SCREENS = {"welcome": WelcomeScreen(),
                "loading": LoadingScreen(),
                "main": MainScreen()}
   
    def on_loading_screen_progress_bar_complete(self) -> None:
        self.pop_screen()
        self.push_screen("main")

    def on_login_form_authenticated(self) -> None:
        self.pop_screen()
        self.push_screen("loading")

    def on_mount(self) -> None:
        if __name__ == "__main__" and len(sys.argv) > 1:
            self.push_screen(sys.argv[1])
        else: 
            self.push_screen("welcome")


if __name__ == "__main__":
    app = TheLivingTerminal()
    app.run()

