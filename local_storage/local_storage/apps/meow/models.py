from django.db import models

class MeowModel(models.Model):
    meow_task = models.TextField(verbose_name='task')

    def __str__(self) -> str:
        return f'task: {self.meow_task}'