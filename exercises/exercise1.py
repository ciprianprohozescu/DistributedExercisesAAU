import random

from emulators.Device import Device
from emulators.Medium import Medium
from emulators.MessageStub import MessageStub


class GossipMessage(MessageStub):

    def __init__(self, sender: int, destination: int, secrets):
        super().__init__(sender, destination)
        # we use a set to keep the "secrets" here
        self.secrets = secrets

    def __str__(self):
        return f'{self.source} -> {self.destination} : {self.secrets}'


class Gossip(Device):

    def __init__(self, index: int, number_of_devices: int, medium: Medium):
        super().__init__(index, number_of_devices, medium)
        # for this exercise we use the index as the "secret", but it could have been a new routing-table (for instance)
        # or sharing of all the public keys in a cryptographic system
        self._secrets = set([index])

    def run(self):
        # the optimal solution is to "loop" through the devices twice, each time sending a message to the next one
        # in the second loop, we stop before reaching the last device, as it already has all the secrets

        # first loop
        while len(self._secrets) < self.index() + 1:
            ingoing: GossipMessage = self.medium().receive()
            if ingoing:
                self.add_secrets(ingoing.secrets)

        neighbour = self.index() + 1
        if self.index() == self.number_of_devices() - 1:
            neighbour = 0
        message = GossipMessage(self.index(), neighbour, self._secrets)
        self.medium().send(message)

        # second loop
        if self.index() == self.number_of_devices() - 1:
            # this is the last device, we're done
            return

        while len(self._secrets) < self.number_of_devices():
            ingoing: GossipMessage = self.medium().receive()
            if ingoing:
                self.add_secrets(ingoing.secrets)

        if self.index() == self.number_of_devices() - 2:
            # this is the penultimate device, we're done
            return

        neighbour = self.index() + 1
        message = GossipMessage(self.index(), neighbour, self._secrets)
        self.medium().send(message)

    def print_result(self):
        print(f'\tDevice {self.index()} got secrets: {self._secrets}')

    def add_secrets(self, new_secrets):
        self._secrets.update(new_secrets)
