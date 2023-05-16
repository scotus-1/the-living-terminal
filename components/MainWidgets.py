import random
import string
from collections import OrderedDict
from faker import Faker

from textual.app import ComposeResult, App
from textual.widget import Widget
from textual.containers import Horizontal, Vertical, Center, Middle, Container
from textual.widgets import Label, DataTable, TabbedContent, TabPane, RadioButton
from textual.reactive import reactive


def app_query(widget: Widget, query):
    current_parent = widget
    while True:
        if current_parent.parent: 
            current_parent = current_parent.parent
        
        if isinstance(current_parent, App):
            return current_parent.query(query)
        

class Directory(Widget):
    directory_seed = reactive(0)

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("LIVING HUMAN DIRECTORY"),
            DataTable(show_cursor=False, zebra_stripes=True)
        )
    
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
        
        Faker.seed(self.directory_seed)
        random.seed(self.directory_seed)

        rows = []
        for index in range(100):
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
            parents = fake[locale].first_name_male() + "," + fake[locale].first_name_female()
            birthday = profile['birthdate']
            location = str(profile['current_location'][0]) + " , " + str(profile['current_location'][1])
            blood_type = profile['blood_group']

            rows.append((index, id, name, parents, birthday, gender, location, blood_type))


        table = self.query_one(DataTable)
        table.add_columns(*("Index", "ID", "Name", "Parents","Birthday", "Gender", "Location", "Blood Type"))
        table.add_rows(rows)


class Viewer(Widget):
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield DataTable(show_cursor=False)
            yield Center(
                Middle(
                Label("Test\nasd\nasdsad\ndadsasdasdsadsadsadad")
                )
            )

    def on_mount(self) -> None:
        files = app_query(self, MainScreen).first().files
        table = self.query_one(DataTable)
        table.add_columns(*("Index", "Name", "filename", "Starred"))
        for index, file in enumerate(files):
            table.add_row(index, file[0], file[1], file[2])


class Mail(Widget):
    def compose(self) -> ComposeResult:
        with Container():
            with TabbedContent():
                with TabPane("Message"):
                    yield Label("Test")
        

class Clock(Widget):
    def compose(self) -> ComposeResult:
        time_on = not app_query(self, MainScreen).first().time_on
        print(time_on)

        yield Vertical(
            Label("Clock"),
            Horizontal(
                RadioButton("past", id="past_button", disabled=time_on),
                RadioButton("present", id="present_button", disabled=time_on),
                RadioButton("future", id="future_button", disabled=time_on)
            )
        )
    

    def on_mount(self):
        time_setting = app_query(self, MainScreen).first().time_setting
        if time_setting == "past":
            self.query_one("#past_button").value = True
        elif time_setting == "present":
            self.query_one("#present_button").value = True
        elif time_setting == "future":
            self.query_one("#future_button").value = True

    def on_radio_button_changed(self, message:RadioButton.Changed):
        for radio_button in self.query():
            if not radio_button.id == message.radio_button.id:
                with radio_button.prevent(RadioButton.Changed):
                    radio_button.value=False
            else:
                if message.radio_button.value == False: message.radio_button.value = True
                
                if message.radio_button.id == "past_button":
                    app_query(self, MainScreen).first().time_setting = "past"
                elif message.radio_button.id == "present_button":
                    app_query(self, MainScreen).first().time_setting = "present"
                elif message.radio_button.id == "future_button":
                    app_query(self, MainScreen).first().time_setting = "future"
                


class Radio(Widget):
    def compose(self) -> ComposeResult:
        yield Label("Test")


class Help(Widget):
    def compose(self) -> ComposeResult:
        yield Label("Help")