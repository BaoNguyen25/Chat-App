class Person:
    """
    Representing name, socket client and IP address of person
    """
    def __init__(self, addr, client):
        self.addr = addr
        self.client = client
        self.name = None

    def set_name(self, name):
        """
        Set the persons name
        :param name: str
        :return:
        """
        self.name = name

    def __repr__(self):
        return f"Person({self.addr}, {self.name})"

