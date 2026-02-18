from abc import ABC, abstractmethod

class AIBase(ABC):
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """Generate a response based on the given prompt."""
        pass