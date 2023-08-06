Before we start
===============

This documentation is a work-in-progres ... before anything I must warn the reader that I'm not a native English speaker, my apologies in advance for all mistakes.

Why Fanery
==========

Fanery is the result of several years struggling around a few basic questions:

- How to build Software that really fulfill end-users expectations?
- How to build Software that really scale?
- How to build Software that is really secure?
- How to build Software at scale that can be managed successfully by a very small team?

Answers came after years of experimentation and failures, but at the end a simple method emerged from chaos. That simple method of Software development is the reason Fanery exists the way it is.

Fulfill end-users expectations
------------------------------

There are infinites ways to build Software, but one easy and cost effective way to create understanding and agreement around a Software project is enlightning user's expectation with the aid of `Story Boards <http://en.wikipedia.org/wiki/Storyboard#Software>`_, sequences of pictures representing front-end interfaces and processes workflows through their interactions.

Once a Story Board get approved it means no misunderstanding still left about how the final product must look like and what it should do. Most important no single line of code is written at this stage, nor time is wasted choosing/arguing about which programming language, storage strategy, database engine, UI toolkit, operating system, etc, should be employed.

A team of interdiciplinary experts in the field of graphic design, human resources and psycology is recommended as usually end users don't know exactly what they want or have issues expressing/clarifying what they need.

Build Software that scale
-------------------------

Scalability is a difficult, a very tough problem to solve and deal with; no final answer exists however lots of clever solutions have been proposed and something many of them have in common is minimization of complexity.

Building Software architectures where logical elements are loosely coupled is a first step in that direction.

Fanery is designed around the idea that the following architecture is one flexible, valuable and real solution to the scalability problem and the framework should make very easy to build Software for it.

.. image:: images/scalable-architecture.png
    :align: center

The *Application Layer* is where the real *product* lives and the core point is:

    It should not care about front-end technologies or transport channels nor about storage strategies and database engines; it should just focus on the core business logic, processes and functionalities.

This simple idea unleash the freedom to switch at will all supporting pieces to our *product*, letting this way, load/stress-test different storage and indexing engines, UI toolkits, filesystems, messages queues, etc ... to consciously peak the bests for the job, taking decisions based on measurable and reproducible results.

Easy debugging, testing and profiling of every single line of written code is another important aspect of true scalability;

    Slow unoptimized sloppy code doesn't scale.

Build Software that is really secure
------------------------------------

Fanery approach to security is:

- Strong cryptography must be transparent and enabled by default.

    Building secure Software is hard, understanding cryptography is harder.

    Fanery pretend to provide transparent cryptography done correctly, trying hard to make it developer friendly (easy and unobtrusive).

- Encryption must not rely on cryptographic keys generated client side.

    Mistrust is a fundamental aspect of Software security, Fanery assume client-side cryptography is weak and for such reason all key-pairs must be generated exclusively server side by proper trong cryptographic primitives.

- Encryption must only rely on unbroken high-quality ciphers/algorithms/implementations.

    Fanery crypto strategy is build on top of ``NaCL``, ``scrypt`` and ``One-Time Pad``.

- Session security must not rely on SessionIDs, bizare URLs, secure cookies, secret tokens, magic keys or any other piece of information that can be guessed or stolen during transmission.

    Authentication and session security must stand even when security weakness are presents in SSL/TLS.

- Capture and re-transmission of encrypted messages must be pointless.

    Every encrypted message is unique and unforgeable, build with cryptographically secure random key-pairs and sign-keys that are destroyed after transmission.

- Transparent protection against brute-force and authenticated sessions abuse.

    Fight agains authentication abuse, message forging, unauthorized access, session hijacking, priviledge escalation, CSRF, MitM, etc.

- Transparent (de)serialization to harmless/built-in only object types.

    Automatic input/output (de)serialization help dramatically during development, avoiding boilerplates code and hacky constructs, but doing it correctly is not easy; Software development and frameworks have been historically plagued by critical security issues related to data (de)serialization.

- Carefull urlpaths validation and sanitization.

    Prevent directory traversal, file inclusion and similar attacks.

The described approach offer a solid fundation to build secure Software that stand against the majority of common attacks.

How to build Software at scale that can be managed successfully by a very small team?
-------------------------------------------------------------------------------------

If we forget about end-user support team for a moment and just focus on DevOps responsibility, a squeezed and over-simplified answer may be:

    Build Software on top of an hardened, massively scalable, almost zero configuration, shared-nothing architecture that can be fully understood by a single person.

That's a dreamed scenario, that may sound absurd or impossible to achieve, however it's not that crazy if we manage to remove all unecesary complexity from the full picture.

This guide pretend to show and explain one cost-effective way to build such architecture; of course there are many other ways, but just for a moment try to forget about current FUD, hype and greedy vendors *"best practice"*.

Disclaimer
----------

The choice of third-party FLOSS tools, programs and libraries is deliberately subjective, based on my personal experience and taste.

Every decision is always influenced by:

#. *Costs*: we are in a limited budget.
#. *Security*: security garanties must be preserved.
#. *Scalability*: the solution must be truly elastic.
#. *Flexibility*: every single piece should be replaced with easy.
#. *Easy of management*: a single person must be able to hadle it.
