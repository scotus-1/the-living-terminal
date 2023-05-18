import random
import string
from collections import OrderedDict
from faker import Faker
from textual.app import ComposeResult, App
from textual.widget import Widget
from textual.containers import Horizontal, Vertical, Center, Middle, Container, VerticalScroll, ScrollableContainer
from textual.widgets import Label, DataTable, TabbedContent, TabPane, RadioButton, Input, Markdown, TextLog
from main import MainScreen
from components import content


def app_query(widget: Widget, query):
    current_parent = widget
    while True:
        if current_parent.parent: 
            current_parent = current_parent.parent
        
        if isinstance(current_parent, App):
            return current_parent.query(query)


class Directory(Widget):
    def generate_filler_person(self, fake: Faker):
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
        
        return (id, name, parents, birthday, gender, location, blood_type)
    
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("LIVING HUMAN DIRECTORY"),
            DataTable(show_cursor=False, zebra_stripes=True, id="directorytable")
        )
    
    def on_mount(self) -> None:
        rows = []
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
        
        directory_seed = app_query(self, MainScreen).first().directory_seed
        Faker.seed(directory_seed)
        random.seed(directory_seed)
        
        item_count = 100
        directory_filter = app_query(self, MainScreen).first().directory_filter
        table = self.query_one(DataTable)

        for index in range(item_count):
            rows.append((index, *self.generate_filler_person(fake)))

        new_rows = rows
        if directory_filter[0] != None:
            if directory_filter[0] == "parents":
                new_rows = []
                for row in rows:
                    row = list(row)
                    row[3] = directory_filter[1]
                    row = tuple(row)
                    new_rows.append(row)
                new_rows = new_rows[:random.randint(7,11)]

                if directory_filter[1] == "Lindsey,Mark":
                    insert_index = random.randint(0, len(new_rows) - 1)
                    new_rows.insert(insert_index, 
                        (0, "l1m0Ty17MDvb1NmQ", "Timothy Portman", "Lindsey,Mark", "1997-10-08", "Male", "33.6145123 , -117.87548926","B-")
                                    )
                    
                    new_new_rows = []
                    for index, row in enumerate(new_rows):
                        row = list(row)
                        row[0] = index 
                        row = tuple(row)
                        
                        new_new_rows.append(row)
                    new_rows = new_new_rows


            elif directory_filter[0] == "birthday":
                new_rows = []
                for row in rows:
                    row = list(row)
                    row[4] = directory_filter[1]
                    row = tuple(row)
                    new_rows.append(row)
                new_rows = new_rows[:random.randint(24,57)]

                if directory_filter[1] == "1989-12-20":
                    new_rows.insert(random.randint(0, len(new_rows) - 1), 
                        (0, "XOXOXOXOXOXOXOXOX", "Harriet Portman", "Lindsey,Gregory", "1989-12-20", "Female", "33.61980134 , -117.97567426","B+")
                                    )
                    
                    new_new_rows = []
                    for index, row in enumerate(new_rows):
                        row = list(row)
                        row[0] = index 
                        row = tuple(row)
                        
                        new_new_rows.append(row)
                    new_rows = new_new_rows

            elif directory_filter[0] == "location":
                coordinates = directory_filter[1].split(",")
                lat = coordinates[0]
                long = coordinates[1]
                if lat.startswith("50.62") and long.startswith("-96.98"):
                    new_rows = [(0, "aaaaaaaaaaaaaaaa", "Mother", "Grandma,Grandpa", "1955-01-15", "Female", directory_filter[1], "AB+")]
                else: new_rows = []

            elif directory_filter[0] == "id":  
                if directory_filter[1] == "C4Rrlef1l7pEr58M":
                    new_rows = [(0, "C4Rrlef1l7pEr58M", "Carrie Hartfield", "Hartfield,Hartfield", "1989-07-04", "Female", "47.1107853 , -88.5066174", "O-")]
                else: new_rows = []

        table.add_columns(*("Index", "ID", "Name", "Parents","Birthday", "Gender", "Location", "Blood Type"))
        table.add_rows(new_rows)


