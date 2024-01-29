from .flashcard_creation_strategy import FlashcardCreationStrategy

class TitleBasedFlashcardStrategy(FlashcardCreationStrategy):
    def create_flashcard(self, video_title):
        # Logic to create a flashcard based on the video title
        # Assuming a simple title-based flashcard creation
        return video_title  # Or return a flashcard object