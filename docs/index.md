# Django API Domains styleguide

This styleguide combines [domain-driven design](https://en.wikipedia.org/wiki/Domain-driven_design) principles and Django's [apps](https://docs.djangoproject.com/en/dev/ref/applications/#module-django.apps) pattern to provide a **pragmatic** guide for developing scalable API services with the Django web framework.

This styleguide tries to tackle two big problems:

1) Design philosophies and design patterns work in "ideal" situations, and most real life problems do not represent this ideal world. Therefore we need to develop a flexible pattern that can adjust to support different situations.
2) The original design and documentation of Django is geared heavily towards server-side-rendered-view applications, yet most modern Django applications are built to serve APIs for a separate frontend application. Therefore, Django's patterns are outdated for today's trends.

In order to overcome these problems, this styleguide tries to achieve the following five goals:

1) Treat Django's `apps` more like software `domains`.
2) Extend Django's `apps` implementation to support strong [bounded context](https://www.martinfowler.com/bliki/BoundedContext.html) patterns between `domains`.
3) Enable separation of domains to happen when it makes sense for **increased development velocity**, not just for **business value**.
4) Design a styleguide that reduces the effort involved in extracting the code for large domains into separate application servers.
5) Make sure the styleguide compliments API-based applications.