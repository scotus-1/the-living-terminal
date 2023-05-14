import glob
from textual.app import App
from screens.WelcomeScreen import WelcomeScreen



class TheLivingTerminal(App):
    """A Textual app to manage stopwatches."""
     
    CSS_PATH = list(glob.glob("./css/*.css"))
    SCREENS = {"welcome": WelcomeScreen()}
   
    def on_login_form_authenticated(self) -> None:
        self.pop_screen()

    def on_mount(self) -> None:
        self.push_screen("welcome")


if __name__ == "__main__":
    app = TheLivingTerminal()
    app.run()
