import glob
from textual.app import App
from screens.WelcomeScreen import WelcomeScreen
from screens.LoadingScreen import LoadingScreen


class TheLivingTerminal(App):
    """A Textual app to manage stopwatches."""
     
    CSS_PATH = list(glob.glob("./css/*.css"))
    SCREENS = {"welcome": WelcomeScreen(),
                "loading": LoadingScreen()}
   
    def on_login_form_authenticated(self) -> None:
        self.pop_screen()
        self.push_screen("loading")

    def on_mount(self) -> None:
        self.push_screen("welcome")


if __name__ == "__main__":
    app = TheLivingTerminal()
    app.run()
