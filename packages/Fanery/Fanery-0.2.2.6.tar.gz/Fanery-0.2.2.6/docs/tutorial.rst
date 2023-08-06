Tutorial
========

This tutorial will show a very simple and contrived example of a simplified `TODO list` web application build with Fanery.

Before we start
---------------

We suppose the story board has been previously approved and the corresponding Web UI has already been coded.

Html, javascript, css and graphic files are teoretically stored inside a local ``static`` folder.

TODO list toy Web application
-----------------------------

`TODO list` application has really basic server side requirements, the full API is reduced to:

- ``get_all() -> [todo]``: retrieve all todos.
- ``add(text) -> todo``: add a new todo.
- ``update(todo) -> todo``: update an existing todo.
- ``remove(todo) -> bool``: remove an existing todo.

Every ``todo`` object is represented by a Json object with the following attributes:

- ``done``: boolean that define if todo is completed.
- ``text``: todo description.
- ``id``: todo unique id.
- ``vsn``: todo record version.

Additionally only authenticated users will be able to manage todos.

Consuming Fanery services with JavaScript
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First let's build a JavaScript proxy to consume Fanery services via asynchronous deferred Ajax calls.

    .. code:: javascript

        window.TodoApp = (function (F, E) {
            
            var self = this;

            self.get_all = function () {
                return F.safe_call('get_all');
            };

            self.add = function (text) {
                return F.safe_call('add', text);
            };

            self.update = function (todo) {
                return F.safe_call('update', todo);
            };

            self.remove = function (todo) {
                var params = {'id': todo.id, 'vsn': todo.vsn};
                return F.safe_call('remove', params);
            };

            self.login = function (username, password) {
                return F.login(username, password);
            };

            self.logout = function () {
                return F.logout();
            };

            E.InvalidCredential = function () {
                alert('Sorry, invalid username or password');
            };

            E.Unauthorized = function () {
                alert('Sorry, must login first');
            };

            E.Error = function () {
                alert('Sorry, an error occurred: ' + error.exc + '\n\n' + error.err.join('\n'));
            };

            return self;
        })(Fanery, Fanery.exc);

Server side TODO list setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^

During development is handy to have modules auto-reload which brings us many benefits in term of productivity.

Create a todoapp/_config.py file as follow:

    .. code:: python

        from fanery import config

        # enable auto-reload
        config.IS_DEVELOPMENT = True

        # the folder where static files lives (html, css, javascripts, etc)
        STATIC_DIR = 'static'

It's important not to forgive that setting ``IS_DEVELOPMENT`` to ``True`` disable default behaviour to force SSL, the reason for such decision is to let start quickly producing/testing/profiling code without requiring first the difficult and time consuming job of properly creating certificates and setting up a caching web reverse proxy.

Production code must always leave ``IS_DEVELOPMENT`` set to default ``False`` value, not only to enforce SSL usage, also because having modules auto-reload in production environment is a very bad idea.

Models definition file todoapp/_models.py may look like this:

    .. code:: python

        from fanery import Hict

        class Todo:

            @classmethod
            def initialize(cls, record):
                record.merge(done=False, text='')

            @classmethod
            def validate(cls, record):
                errors = Hict()

                text = record.text
                if not isinstance(text, basestring):
                    errors.text.bad_type = type(text).__name__
                elif not text.strip():
                    errors.text.invalid = text

                done = record.done
                if not isinstance(done, bool):
                    errors.done.bad_type = type(done).__name__

                return errors

            @classmethod
            def index(cls, record):
                return dict(done=record.done, text=record.text)

            @classmethod
            def to_dict(cls, record):
                return dict(done=record.done, text=record.text,
                            id=record._uuid, vsn=record._vsn)

It's sane to always perform server-side data validations and never trust input sent by our users. Validation in the front-end is also a good idea but we can't rely on it.

Following the idea that storage strategy should be our last concern, we'll start using a toy proxy implementation already provided with Fanery.

