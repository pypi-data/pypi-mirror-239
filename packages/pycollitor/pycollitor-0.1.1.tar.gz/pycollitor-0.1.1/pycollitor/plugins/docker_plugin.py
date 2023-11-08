import docker

from pycollitor.core import Manager


class DockerManager(Manager):
    name = "Docker"

    def connect(self):
        self.client = docker.from_env()

    def collect(self):
        return {
            "Version": self.version,
            # "images": self.images,
            "Containers": self.containers,
            # "volumes": self.volumes,
        }

    @property
    def version(self) -> str:
        return self.client.version()

    @property
    def images(self) -> list:
        return self.client.images.list()

    @property
    def containers(self) -> list:
        return self.client.containers.list()

    @property
    def volumes(self) -> list:
        return self.client.volumes.list()
