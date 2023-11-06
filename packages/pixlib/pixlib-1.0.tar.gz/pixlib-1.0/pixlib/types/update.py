import pixlib


class Update:
    def stop_propagation(self):
        raise pixlib.StopPropagation

    def continue_propagation(self):
        raise pixlib.ContinuePropagation
