from time import monotonic
from typing import Type

from textual.app import App, CSSPathType, ComposeResult
from textual.containers import Container
from textual.driver import Driver
from textual.reactive import reactive
from textual.widgets import Label




class LoginForm(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "LoginForm.css"
    
    def __init__(self, driver_class: Type[Driver] | None = None, css_path: CSSPathType | None = None, watch_css: bool = False):
        super().__init__(driver_class, css_path, watch_css)
        self.apt_logo = """
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
        self.apt_text = """
                                      dP                               .88888.  .d88888b  
                                      88                              d8'   `8b 88.    '
.d8888b. 88d888b. .d8888b. 88d888b. d8888P dP    dP 88d888b. .d8888b. 88     88 `Y88888b. 
88'  `88 88'  `88 88ooood8 88'  `88   88   88    88 88'  `88 88ooood8 88     88       `8b 
88.  .88 88.  .88 88.  ... 88         88   88.  .88 88       88.  ... Y8.   .8P d8'   .8P 
`88888P8 88Y888P' `88888P' dP         dP   `88888P' dP       `88888P'  `8888P'   Y88888P  
        88                                                                               
        dP    
"""
    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Container(Label(self.apt_logo), id="apt_logo")
        yield Label(self.apt_text, id="apt_text")


if __name__ == "__main__":
    app = LoginForm()
    app.run()
