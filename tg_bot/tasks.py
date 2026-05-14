from celery import shared_task
from django.utils import timezone
from habits.models import Habit
from tg_bot.bot import send_telegram_message


@shared_task
def send_habit_reminders():
    now = timezone.now()
    current_time = now.time()
    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute,
        is_pleasant=False,
        user__telegram_chat_id__isnull=False
    )
    for habit in habits:
        chat_id = habit.user.telegram_chat_id
        message = f'Напоминание: {habit.action} в {habit.place} в {habit.time} (займёт {habit.duration} сек)'
        send_telegram_message(chat_id, message)
