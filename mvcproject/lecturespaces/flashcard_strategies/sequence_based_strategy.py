from .flashcard_creation_strategy import FlashcardCreationStrategy
import random

class SequenceBasedFlashcardStrategy(FlashcardCreationStrategy):
    def create_flashcard(self, script):
        # Logic to create a flashcard based on a script sequence
        sequence = self.extract_random_sequence(script)
        return sequence  # Or return a flashcard object

    def extract_random_sequence(self, script, sequence_length=10):
        words = script.split()
        if len(words) < sequence_length:
            return None
        start_index = random.randint(0, len(words) - sequence_length)
        return ' '.join(words[start_index:start_index + sequence_length])