# Compatibility wrapper module
# Some parts of the codebase import `apps.dashboard.mongo_models`.
# To avoid duplicating model definitions, re-export the models
# defined in `apps.dashboard.models` from here.

from .models import CourseContent, StudentProgress

__all__ = ["CourseContent", "StudentProgress"]
