from django.shortcuts import render


def chat_index(request, room_name):
    return render(request, 'chat/index.html', {'room_name': room_name})
