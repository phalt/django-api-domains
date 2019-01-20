import logging
import uuid
from typing import Dict, Str  # noqa

from .interfaces import AuthorInterface
from .models import Book

logger = logging.getLogger(__name__)


# Plain example
def get_book(*, id: uuid.UUID) -> Book:
    book = Book.objects.get(id=id)
    author = AuthorInterface.get_author(id=book.author_id)
    return {
        'name': book.name,
        'author_name': author.name,
    }


# Class example
class PGMNodeService:

    @staticmethod
    def get_book(*, id: uuid.UUID) -> Dict:
        book = Book.objects.get(id=id)
        author = AuthorInterface.get_author(id=book.author_id)
        return {
            'name': book.name,
            'author_name': author.name,
        }

    @staticmethod
    def create_book(*, name: Str, author_id: uuid.UUID) -> Dict:
        logger.info('Creating new book')
        new_book = Book.objects.create(name=name, author_id=author_id)
        author = AuthorInterface.get_author(id=new_book.author_id)
        return {
            'name': new_book.name,
            'author_name': author.name,
        }

    @staticmethod
    def update_book_name_and_author_name(
        *,
        name: Str,
        author_name: Str,
        author_id: uuid.UUID,
        id: uuid.UUID,
    ) -> Dict:
        logger.info('Updating book name and author name')
        book = Book.objects.get(id=id).update(name=name)
        author = AuthorInterface.update_author_name(
            name=author_name, id=author_id,
        )
        return {
            'name': book.name,
            'author_name': author.name,
        }
