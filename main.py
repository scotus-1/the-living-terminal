import glob
import sys
from textual.app import App
from screens.WelcomeScreen import WelcomeScreen
from screens.LoadingScreen import LoadingScreen

from components.MainWidgets import *
from components.MainScreenComponents import *
from textual.screen import Screen
from textual.reactive import var
import string
import decimal


class MainScreen(Screen):
    current_widget = reactive(5)
    directory_filter = var((None, ""))
    directory_seed = var(0)
    files = reactive([
        ("Elizabeth", "Elizabeth.prs", True)
    ])
    time_setting = reactive("present")
    time_on = reactive(False)
    rf_on = reactive(False)
    radio_code = reactive("")
    radio_frequency = reactive("")

    def on_list_view_selected(self, event):
        widget = event.list_view.index
        if widget == self.current_widget: return

        self.current_widget = widget
        main_widget_container = self.query_one("#mainwidgetcontainer")
        
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

        if main_widget_container.children:
            main_widget_container.children[0].remove()
        main_widget_container.mount(mount_widget)

    def on_switch_changed(self, message:Switch.Changed):
        switch = message.switch
        
        if switch.id == "time_switch" and switch.value == False:
            self.time_on = not self.time_on
            for radio_button in self.query("Clock RadioButton"):
                radio_button.disabled = True
                
        elif switch.id == "time_switch" and switch.value == True:
            self.time_on = not self.time_on
            for radio_button in self.query("Clock RadioButton"):
                radio_button.disabled = False
        
        elif switch.id == "rf_switch" and switch.value == False:
            self.rf_on = not self.rf_on
            for rf_input in self.query("Radio Input"):
                rf_input.disabled = True
                                       

        elif switch.id == "rf_switch" and switch.value == True:
            self.rf_on = not self.rf_on
            for rf_input in self.query("Radio Input"):
                rf_input.disabled = False

        print("test")

    def on_input_submitted(self, message: Input.Submitted):
        command = message.input.value.strip()
        command = command.split(" ")

        try: 
            assert command != [""]
        except AssertionError:
            with message.input.prevent(Input.Changed):
                message.input.value = ""
            return

        invoked_command = command[0]

        if invoked_command == "filter":
            try:
                if command[1] == "reset":
                    self.directory_filter = (None, "")
                else:
                    self.directory_filter = (command[1].lower(), command[2].lower())
            except IndexError:
                with message.input.prevent(Input.Changed):
                    message.input.value = ""
                return

        with message.input.prevent(Input.Changed):
            message.input.value = ""
    
    def validate_directory_filter(self, directory_filter):
        filter = directory_filter[0]
        filter_string = directory_filter[1]
        try: 
            if filter == "id":
                assert len(filter_string) == 16
                allowed = set(string.ascii_lowercase + string.ascii_uppercase + string.digits)
                assert set(filter_string) <= allowed
            elif filter == "parents":
                parents = filter_string.split(",")
                allowed = set(string.ascii_lowercase + string.ascii_uppercase)
                assert len(parents) == 2
                assert set(parents[0]) <= allowed
                assert set(parents[1]) <= allowed
                assert len(parents[0]) < 15
                assert len(parents[1]) < 15
            elif filter == "birthday":
                birthday = filter_string.split("-")
                assert len(birthday) == 3
                assert len(birthday[0]) == 4 and int(birthday[0]) >= 1900 and int(birthday[0]) <= 2023
                assert len(birthday[1]) <= 2 and int(birthday[1]) >= 1 and int(birthday[1]) <= 12
                assert len(birthday[2]) <= 2 and int(birthday[2]) >= 1 and int(birthday[2]) <= 31
            elif filter == "location":
                location = filter_string.split(",")
                assert len(location) == 2
                try:
                    assert decimal.Decimal(location[0]) >= 0 and decimal.Decimal(location[0]) <= 100
                    assert decimal.Decimal(location[1]) >= 0 and decimal.Decimal(location[1]) <= 100
                except:
                    raise AssertionError
            else:
                return (None, "")
            
            return (filter, filter_string)
        
        except AssertionError:
            return (None, "")
    

    def watch_directory_filter(self, filter):
        
        if filter == (None, ""):
            self.directory_seed = 0
        else:
            self.directory_seed = filter[0] + filter[1]

        print(self.directory_seed)
        main_widget_container = self.query_one("#mainwidgetcontainer")
        if isinstance(main_widget_container.children[0], Directory):
            main_widget_container.children[0].remove()
            main_widget_container.mount(Directory())


    def compose(self) -> ComposeResult:
        yield TopHeader()
        with Horizontal():
            yield SideBar()
            with Vertical():
                yield MainWidgetContainer()
                yield TerminalInput()
    

    def on_mount(self) -> ComposeResult:
        main_screen = self.query_one("#mainwidgetcontainer")
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
