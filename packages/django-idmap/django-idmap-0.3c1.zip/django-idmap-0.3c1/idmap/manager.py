from django.db.models.manager import Manager

from .queryset import SharedMemoryQuerySet


class SharedMemoryManager(Manager):

    use_for_related_fields = True

    def get_query_set(self):
        return SharedMemoryQuerySet(self.model, using=self._db)
