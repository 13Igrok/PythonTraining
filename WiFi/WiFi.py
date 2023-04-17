import os


class Finder:
    def __init__(self, *args, **kwargs):
        self.server_name = kwargs['server_name']
        self.password = kwargs['password']
        self.interface_name = kwargs['interface']
        self.main_dict = {}

    def run(self):
        command = """sudo iwlist wlp2s0 scan | grep -ioE 'ssid:"(.*{}.*)'"""
        result = os.popen ( command.format ( self.server_name ) )
        result = list ( result )

        if "Device or resource busy" in result:
            return None
        ssid_list = [item.lstrip ( 'SSID:' ).strip ( '"\n' ) for item in result]
        print ( f"Successfully get ssids {ssid_list}" )

        for name in ssid_list:
            try:
                result = self.connection ( name )
            except Exception as exp:
                print ( f"Couldn't connect to name : {name}. {exp}" )
            else:
                if result:
                    print ( f"Successfully connected to {name}" )

    def connection(self, name):  # sourcery skip: raise-specific-error
        cmd = f"nmcli d wifi connect {name} password {self.password} iface {self.interface_name}"
        try:
            if os.system ( cmd ) != 0:  # This will run the command and check connection
                raise Exception ()
        except:
            raise  # Not Connected
        else:
            return True  # Connected


if __name__ == "__main__":
    # Server_name is a case insensitive string, and/or regex pattern which demonstrates
    # the name of targeted WIFI device or a unique part of it.
    server_name = "example_name"
    password = "your_password"
    interface_name = "your_interface_name"  # i. e wlp2s0
    F = Finder ( server_name=server_name,
                 password=password,
                 interface=interface_name )
    F.run ()
