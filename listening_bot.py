#from webex_bot.commands.echo import EchoCommand
from expe import ExpeCommand
from webex_bot.webex_bot import WebexBot
from send_file import SendfileCommand
from credentials import credentials

# Create a Bot Object

class ExpeBot(WebexBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.commands = set()
        self.help_command.commands = set ()
        self.card_callback_commands = None
if __name__ == '__main__':

    bearer = credentials['bearer']
    #bot = WebexBot(teams_bot_token = bearer)
    bot = ExpeBot(teams_bot_token = bearer)
    # Add new commands for the bot to listen out for.
    #bot.add_command(EchoCommand())
    bot.add_command(ExpeCommand())
    bot.add_command(SendfileCommand())
    # Call `run` for the bot to wait for incoming messages.
    bot.run()