Setup file todoapp/_setup.py take care of it:

    .. code:: python
           
        from fanery import DataStore, dbm, auth, add_model, add_storage
        from _models import Todo

        db = dbm.MemDictStore()
        storage = DataStore(db, permission=db,
                                state=db,
                                abuse=db,
                                profile=db,
                                settings=db)

        add_model(Todo)
        add_storage(storage, Todo)

        auth.setup(storage)
        auth.add_user('MY-USER', 'MY-SECRET', domain='MY-DOMAIN')

Fanery is build with the idea that applications should be multi-tenant, transparent multi-tenancy is achived via domains abstraction, in other words, ``state`` and ``Record`` objects belongs to a specific ``domain`` which define the tenancy space.

``MemDictStore`` is a toy in-memory datastore implementation that define all required hooks necessary to support Fanery ``storage`` facility, its purpose is only to get started with a storage strategy that let experiment with data models during early development stage, until a proper and production ready stategy is choosen.

Application business logic may be defined inside todoapp/_api.py file as follow:

    .. code:: python

        from fanery import service, storage
        from _models import Todo

        @service()
        def get_all():
            with storage() as db:
                return map(Todo.to_dict, db.select(Todo))

        @service(auto_parse=False)
        def add(text):
            with storage() as db:
                record = db.insert(Todo, text=text)
            return Todo.to_dict(record)

        @service(auto_parse=False)
        def update(id, vsn, text, done):
            with storage() as db:
                record = db.fetch(Todo, id, vsn)
                record.text = text
                record.done = done
                db.update(record)
                # or just
                # record = db.update(Todo, id, vsn, text=text, done=done)
            return Todo.to_dict(record)

        @service()
        def remove(id, vsn):
            with storage() as db:
                record = db.fetch(Todo, id, vsn)
                db.delete(record)
                # or just
                # db.delete(Todo, id, vsn)
            return True

What's left is starting our ``TODO list`` behind some ``WSGI`` capable application server.

For development purpose start_server.py will do:

    .. code:: python
    
        from fanery import server, static
        from todoapp import config

        static('/', config.STATIC_DIR)

        server.start_wsgi_server()

Make todoapp directory a Python module:

    .. code:: bash

        cat > todoapp/__init__.py <<EOF
        import _config as config
        import _models as models
        import _api as api
        import _setup
        EOF

Finally start TODO list Web application.

    .. code:: bash

        PYTHONPATH=. python start_server.py

The way our ``TodoApp`` ajax proxy may be used to consume todoapp API should be clarified by the following JavaScript sniplet:

    .. code:: javascript

        // login first
        TodoApp.login("MY-USER", "MY-SECRET").then(function () {

            // create your first todo
            TodoApp.add("Play with Fanery").then(function (todo) {

                // verify got stored
                TodoApp.get_all().then(function (data) {
                    if (data.length != 1) alert("invalid length");
                    if (data[0].id != todo.id) alert("unexpected id");
                    if (todo.done || data[1].done) alert("should not be done");

                    // update todo
                    todo.done = true;

                    // verify got updated
                    TodoApp.update(todo).then(function (updated) {
                        if (todo.id != updated.id) alert("id mismatch");
                        if (todo.vsn != (updated.vsn - 1)) alert("unexpected version");
                        if (todo.text != updated.text) alert("text mismatch");
                        if (!updated.done) alert("should be done");

                        // remove updated todo
                        TodoApp.remove(updated).then(function (success) {
                            if (!success) alert("couldn't remove updated todo");

                            // verify no more todo available
                            TodoApp.get_all().then(function (data) {
                                if (data.length > 0) alert("should be no more todos left");

                                // logout
                                TodoApp.logout().then(function () {

                                    // no anonymous access 1
                                    TodoApp.get_all();

                                    // no anonymous access 2
                                    Fanery.safe_call("get_all");

                                    // no anonymous access 3 (detected as abusive behaviour)
                                    Fanery.call("/get_all.json");

                                    // no anonymous access 4 (detected as abusive behaviour)
                                    jQuery.get("/get_all.json");

                                    // repeate the last 2 calls a few more times and you won't be able to login anymore
                                });
                            });
                        });
                    });
                });
            });
        });
