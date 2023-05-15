import glob
import sys
from textual import events
from textual.app import App
from screens.WelcomeScreen import WelcomeScreen
from screens.LoadingScreen import LoadingScreen

from textual.screen import Screen
from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Horizontal, Vertical, VerticalScroll, Container
from textual.widgets import Label, Input, MarkdownViewer, DataTable, ListView, ListItem, Switch

class SideBar(Widget):
    def compose(self) -> ComposeResult:
        yield VerticalScroll(
        ListView(
            ListItem(Label("\[directory]")),
            ListItem(Label("\[viewer]")),
            ListItem(Label("\[mail]")),
            ListItem(Label("\[clock]")),
            ListItem(Label("\[radio]")),
            ListItem(Label("\[help]")),
        initial_index=5),
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
        yield Horizontal(
            Label(">"),
            Input(placeholder="command [argument]")
        )
        

class Directory(Widget):
    def compose(self) -> ComposeResult:
        yield DataTable()
    
    def on_mount(self) -> None:
        ROWS = [
    ("lane", "swimmer", "country", "time"),
    (4, "Joseph Schooling", "Singapore", 50.39),
    (2, "Michael Phelps", "United States", 51.14),
    (5, "Chad le Clos", "South Africa", 51.14),
    (6, "László Cseh", "Hungary", 51.14),
    (3, "Li Zhuhao", "China", 51.26),
    (8, "Mehdy Metella", "France", 51.58),
    (7, "Tom Shields", "United States", 51.73),
    (1, "Aleksandr Sadovnikov", "Russia", 51.84),
    (10, "Darren Burns", "Scotland", 51.84),
]
        table = self.query_one(DataTable)
        table.add_columns(*ROWS[0])
        table.add_rows(ROWS[1:])

class Viewer(Widget):
    def compose(self) -> ComposeResult:
        yield Label("Test")


class Mail(Widget):
    def compose(self) -> ComposeResult:
        yield Label("Test")


class Clock(Widget):
    def compose(self) -> ComposeResult:
        yield Label("Test")


class Radio(Widget):
    def compose(self) -> ComposeResult:
        yield Label("Test")


class Help(Widget):
    def compose(self) -> ComposeResult:
        yield Label("Help")


class MainWidgetContainer(Widget):
    def compose(self) -> ComposeResult:
        yield Container(id="mainscreen")
    

class TopHeader(Widget):
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Label("\[X]", id="title_button"),
            Label("ApertureOS", id="title")
        )


class MainScreen(Screen):
    
    def on_list_view_selected(self, event):
        widget = event.list_view.index
        main_screen = self.query_one("#mainscreen")
        
        if widget == 0:
            mount_widget = Directory()
        elif widget == 1:
            mount_widget = Viewer()
        elif widget == 2:
            mount_widget = Mail()
        elif widget == 3:
            mount_widget = Clock()
        elif widget == 4:
            mount_widget = Radio()
        elif widget == 5:
            mount_widget = Help()

        if main_screen.children:
            main_screen.children[0].remove()
        main_screen.mount(mount_widget)


    def compose(self) -> ComposeResult:
        yield TopHeader()
        with Horizontal():
            yield SideBar()
            with Vertical():
                yield MainWidgetContainer()
                yield TerminalInput()
    
    def on_mount(self) -> ComposeResult:
        main_screen = self.query_one("#mainscreen")
        main_screen.mount(Help())


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

