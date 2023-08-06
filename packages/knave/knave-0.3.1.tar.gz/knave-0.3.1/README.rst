Knave: a library for authorization in WSGI apps
===============================================


Knave is similar in design and scope to repoze.what.

Knave does not depend on any particular authentication package (it works well
with `repoze.who`_, but should work equally well with any authentication
mechanism)


Configuration
-------------

To start using knave, you need to define roles and permissions::

    from knave.acl import Role, Permission, ACL
    from knave.roles import StaticRoleProvider

    class Permissions:

        #: Can manage user accounts
        USER_MANAGE = Permission('user_manage')

        #: Can author articles
        ARTICLE_CREATE = Permission('article_create')

        #: Can publish articles
        ARTICLE_PUBLISH = Permission('article_publish')

    class Roles:

        ADMINS = Role('admins')
        EDITORS = Role('editors')

Then you can map permissions to the roles that should be authorized for them::

    role_permssions = {
        Permissions.USER_MANAGE: {Roles.ADMINS},
        Permissions.ARTICLE_CREATE: {Roles.ADMINS, Roles.EDITORS},
        Permissions.ARTICLE_PUBLISH: {Roles.ADMINS, Roles.EDITORS},
    }


Finally, you need to tell knave which users belong to which roles. The
demonstration purposes we've used a static mapping of user names to roles::

    role_provider = StaticRoleProvider({
        'spike': {Roles.ADMINS},
        'harry': {Roles.EDITORS}
    })

You can subclass ``knave.roles.RoleProvider`` to look up role membership from
a dynamic source such as a database.

With everything defined, you can link all this together in an ACL::

    acl = ACL([role_provider], role_permssions)

Once you have created an acl,
you can use its ``role_provider`` method to add
more RoleProviders using a class decorator syntax::

    @acl.role_provider
    class MyRoleProvider(RoleProvider):

        def member_subset(self, roles, identity, context=None):
            ...

If your role provider acts on a single role,
you can also supply this as role
as an argument to ``ACL.role_provider``
and use it to decorate a function returning a boolean value::

    owner_role = Role('owner')

    @acl.role_provider(owner_role)
    def is_owner(identity, context):
        return context and context.author == identity


WSGI Middleware
---------------

You should use ``knave.middleware.KnaveMiddleware``
to link the ACL into your WSGI application::

    from knave import KnaveMiddleware

    app = KnaveMiddleware(app, acl)

This middleware makes it possible
for your app to access the ACL
from within a WSGI request, eg::

    def wsgi_app(environ, start_response):
        ...

        if ACL.of(environ).test(Permissions.USER_MANAGE):
            ...


The middleware also takes care of
catching any ``knave.predicates.Unauthorized`` exceptions
and returning an HTTP 401 response instead.

Integrating with an authentication system
-----------------------------------------

By default knave looks at the WSGI environ ``REMOTE_USER`` key to retrieve the
identity of the current user.

You can change this behaviour
by supplying a different ``identity_adapter``
when configuring your ACL.

If you are using `repoze.who`_,
there is a built in adapter for this::

    import knave.identity
    acl = ACL(..., identity_adapter=knave.identity.RepozeWhoIdentityAdapter())

If you have a custom authentication layer,
you may need to write your own IdentityAdapter.
Here's an example for an authentication system
where the user id is saved in the session (using beaker_ sessions)::

    from knave.identity import IdentityAdapter

    class SessionIdentityAdapter(IdentityAdapter):
        """
        Extract the user identity from the current session
        """
        def __call__(self, environ):
            return environ['beaker.session'].get('current_user')

    ...

    acl = ACL(..., identity_adapter=SessionIdentityAdapter())

Checking permissions
--------------------

