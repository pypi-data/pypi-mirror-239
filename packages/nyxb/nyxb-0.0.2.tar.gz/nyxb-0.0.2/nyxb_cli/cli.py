import webbrowser
import argparse

class DiscordCommand:
    discord_url = "https://nyxb.chat"

    @staticmethod
    def exec():
        webbrowser.open(DiscordCommand.discord_url)

def main():
    parser = argparse.ArgumentParser(description='Nyxb CLI')
    parser.add_argument('command', metavar='discord', help="Opens Nyxb's Discord Server.")
    args = parser.parse_args()

    if args.command == 'discord':
        DiscordCommand.exec()

if __name__ == "__main__":
    main()
