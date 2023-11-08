class MetaManager(type):
    registry: dict = {}

    def __new__(cls, name, bases, attrs):
        new_cls = super().__new__(cls, name, bases, attrs)

        parents = [b for b in bases if isinstance(b, MetaManager)]
        if parents:
            cls.registry[new_cls.__name__] = new_cls

        return new_cls

    @classmethod
    def get_registry(cls):
        return dict(cls.registry)


class Manager(metaclass=MetaManager):
    name: str

    def __init__(
        self,
    ) -> None:
        self.data: dict = {}

    def connect(self):
        raise NotImplementedError()

    def collect(self):
        raise NotImplementedError()

    def run(self):
        print(f"#################### {self.name} ####################")
        try:
            print(f"Connecting to {self.name}")
            self.connect()
        except Exception as e:
            print(f"The {self.name} is down. Here is the error: {e}")
        else:
            print(f"Collecting {self.name} data...")
            self.data = self.collect()


def launch_server(show_terminal: bool = False):
    print("Launching the server...")
    data = {}
    subclasses = MetaManager.get_registry()
    for _, subclass in subclasses.items():
        subclass_instance = subclass()
        subclass_instance.run()
        data[subclass_instance.name] = subclass_instance.data

        if show_terminal:
            for key, value in subclass_instance.data.items():
                print(f"--- {key}: {value}")

    return data
