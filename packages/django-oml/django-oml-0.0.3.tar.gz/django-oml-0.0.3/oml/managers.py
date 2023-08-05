from django.db import models


class ModeratedModelQuerySet(models.query.QuerySet):
    def main_queryset(self, status):
        return self.filter(status=status)


class ModeratedModelManager(models.Manager):
    def get_queryset(self):
        return ModeratedModelQuerySet(self.model, using=self._db)

    def accepted(self):
        return self.get_queryset().main_queryset(status='a')

    def rejected(self):
        return self.get_queryset().main_queryset(status='r')

    def pending(self):
        return self.get_queryset().main_queryset(status='p')
