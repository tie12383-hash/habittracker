from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=200, verbose_name='Место')
    time = models.TimeField(verbose_name='Время выполнения')
    action = models.CharField(max_length=200, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False,
                                      verbose_name='Признак приятной привычки')
    related_habit = models.ForeignKey('self',
                                      on_delete=models.SET_NULL,
                                      null=True, blank=True, verbose_name='Связанная привычка')
    periodicity = models.PositiveIntegerField(default=1,
                                              verbose_name='Периодичность (дни)', help_text='Не реже 1 раза в 7 дней')
    reward = models.CharField(max_length=200, blank=True, null=True, verbose_name='Вознаграждение')
    duration = models.PositiveIntegerField(verbose_name='Время на выполнение (сек)', help_text='Не больше 120 секунд')
    is_public = models.BooleanField(default=False, verbose_name='Публичная')

    class Meta:
        ordering = ['-id']

    def clean(self):
        # Время выполнения не больше 120 секунд
        if self.duration > 120:
            raise ValidationError({'duration': 'Время выполнения не должно превышать 120 секунд'})

        # Нельзя одновременно заполнять вознаграждение и связанную привычку
        if self.reward and self.related_habit:
            raise ValidationError('Нельзя указывать одновременно вознаграждение и связанную привычку')

        # У приятной привычки не может быть вознаграждения или связанной привычки
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки')

        # Связанная привычка может быть только приятной
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError('Связанная привычка должна быть приятной')

        # Периодичность не реже 1 раза в 7 дней
        if self.periodicity < 1 or self.periodicity > 7:
            raise ValidationError({'periodicity': 'Периодичность должна быть от 1 до 7 дней'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.action} в {self.time} в {self.place}'
