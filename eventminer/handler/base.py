import abc

__all__ = ['BaseUploadHandler']

class BaseUploadHandler(abc.ABC):
    """Abstract base class for upload API handlers."""

    @abc.abstractmethod
    def setup(self):
        """Load credentials from environment or file and create API object."""
        pass

    @abc.abstractmethod
    def upload(self, path, **kwargs):
        """Upload a file to the target service."""
        pass