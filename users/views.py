from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions


class SetTelegramChatIdView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        chat_id = request.data.get('chat_id')
        if chat_id:
            request.user.telegram_chat_id = chat_id
            request.user.save()
            return Response({'status': 'ok'})
        return Response({'error': 'chat_id required'}, status=400)
