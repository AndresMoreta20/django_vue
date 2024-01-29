from collections import Counter
from ..models import UserSavedLecturespace, UserSavedFlashcard


def get_user_saved_data(user):
    saved_lecturespaces = UserSavedLecturespace.objects.filter(user=user)
    saved_flashcards = UserSavedFlashcard.objects.filter(user=user)
    return saved_lecturespaces, saved_flashcards

def process_tags(saved_lecturespaces):
    tag_list = [tag.name for saved_ls in saved_lecturespaces for tag in saved_ls.lecturespace.tags.all()]
    most_common_tags = Counter(tag_list).most_common()
    return most_common_tags

