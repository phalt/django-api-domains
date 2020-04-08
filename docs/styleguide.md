## Visualisation

![diagrams/dads_main.png](https://raw.githubusercontent.com/phalt/django-api-domains/master/diagrams/dads_main.png)

## File structure

* A domain **must** use the following file structure:

```
- apis.py - Public functions and access points, presentation logic.
- interfaces.py - Integrations with other domains or external services.
- models.py - Object models and storage, simple information logic.
- services.py - coordination and transactional logic.
```

In addition, any existing files from a standard Django app are still allowed, such as `urls.py`, `apps.py` and `migrations/*`.

* `Views.py` in [Django's pattern](https://docs.djangoproject.com/en/dev/#the-view-layer) is **explicitly not allowed** in this styleguide.

We only focus on API-based applications. Most logic that used to live in Django's `views.py` would now be separated into APIs and Services.

* You **can** mask one of the required files as a directory for better file organisation. For example, you might want to split `apis.py` file into this structure:

```
apis/
  __init__.py
  rest.py
  graphql.py
```

Your `__init__.py` file in this directory can import the local files:

```python
# apis/__init__.py
from .rest import *  # noqa
from .graphql import *  # noqa
```

Then, any other file can import from apis like so:

```python
# example.py
from domain.apis import Foo
```

This keeps namespaces tidy and does not leak domain details.

* A domain **does not** need to have all these files if it is not using them. For example - a domain that just coordinates API calls to other domains does not need to have Models as it is probably not storing anything in a datastore.

* A domain **can have** additional files when it makes sense (such as `utils.py` or `enums.py` or `serializers.py`) to separate out parts of the code that aren't covered by the styleguide pattern.

Read more about the files in the [files](/files) section.

## Absolute or Relative imports?

The ruling for absolute or relative imports is as follows:

* When importing files within a domain, you **must** use relative imports.
* When importing other domains in the same project, you **must** use absolute imports.
* When importing domains in tests, you **should** use absolute imports.
* When importing third-party packages you **should** use absolute imports.

TL;DR - relative imports inside a domain, absolute for everything else!

With this ruling domains are easy to package and move around. When it comes time to move it into it's own project; tidying up imports will be one less thing you have to do.

## Which logic lives where?

It's common in programming to end up confused about what type of logic should live where.

There are many cases where it's difficult to decide, and the best advice is to **pick a pattern and stick to it**, but for simpler things, this guide emphasises the following:

### APIs
Logic about presentation.

---

> **If you ask:**
> "Where should I show this data to the user?" or "Where do I define the API schema?"

---


### Services
Logic around coordination and transactions.

---

> **If you ask:**
> "Where do I coordinate updating many models in one domain?" or "Where do I dispatch a single action out to other domains?"

---


### Models
Logic around information.

---

> **If you ask:**
> "Where can I store this data?" or  "Where can I do any post/pre-save actions?"

---


### Interfaces

Logic for handling the transformation of data from other domains.

---

> **If you ask:**
> "Where shall I connect to another domain?" or "How do I change the data format for another domain?"

---
