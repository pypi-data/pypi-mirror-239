from .connection import select_port, ConnectionContext, requires_connection, print_exc
from ._aura_pybind import AuraSerialHub
from ._aura_pybind import TimeoutException, IOException, PortNotOpenedException
import sys


class AuraGatewayClient(ConnectionContext):
    """
        manages a connection to the Aura Gateway.
    """

    def __init__(self, port_name=""):
        """
        :param port_name: name of a specific port to connect to e.g. COM3 on Windows.
                        if left empty, can be auto-detected.
        """
        self._aura_client_impl = AuraSerialHub()

        if len(port_name):
            self._aura_client_impl.set_port_name(port_name)

    def get_port_name(self):
        return self._aura_client_impl.get_port_name()

    def connect(self, silent=False):
        """
        establishes a serial connection to an Aura gateway
        :return: whether the connection was successful or not
        """

        if not self.get_port_name():
            try:
                port_name = select_port()
                #if not silent:
                #    print('Connecting to serial:', port_name)
                self._aura_client_impl.set_port_name(port_name)
            except PortNotOpenedException as exc:
                if not silent:
                    print(str(exc))
                return False
            except KeyboardInterrupt:
                if sys.platform.startswith("linux"):
                    print()
                return False

        try:
            self._aura_client_impl.connect()
        except TimeoutException:
            return False

        return True

    def disconnect(self, force_disconnect=False, silent=False):
        self._aura_client_impl.disconnect(force_disconnect)

    def is_connected(self):
        return self._aura_client_impl.is_connected()

    def get_connected_version(self):
        return self._aura_client_impl.get_connected_version()