class Viewer(Widget):
    def compose(self) -> ComposeResult:
        
        with Horizontal():
            yield DataTable(show_cursor=True)
            yield Center(
                Middle(id="content_container")
            )

    def on_mount(self) -> None:
        files = app_query(self, MainScreen).first().files
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.add_columns(*("Index", "Name", "filename", "Starred"))


        for index, file in enumerate(files):
            table.add_row(index, file.name, file.filename, file.starred)
        
        selected_file_index = app_query(self, MainScreen).first().selected_file
        table.cursor_coordinate = (selected_file_index, 0)

        time_on = app_query(self, MainScreen).first().time_on
        
        main_container = self.query("#content_container").first()
        
        if time_on:
            time_setting = app_query(self, MainScreen).first().time_setting
            if time_setting == "past":
                label_content = files[selected_file_index].past
            elif time_setting == "present":
                label_content = files[selected_file_index].present
            elif time_setting == "future":
                label_content = files[selected_file_index].future
        else:
            label_content = files[selected_file_index].present
        
        text_log = TextLog(wrap=True)
        main_container.mount(text_log)
        text_log.write(label_content, width=75)
    
    def on_data_table_row_selected(self, message):
        app_query(self, MainScreen).first().selected_file = message.cursor_row

        
        time_on = app_query(self, MainScreen).first().time_on
        files = app_query(self, MainScreen).first().files
        selected_file_index = message.cursor_row
        if time_on:
            time_setting = app_query(self, MainScreen).first().time_setting
            if time_setting == "past":
                label_content = files[selected_file_index].past
            elif time_setting == "present":
                label_content = files[selected_file_index].present
            elif time_setting == "future":
                label_content = files[selected_file_index].future
        else:
            label_content = files[selected_file_index].present
        
        main_container = self.query("#content_container").first()
        main_container.children[0].remove()
        text_log = TextLog(wrap=True)
        main_container.mount(text_log)
        text_log.write(label_content, width=75)

class Mail(Widget):
    def compose(self) -> ComposeResult:
        messages = app_query(self, MainScreen).first().messages
        with Container():
            with TabbedContent():
                for message in messages:
                    with TabPane(message[0]):
                        yield VerticalScroll(Markdown(message[1]))
        

class Clock(Widget):
    def compose(self) -> ComposeResult:
        time_on = not app_query(self, MainScreen).first().time_on

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
        rf_on = not app_query(self, MainScreen).first().rf_on
        radio_code = app_query(self, MainScreen).first().radio_code
        radio_frequency = app_query(self, MainScreen).first().radio_frequency

        yield Vertical(
            Label("RADIO SETTINGS", id="radio_label"),
            Horizontal(
                Label("RADIO Code: "),
                Input(radio_code, placeholder="######", disabled=rf_on, id="radio_code_input")
            ),
            Horizontal(
                Label("RADIO Frequency: "),
                Input(radio_frequency, placeholder="###.#####", disabled=rf_on, id="radio_frequency_input")
            )
        )
    

    def on_input_changed(self, message):
        changed_input = message.input
        
        if changed_input.id == "radio_code_input":
            if len(changed_input.value) > 6:
                changed_input.value = changed_input.value[:6]
            
            if changed_input.value == "1a5Pm0":
                messages = app_query(self,MainScreen).first().messages

                added_message = False
                for message in messages:
                    if message[0] == "Message - father": added_message = True
                
                if not added_message: app_query(self,MainScreen).first().messages.append(("Message - father", content.FATHER_MESSAGE))

            app_query(self, MainScreen).first().radio_code = changed_input.value

        elif changed_input.id == "radio_frequency_input":
            if len(changed_input.value) > 9:
                changed_input.value = changed_input.value[:9]
            app_query(self, MainScreen).first().radio_frequency = changed_input.value


    def on_input_submitted(self, message): 
        message.stop()


class Help(Widget):
    def compose(self) -> ComposeResult:
        yield ScrollableContainer(Label(content.APERTURE_HELP))