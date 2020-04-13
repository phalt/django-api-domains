# Domains

A [domain](https://en.wikipedia.org/wiki/Domain_(software_engineering)) is a piece of software that provides a distinct **business** value for your application.

What this styleguide calls a `domain` is roughly an extension of what Django would call an `app`. Therefore a business domain **should** have at least one distinct software domain mirroring it.

---

> ### Examples in this guide

> The examples in this guide will talk about a `book shop` that shares details about books.
> This can be modelled as a _business domain_ called `books`, and as a _software domain_ also called `books`.

---

This guide tries to keep the key benefits of Django's `app` pattern - namely Django's [models](https://docs.djangoproject.com/en/2.1/topics/db/models/) to represent tables in a datastore, but with an emphasis on **skinny models**.

This guide also retains Django's ability to *package apps as installable components in other applications*. This allows domains to be easily migrated to different codebases or completely different projects.

## Domain rules

There are two major rules around domains:

1. You **should** split a domain if it becomes too big to work on.

    A domain should allow between 4-6 developers (3 pairs) to comfortably work on it. If you find your developers being blocked by each other then it is time to consider splitting the domain or checking whether the software has not diverged too far from the styleguide.

---

2. You **should** adhere to the styleguide patterns in this document in order to maintain strong bounded contexts between your domains.

    This applies even in situations where you extract one domain into two domains to increase velocity, but they still have to maintain a dependency between one another. We have found that if you relax the bounded context between domains, the boundary will erode and you will lose the ability to work on them independent of each other.


---

> ### Protip
> An example _software_ domain is provided in the same directory as this styleguide under [example_domain/](https://github.com/phalt/django-api-domains/tree/master/example_domain).

---

Next, we will discuss the styleguide in detail.
