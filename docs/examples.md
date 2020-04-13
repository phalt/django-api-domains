## Two domains

Let's start with a basic example - a project that has two domains. They both expose APIs for a Frontend service, and they also communicate to each other.
Communicating to the Frontend service is simple - they have defined a REST API in their API layer and the Frontend calls it.

When talking to each other, they both _interface_ (hence the naming choice) with each other through the appropriate layers. Sometimes we call this the "API to interface path".

Let's imagine that the owners of Domain B decide they want to move their software into another web server on the other side of the world. The first thing they might do is make a copy of the software of Domain B. They might spin that copy up in the new world, and slowly port the data over from the old Domain B.

During this time, Domain A is still talking to the old Domain B. When the new Domain B is ready to go, they inform the team that owns Domain A. The Domain A team will then update their interfaces.py to point to the new Domain B instance. Because they have not leaked Domain B's logic throughout Domain A, the change is isolated to a single file (and hopefully a single git commit).

![two-domains](https://raw.githubusercontent.com/phalt/django-api-domains/master/diagrams/two_dads.png)

More examples to come in the future.