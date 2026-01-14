
# Create your models here.
from mongoengine import (
    Document, EmbeddedDocument,
    StringField, IntField,
    ListField, EmbeddedDocumentField,
    DateTimeField
)
import datetime


class LessonEmbedded(EmbeddedDocument):
    lesson_id = StringField(required=True)
    title = StringField(required=True)
    video_url = StringField()
    duration = IntField()


class ModuleEmbedded(EmbeddedDocument):
    title = StringField(required=True)
    order = IntField()
    lessons = ListField(EmbeddedDocumentField(LessonEmbedded))


class CourseContent(Document):
    meta = {'collection': 'course_contents'}

    course_id = IntField(required=True)  # FK to SQL Course.id
    modules = ListField(EmbeddedDocumentField(ModuleEmbedded))
    created_at = DateTimeField(default=datetime.datetime.utcnow)


class StudentProgress(Document):
    meta = {'collection': 'student_progress'}

    user_id = IntField(required=True)
    course_id = IntField(required=True)
    completed_lessons = ListField(StringField())
    progress_percent = IntField(default=0)
    last_updated = DateTimeField(default=datetime.datetime.utcnow)