From your WSGI application you can call ``ACL.of(environ).test(...)``
to test a permission::

    if not ACL.of(environ).test(Permissions.USER_MANAGE):
        start_response('401 Unauthorized', [('Content-Type', 'text/html')]
        return ['<h1>Sorry, you're not authorized to view this page</h1>']

Or you can call ``ACL.of(environ).require(...)`` to test the permission and
raise an unauthorized exception if it isn't met:

    ACL.of(environ).require(Permissions.USER_MANAGE)

``knave.middleware.KnaveMiddleware`` will trap this exception and
return an appropriate WSGI response.

Contextual roles and fancy permissions checks
`````````````````````````````````````````````

All checks support an optional ``context`` argument. You can use this to add
roles dynamically.

For example, suppose you have a blogging application that creates ``BlogEntry``
objects, which have an ``author`` attribute.

You can define a owner role and have it set dynamically so that only the
BlogEntry author has the role::

    class Permissions:
        ARTICLE_EDIT = Permission('article_edit')

    class Roles:
        OWNER = Role('owner')
        ADMIN = Role('admin')

    role_permssions = {
        Permissions.ARTICLE_EDIT: {Roles.ADMIN, Roles.OWNER},
    }
    role_provider = StaticRoleProvider({
        'spike': {Roles.ADMIN}
    })

    class OwnerRoleProvider(RoleProvider):
        "A role provider to tell the ACL when the user has the owner role"

        contextual = True
        determines = {Roles.OWNER}

        def member_subset(self, roles, identity, context=None):

            if context is None or Roles.OWNER not in roles:
                return set()

            if getattr(context, 'author', None) == identity:
                return set(Roles.OWNER)

            return set()

    acl = ACL([StaticRoleProvider, OwnerRoleProvider], role_permssions)

Your application code would then need to pass the article object to the
permissions check::

    blogentry = store.get(BlogEntry, id=request.get('id'))
    ACL.of(environ).test(Permissions.ARTICLE_EDIT, context=blogentry)

Note also the ``contextual = True`` and ``determines = {...}``
lines in the OwnerRoleProvider class.
These are optimization hints,
telling the system not to bother querying the RoleProvider
unless a context object is provided and one of the listed roles
is present in the query.
You can safely omit these lines,
in which case your RoleProvider will be called for every lookup.
Note RoleProviders can be called directly,
in which case these hints are ignored.
Your ``member_subset`` logic should still account for cases
where ``context`` is None, or where it is queried for other roles.

If you want to check for a single role,
the ``@role_decider`` decorator
is a convenient shortcut.
The ``OwnerRoleProvider`` might have been more concisely written as::

    from knave.roles import role_decider

    @role_decider(Roles.OWNER, contextual=True)
    def is_owner(identity, context=None):
        return context and getattr(context, 'author', None) == identity


Permissions can also implement custom checking logic, for example::

    class DaytimePermission(Permission):
        """
        Only allow access during daytime working hours
        """

        def __call__(self, acl, identity, context=None):
            from datetime import datetime
            return (9 <= datetime.now().hour < 5)



Custom unauthorized responses
-----------------------------

By default ``KnaveMiddleware`` returns a minimal HTTP
``401 Not Authorized`` response when encountering an Unauthorized exception.

You can change what action to take
when an by supplying an ``unauthorized_response`` argument
to ``KnaveMiddleware``. This must be a WSGI app,
and as such can return any suitable response
(for example, redirecting to a login page)::

    def redirect_on_unauthorized(environ, start_response):

        start_response('302 Found',
                       [('Location', '/login'), ('Content-Type', 'text/html')])
        return ['<html><body><a href="/login">Login</a></body></html>']


    app = KnaveMiddleware(app,
                          acl,
                          unauthorized_response=redirect_on_unauthorized)

Upgrading
=========

Upgrading to v0.3
-----------------

You will need to make the following changes in order to upgrade from previous
versions:

Predicate classes have changed their signature.
In v0.2 you would have written::

    class MyPredicate(Predicate):
        def __call__(self, environ, context=None):
            ...

    @make_predicate
    def my_custom_predicate(environ, context=None):
        ...

In v0.3 you should to change this to::

    class MyPredicate(Predicate):
        def __call__(self, acl, identity, context=None):
            ...

    @make_predicate
    def my_custom_predicate(acl, identity, context=None):
        ...

RoleProviders also have a different signature. Change from this::

    CustomRoleProvider(RoleProvider):
        def member_subset(self, roles, identity, environ, context):
            ...

To this::

    CustomRoleProvider(RoleProvider):
        def member_subset(self, roles, identity, context):
            ...

If your RoleProvider or Predicate depends on information from the WSGI environ,
this is no longer directly supported. Your application must now explicitly pass
any context information required to evaluate roles or predicates in the
``context`` argument.

Testing permissions now always requires an ACL object. Where in 0.2 you would
have written this::

    some_permission.check(environ)
    if some_other_permission.is_met(environ):
        do_something()

You should now change this to::

    from knave import ACL
    acl = ACL.of(environ)

    acl.require(some_permission)
    if acl.test(some_other_permission):
        do_something()



.. _repoze.who: http://docs.repoze.org/who/
.. _beaker: http://beaker.readthedocs.org/
