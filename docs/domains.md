# Domains

A [domain](https://en.wikipedia.org/wiki/Domain_(software_engineering)) is a piece of software that provides distinct business value within the context of your application.

Within the context of software, what this styleguide calls a `domain` is roughly an extension of what Django would call an `app`. Therefore a _business_ domain **should** have at least one distinct _software_ domain mirroring it.

## Examples in this guide

The examples in this guide will talk about a `book shop` that must share details about books. This can be modelled as a _domain_ called `books`, and as a _software domain_ also called `books`.

We keep the key benefits of Django's `app` pattern - namely Django's [models](https://docs.djangoproject.com/en/2.1/topics/db/models/) to represent tables in a datastore, with an emphasis on **skinny models**. We also retain Django's ability to *package apps as installable components in other applications*. This allows domains to be easily migrated to different codebases or completely different projects.

## Domain rules

There are two high-level rules around domains:

1. You **should** split a domain if it becomes too big to work on.

As a rule of thumb is that a domain should allow between 4-6 developers (3 pairs) to comfortably work on it. If you find your developers being blocked by each other then it is time to consider splitting the domain or checking the software has not diverged too far from the styleguide.

2. You **should** adhere to the styleguide patterns in this document in order to maintain strong bounded contexts between your domains.

This applies even in situations where you extract one domain into two domains to increase velocity, but they still have to maintain a dependency between each other. We have found that if you relax the bounded context between domains, the boundary will erode and you will lose the ability to work on them independent of each other.

An example _software_ domain is provided in the same directory as this styleguide under [example_domain/](https://github.com/phalt/django-api-domains/tree/master/example_domain).

Next, we will discuss the styleguide in detail.