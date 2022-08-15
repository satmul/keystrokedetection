class Device:
    def __init__(self, device_id, slave_id, name):
        self.device_id = device_id
        self.slave_id = slave_id
        self.name = name.strip()