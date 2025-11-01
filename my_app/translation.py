from modeltranslation.translator import translator, TranslationOptions
from my_app.models import Room

class RoomTranslationOptions(TranslationOptions):
    fields = ('description', 'room_type')

translator.register(Room, RoomTranslationOptions)