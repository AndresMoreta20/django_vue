from abc import ABC, abstractmethod

class FlashcardCreationStrategy(ABC):
    @abstractmethod
    def create_flashcard(self, input_data):
        """
        Create a flashcard based on the given input data.
        :param input_data: The data used for creating the flashcard.
        :return: Flashcard object or equivalent data structure.
        """
        pass