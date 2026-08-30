class IncidentNotFoundException(Exception):

    def __init__(self):

        self.message = "Incident not found."

        super().__init__(self.message)