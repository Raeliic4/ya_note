# news/tests/test_content.py
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model

from notes.models import Note
from notes.forms import NoteForm
import sys

sys.path.insert(0, '/ya_notes')

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(title='Заголовок', text='Текст', slug='testnote', author=cls.author)

# В тесте используем фикстуру заметки
# и фикстуру клиента с автором заметки.
    def test_note_in_list_for_author(self):
        user = self.author
        self.client.force_login(user)
        url = reverse('notes:list')
    # Запрашиваем страницу со списком заметок:
        response = self.client.get(url)
    # Получаем список объектов из контекста:
        object_list = response.context['object_list']
    # Проверяем, что заметка находится в этом списке:
        self.assertIn(self.note, object_list)


# В этом тесте тоже используем фикстуру заметки,
# но в качестве клиента используем not_author_client;
# в этом клиенте авторизован не автор заметки, 
# так что заметка не должна быть ему видна.
    def test_note_not_in_list_for_another_user(self):
        user = self.reader
        self.client.force_login(user)
        url = reverse('notes:list')
    # Запрашиваем страницу со списком заметок:
        response = self.client.get(url)
    # Получаем список объектов из контекста:
        object_list = response.context['object_list']
    # Проверяем, что заметка находится в этом списке:
        self.assertNotIn(self.note, object_list)     

    def test_create_note_page_contains_form(self):
        url = reverse('notes:add')
        user = self.author
        self.client.force_login(user)
    # Запрашиваем страницу создания заметки:
        response = self.client.get(url)
    # Проверяем, есть ли объект form в словаре контекста:
        self.assertIn('form', response.context)
    # Проверяем, что объект формы относится к нужному классу.
        self.assertIsInstance(response.context['form'], NoteForm)


# В параметры теста передаём фикстуру slug_for_args и клиент с автором заметки:
    def test_edit_note_page_contains_form(self):
        url = reverse('notes:edit', args=(self.note.slug,))
    # Запрашиваем страницу редактирования заметки:
        user = self.author
        self.client.force_login(user)
    # Запрашиваем страницу создания заметки:
        response = self.client.get(url)
    # Проверяем, есть ли объект form в словаре контекста:
        self.assertIn('form', response.context)
    # Проверяем, что объект формы относится к нужному классу.
        self.assertIsInstance(response.context['form'], NoteForm)
