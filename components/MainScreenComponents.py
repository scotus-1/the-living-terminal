from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Horizontal, Vertical, VerticalScroll,  Container
from textual.widgets import Label, Input,  ListView, ListItem, Switch



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
            Label("TIME:"), Switch(animate=False, id="time_switch")
        ),
        Horizontal(
            Label("RF:"), Switch(animate=False, id="rf_switch")
        ),
        Vertical(Label("ver0.1.0-beta-3"), id="version-label")
        )


class TerminalInput(Widget):
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Label(">"),
            Input(placeholder="command [argument]")
        )

class MainWidgetContainer(Widget):
    def compose(self) -> ComposeResult:
        yield Container(id="mainwidgetcontainer")
    

class TopHeader(Widget):
    def compose(self) -> ComposeResult:
        yield Container(Label("@ ApertureOS", id="title"))