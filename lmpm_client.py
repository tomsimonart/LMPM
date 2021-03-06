from server import Client

class MainClient():
    def __init__(self, addr):
        self._addr = addr
        self.client = Client(self._addr)

    def close(self):
        self.client.close()

    def load_index(self):
        return self.client.call("LOADINDEX")

    def load_plugin(self, id_):
        return self.client.call("LOADPLUGIN", id_)

    def load_webview(self):
        return self.client.call("LOADWEBVIEW")

    def get_state(self):
        return self.client.call("GETSTATE")

    def send_event(self, event):
        return self.client.call("SENDEVENT", event)


class PluginClient():
    def __init__(self, addr):
        self._addr = addr
        self.client = Client(self._addr)

    def close(self):
        self.client.close()

    def refresh(self):
        return self.client.call("SENDWEBVIEW")
