# EXPERIMENTAL: MongoEngine-backed CourseDocument (optional)
# This file contains experimental MongoEngine models for storing courses as
# documents. Keep only for reference or experimentation; the project uses
# Django ORM for core domain models by default.

from datetime import datetime
from decimal import Decimal

from mongoengine import Document, EmbeddedDocument, fields


class LessonEmbedded(EmbeddedDocument):
    title = fields.StringField(required=True)
    video_url = fields.URLField()
    content = fields.StringField()
    order = fields.IntField()


class ModuleEmbedded(EmbeddedDocument):
    title = fields.StringField(required=True)
    order = fields.IntField()
    lessons = fields.EmbeddedDocumentListField(LessonEmbedded)


class CourseDocument(Document):
    meta = {
        'collection': 'courses',
        'ordering': ['-created_at'],
    }

    instructor_id = fields.IntField(required=True)
    title = fields.StringField(required=True, max_length=255)
    description = fields.StringField()
    price = fields.DecimalField(precision=2, default=Decimal('0.00'))
    is_published = fields.BooleanField(default=False)
    modules = fields.EmbeddedDocumentListField(ModuleEmbedded)
    created_at = fields.DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return self.title

    def to_dict(self):
        # Lightweight serializer for tests / examples
        return {
            'instructor_id': self.instructor_id,
            'title': self.title,
            'description': self.description,
            'price': str(self.price),
            'is_published': self.is_published,
            'modules': [
                {
                    'title': m.title,
                    'order': m.order,
                    'lessons': [
                        {'title': l.title, 'order': l.order, 'video_url': l.video_url, 'content': l.content}
                        for l in m.lessons
                    ],
                }
                for m in self.modules
            ],
            'created_at': self.created_at.isoformat(),
        }