from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Label, Input
from textual.widget import Widget
from textual.screen import Screen
from textual.message import Message
from textual import log

class LoginForm(Widget):
    class Authenticated(Message):
        pass

    def validate_login(self):
        input_fields = self.query("LoginForm Input")
        username = input_fields.first().value.strip()
        password = input_fields.last().value.strip()
        
        if username == "yr_protagonist" and password == "Th3c&k3i5@1!E":
            log("Authenticated")
            self.box.border_subtitle = None
            self.post_message(self.Authenticated())

        elif username == "" or password == "":
            self.box.border_subtitle = "Missing field"
        else:
            self.box.border_subtitle = "Incorrect username or password"

    class submitLabel(Label):
        def action_submit_login(self):
            self.post_message(Input.Submitted(Input(), ""))

    def on_input_submitted(self):
        self.validate_login()

    def compose(self) -> ComposeResult:
        submit_text = "[@click=submit_login()][ submit ][/]"
        self.box = Vertical(
            Horizontal(
                Label("username: "),
                Input(),
                classes="input_container"
            ),
            Horizontal(
                Label("password: "),
                Input(password=True),
                classes="input_container"
            ),
            self.submitLabel(submit_text, classes="input_container")
        , id="box")
        self.box.border_title = "login"
        yield self.box


class ApertureWelcome(Widget):
    def compose(self) -> ComposeResult:
        apt_logo = """
              .,-:;//;:=,
          . :H@@@MM@M#H/.,+%;,
       ,/X+ +M@@M@MM%=,-%HMMM@X/,
     -+@MM; $M@@MH+-,;XMMMM@MMMM@+-
    ;@M@@M- XM@X;. -+XXXXXHHH@M@M#@/.
  ,%MM@@MH ,@%=             .---=-=:=,.
  =@#@@@MX.,                -%HX$$%%%:;
 =-./@M@M$                   .;@MMMM@MM:
 X@/ -$MM/                    . +MM@@@M$
,@M@H: :@:                    . =X#@@@@-
,@@@MMX, .                    /H- ;@M@M=
.H@@@@M@+,                    %MM+..%#$.
 /MMMM@MMH/.                  XM@MH; =;
  /%+%$XHH@$=              , .H@@@@MX,
   .=--------.           -%H.,@@@@@MX,
   .%MM@@@HHHXX$$$%+- .:$MMX =M@@MM%.
     =XMMM@MM@MM#H;,-+HMM@M+ /MMMX=
       =%@M@M#@$-.=$@MM@@@M; %M%=
         ,:+$+-,/H#MMMMMMM@= =,
               =++%%%%+/:-.
    """
        apt_text = """
                                      dP                               .88888.  .d88888b  
                                      88                              d8'   `8b 88.    '
.d8888b. 88d888b. .d8888b. 88d888b. d8888P dP    dP 88d888b. .d8888b. 88     88 `Y88888b. 
88'  `88 88'  `88 88ooood8 88'  `88   88   88    88 88'  `88 88ooood8 88     88       `8b 
88.  .88 88.  .88 88.  ... 88         88   88.  .88 88       88.  ... Y8.   .8P d8'   .8P 
`88888P8 88Y888P' `88888P' dP         dP   `88888P' dP       `88888P'  `8888P'   Y88888P  
        88                                                                               
        dP    
"""

        yield Horizontal(
                    Label(apt_logo, id="apt_logo"),
                    Label(apt_text, id="apt_text"),
                    id="aperture"
            )

class WelcomeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield ApertureWelcome()
        yield Container(LoginForm(), id="LoginContainer")