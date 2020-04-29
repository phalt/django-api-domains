
### Examples on this page

In the examples below we imagine a service with two domains - one for books, and one for authors. The abstraction between books and authors is only present to demonstrate the concepts in the styleguide. You could argue that Books and Authors can live in one domain. In our example **we also assume that a book can only have one author.** It's a strange world.

## Models

_Models_ defines how a data model / database table looks. This is a Django convention that remains mostly unchanged. The key difference here is that you use _skinny models_. No complex functional logic should live here.

In the past Django has recommended an [active record](https://docs.djangoproject.com/en/2.1/misc/design-philosophies/#models) style for its models. In practice, we have found that this encourages developers to bloat `models.py`, making it do too much and often binding the presentation and functional logic of a domain too tightly. This makes it very hard to have abstract presentations of the data in a domain. Putting all the logic in one place also makes it difficult to scale the number of developers working in this part of the codebase. See the [_"Which logic lives where?"_](/styleguide/#which-logic-lives-where) section for clarification.

A models.py file can look like:

```python
import uuid
from django.db import models


class Book(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=256)
    publisher = models.CharField(max_length=256)
    author_id = models.UUIDField(default=uuid.uuid4)

    @property
    def name_and_publisher(self):
        return f'{self.name}, {self.publisher}'

```

- Models **must not** have any complex functional logic in them.
- Models **should** own informational logic related to them.
- Models **can** have computed properties where it makes sense.
- Models **must not** import services, interfaces, or apis from their own domain or other domains.
- Table dependencies (such as ForeignKeys) **must not** exist across domains. Use a UUID field instead, and have your Services control the relationship between models.
- You **can** use ForeignKeys between tables in one domain. (But be aware that this might hinder future refactoring.)


## APIs

_APIs_ defines the external API interface for your domain. Anyone using the APIs defined here is called a _consumer_. The API can be either an HTTP API using [GraphQL](https://github.com/graphql-python) or [REST](https://www.django-rest-framework.org/) for consumers over the web, or a software API for internal consumers. APIs is defined in `apis.py` which is agnostic to the implementation you choose, you can even put more than one API in a domain. For example - you might want to wrap a GraphQL API _and_ a REST API around your domain for different consumers.

An `apis.py` file that defines a simple software API can look like:

```python
import logging
import uuid
from typing import Dict  # noqa

from .services import BookService

logger = logging.getLogger(__name__)


class BookAPI:

    @staticmethod
    def get(*, book_id: uuid.UUID) -> Dict:
        logger.info('method "get" called')
        return BookService.get_book(id=book_id)

```

- APIs **must be** used as the entry point for all other consumers who wish to use this domain.
- APIs **should** own presentational logic and schema declarations.
- Internal domain-to-domain APIs **should** just be functions.
- You **can** group internal API functions under a class if it makes sense for organisation.
- If you are using a class for your internal APIs, it **must** use the naming convention `MyDomainAPI`.
- Internal functions in APIs **must** use type annotations.
- Internal functions in APIs **must** use keyword arguments.
- You **should** log API function calls.
- All data returned from APIs **must be** serializable.
- APIs **must** talk to Services to get data.
- APIs **must not** talk to Models directly.
- APIs **should** do simple logic like transforming data for the outside world, or taking external data and transforming it for the domain to understand.
- Objects represented through APIs **do not** have to map directly to internal database representations of data.


## Interfaces

Your domain may need to communicate with another domain. That domain can be in another web server across the web, or it could be within the same server. It could even be a third-party service. When your domain needs to talk to other domains, you should define **all interactions to the other domain in the `interfaces.py` file**. Combined with APIs (see above), this forms the bounded context of the domain and prevents domain logic from leaking in.

Consider `interfaces.py` like a mini _Anti-Corruption Layer_. Most of the time it won't change and it'll just pass on arguments to an API function. But when the other domain moves - say you extract it into its own web service, your domain only needs to update the code in `interfaces.py` to reflect the change. No complex refactoring needed, woohoo!

It's worth noting that some guides would consider this implementation a 'code smell' because it has the potential for creating shallow methods or pass-through methods. This is somewhat true, and leads us back to the [pragmatism](/django-api-domains/using/#be-pragmatic) point in our guide. If you find your `interfaces.py` is redundant, then you probably don't need it. That said: **we recommend starting with it and removing it later**.

An `interfaces.py` may look like:

```python
import uuid
from typing import Dict, Str  # noqa

# Could be an internal domain or an HTTP API client - we don't care!
from src.authors.apis import AuthorAPI


# plain example
def update_author_name(*, author_name: Str, author_id: uuid.UUID) -> None:
    AuthorAPI.update_author_name(
        id=author_id,
        name=author_name,
    )


# class example
class AuthorInterface:

    @staticmethod
    def get_author(*, id: uuid.UUID) -> Dict:
        return AuthorAPI.get(id=id)

    @staticmethod
    def update_author_name(
      *,
      author_name: Str,
      author_id: uuid.UUID,
    ) -> None:
        AuthorAPI.update_author_name(
            id=author_id,
            name=author_name,
        )

```

- The primary components of Interfaces **should** be functions.
- You **can** group functions under a class if it makes sense for organisation.
- If you are using a class, it **must** use the naming convention `MyDomainInterface`.
- Functions in Interfaces **must** use type annotations.
- Functions in Interfaces **must** use keyword arguments.

## Services

Everything in a domain comes together in Services.

_Services_ gather all the business value for this domain. What type of logic should live here? Here are a few examples:

- When creating a new instance of a model, we need to compute a field on it before saving.
- When querying some content, we need to collect it from a few different places and gather it together in a python object.
- When deleting an instance we need to send a signal to another domain so it can do it's own logic.

Anything that is specific to the domain problem and **not** basic informational logic should live in Services. As most API projects expose single functional actions such as Create, Read, Update, and Delete, _Services_ has been designed specifically to compliment stateless, single-action functions.

A `services.py` file could look like:

```python
import logging
import uuid
from typing import Dict, Str  # noqa

from .interfaces import AuthorInterface
from .models import Book

logger = logging.getLogger(__name__)


# Plain example
def get_book(*, id: uuid.UUID) -> Dict:
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

```

- The primary components of Services **should** be functions.
- Services **should** own co-ordination and transactional logic.
- You **can** group functions under a class if it makes sense for organisation.
- If you are using a class, it **must** use the naming convention `MyDomainService`.
- Functions in services.py **must** use type annotations.
- Functions in services.py **must** use keyword arguments.
- You **should** be logging in `services.py`.
