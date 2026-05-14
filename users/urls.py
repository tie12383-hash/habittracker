from django.urls import path
from users.views import SetTelegramChatIdView

urlpatterns = [
    path('set_telegram_id/', SetTelegramChatIdView.as_view(), name='set-telegram-id'),
]
