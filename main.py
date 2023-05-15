import glob
import sys
from textual import events
from textual.app import App
from screens.WelcomeScreen import WelcomeScreen
from screens.LoadingScreen import LoadingScreen

import random
import string
from collections import OrderedDict
from faker import Faker
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Horizontal, Vertical, VerticalScroll, Container, ScrollableContainer
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
        
        fake = Faker(OrderedDict([
                        ('en-US', 1),
                        ('de_DE', 1),
                        ('ja_JP', 1),
                        ('es_ES', 1),
                        ('fr_FR', 1),
                         ('ko_KR', 1),
                        ('ru_RU', 1),
                        ('zh_CN', 1),
                        ('ar_AA', 1)
                    ]))
        Faker.seed(0)

        rows = []
        for _ in range(100):
            id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=16))
            gender = fake.random_element(elements=OrderedDict([("Male", 0.475),("Female", 0.475), ("Non-binary", 0.05)]))
            
            locale = fake.random_element(OrderedDict([
                        ('en-US', 5),
                        ('de_DE', 1),
                        ('ja_JP', 1),
                        ('es_ES', 1),
                        ('fr_FR', 1),
                        ('ko_KR', 1),
                        ('ru_RU', 1),
                        ('zh_CN', 1),
                        ('ar_AA', 1)
                    ]))
            
            
            if gender == "Male":
                name = fake[locale].name_male()
            elif gender == "Female":
                name = fake[locale].name_female()
            elif gender == "Non-binary":
                name = fake[locale].name_nonbinary()

            profile = fake.profile()
            parents = fake[locale].first_name() + "," + fake[locale].first_name_female()
            birthday = profile['birthdate']
            location = str(profile['current_location'][0]) + " , " + str(profile['current_location'][1])
            blood_type = profile['blood_group']

            rows.append((id, name, parents, birthday, gender, location, blood_type))


        table = self.query_one(DataTable)
        table.add_columns(*("ID", "Name", "Username", parents, "Gender", "Location", "Blood Type"))
        table.add_rows(rows[1:])

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
        yield ScrollableContainer(id="mainscreen")
    

class TopHeader(Widget):
    def compose(self) -> ComposeResult:
        yield Container(Label("ApertureOS", id="title"))
        


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

