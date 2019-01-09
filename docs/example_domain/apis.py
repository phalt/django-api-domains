import logging
import uuid
from typing import Dict  # noqa

import graphene
from graphene import ObjectType, relay

from .services import BookService

logger = logging.getLogger(__name__)


# Internal API
class BookAPI:

    @staticmethod
    def get(*, book_id: uuid.UUID) -> Dict:
        logger.info('method "get" called')
        return BookService.get_book(id=book_id)


# graphQL Entity
class BookEntity(ObjectType):
    class Meta:
        interfaces = (relay.Node,)
    name = graphene.String()
    author_name = graphene.String()


# graphQL mutation
class CreateBook(relay.ClientIDMutation):
    class Input:
        book_name = graphene.String(required=True)
        author_id = graphene.ID(required=True)

    book = graphene.Field(BookEntity)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        new_book = BookService.create_book(
            name=input.get('book_name'),
            author_id=input.get('author_id')
        )
        return BookEntity(
            name=new_book['name'],
            author_name=new_book['author_name'],
        )


# graphQL mutation
class UpdateBookAndAuthorName(relay.ClientIDMutation):
    class Input:
        book_name = graphene.String(required=True)
        author_name = graphene.String(required=True)
        author_id = graphene.ID(required=True)
        book_id = graphene.ID(required=True)

    book = graphene.Field(BookEntity)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        book = BookService.update_book_name_and_author_name(
            name=input.get('book_name'),
            id=input.get('book_id'),
            author_id=input.get('author_id'),
            author_name=input.get('author_name'),
        )
        return BookEntity(
            name=book['name'],
            author_name=book['author_name'],
        )


class Mutation:
    create_book = CreateBook.Field()


class Query:
    book = graphene.Field(BookEntity)

    def resolve_book(self, info):
        logger.info(f"graphQL query for book with id {info.get('id')}")
        book = BookService.get_book(id=info.get('id'))
        return BookEntity(
            name=book['name'],
            author_name=book['author_name'],
        )
