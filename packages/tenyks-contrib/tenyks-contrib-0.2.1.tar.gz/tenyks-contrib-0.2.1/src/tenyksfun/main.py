from datetime import date
import random

from tenyks.client import Client, run_client


class TenyksFun(Client):

    direct_only = False

    def __init__(self, *args, **kwargs):
        self.hello_counts = {}
        super(TenyksFun, self).__init__(*args, **kwargs)

    def handle(self, data, match, filter_name):
        if data['payload'] == "You're doing great work tenyks!":
            self.send('!m tenyks', data)


def main():
    run_client(TenyksFun)


if __name__ == '__main__':
    main()
