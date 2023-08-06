Working with Fanery
===================

Fanery is a framework build by developers for developers.

Opinionated frameworks usually takes uncommon and controversial paths you may disagree with, that's why before starting to work with Fanery it's fundamental to understand the intrinsics ideas that give birth to the tool as it is:

- Strong security by default.
- Focus on being developer-oriented.
- Promote funcional pythonic style.
- Promote continuous testing+profiling.

This section is dedicated to make sense of that 4 ideas in the context of Web Software Development with Fanery Framework.

Strong security by default
--------------------------

Simplicity is key to growth and manageability of Software projects, however isn't uncommon that development frameworks get in your way during the process.

Fanery services, which are just remotely callable functions, let safely expose functionalities unobtrusively via ``@service`` decorator.

Let briefly look at two simple services, a public anonymously callable and another one that require authenticated encrypted connection.

Public anonymous service
^^^^^^^^^^^^^^^^^^^^^^^^

Public anonymous exposed functions do not comply to Fanery security protocol, but as Fanery enable strong security by default it's necessary to decorate our service explicitly to be anonymous:

    .. code:: python

        from fanery import service

        @service(safe=False, ssl=False, auto_parse=False, cache=True)
        def hello(name='World'):
            return "Hello, %s!" % name

By default call's arguments are auto-parsed to built-in/harmless data types. In this case ``hello`` service explicitly disable it.

Caching control through ``pragma``, ``cache-control`` and ``expires`` headers can be enabled setting ``cache`` argument to ``True`` or a positive value representing cache expiration in seconds (default to ``False``).

Additionally ``hello`` service may be called over unsecure ``HTTP`` connections; by default only ``SSL/TLS`` encrypted calls are accepted.

Disabling ``safe`` argument tells Fanery not to trigger session's security checks.

Secure authenticated service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Our service ``profile_data`` just return some personal information about the current session user.

    .. code:: python

        from fanery import service, get_state

        @service()
        def profile_data():
            profile = get_state().profile
            return dict(name=profile.username,
                        email=profile.email,
                        role=profile.role)

The use of ``@service()`` without arguments imply ``@service(safe=True, ssl=True, cache=False)`` which means our exposed function ``profile_data()`` can be called only if the following conditions are honored:

- Calls must travel inside encrypted SSL/TLS channel.
- A valid/active authenticated session exists.
- Remote call goes through Fanery security protocol (``NaCL`` + ``One-Time pad``).

Fanery framework comes with all required JavaScript functionalities to perform such type of secure Ajax calls.

Safe Ajax calls are asynchronous and deferred:

    .. code:: javascript

        Fanery.safe_call('profile_data').then(console.log).fail(console.error);
        Fanery.safe_call('profile_data.json').always(console.debug);

In both cases all data between the client and server is secured and (de)serialized automatically to ``JSON``.

All required JavaScript codes and third party libraries are mapped by default behind ``jfanery/`` urlpath:

    .. code:: html

        <!-- third party FLOSS libraries jfanery depends on -->
        <script src="jfanery/nacl_factory.js"></script>
        <script src="jfanery/scrypt.js"></script>
        <script src="jfanery/base64.js"></script>

        <!-- fanery security protocol implementation -->
        <script src="jfanery/jfanery.js"></script>

Unobtrusiveness is reflected in the following principles:

    ``profile_data`` know nothing and should not care about protocols (``HTTP/S``, ``WSGI``), serialization formats (``JSON``), encryption (``NaCL``, ``One-Time pad``), session abuse (``bruteforce``, ``hijacking``, ``MitM``, ``CSRF``) nor anything outside Python and the job it's supposed to perform.

Staying focused on the job to perform without wasting precious resources thinking about the external environment is fundamental to reduce complexity.

Focus on being developer-oriented
---------------------------------

Fanery doesn't try or pretend to define `"best pratice"` about Software development. Every developer has his own style and the tool shouldn't impose boundaries, for such reason the following principles are respected:

- The framework must not depend on strict/pre-defined configuration style/format and/or directory structure.
- The framework must not tie to a particular storage or UI technology.
- The framework must provide the facilities for easy testing, debugging and profiling.
- The framework must not rely on components that inhibit elastic/horizontal scalability.

At this point must be clear that Fanery set apart from most commons Web development frameworks; indeed it's been build in compliance to the following `"unpopular"` ideas:

- Storage strategy should be the last concern during Software development.
- End-user interfaces should not be generated server-side.
- Funcional development style is superior to Object Oriented.
- Premature optimization may be evil but early optimization is prerequisite to Software quality.
- Security must not be compromised in favor to obsolete/legacy systems compatibility nor performance.

Promote functional pythonic style
---------------------------------

Functional pythonic style here refer to the practice of building Software around a collection of functions organized and named accordingly to their being, the practice of using data as pure data, rejecting the idea of black boxes with inner state and personalized behaviours as proposed by Object Orientation.

Fanery itself is build following such principle, classes are seldom choosen as building blocks, only when it make sense in a pythonic style.

Specific classes used by Fanery are:

- ``Hict``: dotted hierarchical dictionary.
- ``Aict``: dotted hierarchical dictionary with terms auto-parsing.
- ``DataStore``: store strategy proxy, a glue between all containers representing the `Elastic Backend storage` layer seen in our introductory setion.
- ``Record``: versioned model-aware data container.
- ``store``: abstraction built to handle all storage activities as a single unit of work inside a ``with`` statement.

Fanery data types, decorators, functions library and abstraction helpers aid developers in their quest to elegant, scalable and high available Software solutions.

Promote continuous testing+profiling
------------------------------------

Software development is a process, a never ending quest to maturity, perfection and mankind knowledge growth; in such spirit maturity and knowledge come from experimentation and understanding after each mistake/achievement:

    `What's measurable and replicable has a really good chance to be improoved.`

This corollary stone of science is intrinsics to Software production, that's why testing and profiling must be a fundamental gear inside development machinery.

Fanery try to shorten the path required to apply testing and profiling practice to the process, providing easy access to venerable third party libraries like:

- ``memory-profiler``: line-by-line memory usage.
- ``line-profiler``: line-by-line execution performance.
- ``profile-hooks``: code coverage and functions execution timing.
- ``linesman``: wsgi middleware able to build execution stack performance metrics and graphs.
- ``ipdb``: Python debugger on steroids.
- ``rpdb2``: remote Python debugger.

Software testing and profiling is fundamental to garantee quality, it should be done early and iteratively; I'm not advocating one or another testing methodology here, just use the one you feel more confortable with, the one that fit best in your development process.

Another Python project that deserve great mention is ``pyrasite``, it let for injection of arbitrary code into running Python process and integrate nicely with ``meliae``, ``pycallgraph`` and ``psutil``.

Software Performance Testing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Knowing your Software works correctly is not enough, customers have expectations that should be fulfilled, that means our Software must be load/stress tested through each architecture layers to guarantee the required level of robustness and availability.

Several tools exists for the job, some that deserve attentions are:

- multi-mechanize, funkload, locust.io: load/stress testing of Web applications.
- munin: hardware, network, system and application resource monitoring.
- bucky: web page rendering performance and timing.
- sentry, graylog2: centralized logging and events correlation.

TODO: add hyperlinks to projects pages
