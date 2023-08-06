=====
django-hashphrase
=====

django-hashphrase is a django module that facilitates the process that
users click on a link in an email and django handles the click.
Hashlink makes it easy to generate such a link, authenticate it or not,
calls a custom function or not, etc.

Quick start
-----------

1. Add "hashphrase" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'hashphrase',
    )

2. Include the hashphrase URLconf in your project urls.py like this::

    url(r'^hl/', include('hashphrase.urls')),

3. To generate a link::

    from hashphrase.models import HashLink

    from django.contrib.auth.models import User
    any_object = User.objects.get(id=1)

    import datetime
    action = 'my_click_handler'
    hash_phrase = HashLink.gen_key(request.user, any_object, datetime.datetime.now(), action=action)

    # Then generate for example "http://yourhost.com/hl/"+hash_phrase+"/"
    # that lick will call the "registered" function

4. To register a function::

    from hashphrase.helpers import hashphrase_register
    @hashphrase_register('my_click_handler')
    def test_success(request, has_error, error_code, hash_link, content_obj):
        """
        use hashphrase_register decorator to register this function to be called when
        users click on the email link.
        be sure to check has_error. If not verified, has_error = True
        See HashLink class for error code definition
        """
        if has_error or not hash_link or not content_obj:
            from hashphrase.models import HashLink
            ret = "Invalid email link."
            if error_code == HashLink.ERR_EXPIRED:
                ret = "Link expired."
            elif error_code == HashLink.ERR_INVALID_USER:
                ret = "Needs to login."
            elif error_code == HashLink.ERR_INVALID_LINK:
                ret = "Invalid link."
            return HttpResponse(ret)
        return HttpResponse("Successful.")



5. To register a function, required::

    from hashphrase import hashphrase_register
    In your settings.py, add HASHPHRASE_HANDLERS that should list where your registered functions are.
    For example,
    HASHPHRASE_HANDLERS = ['views.handler1', 'views.handler2']
    This is required because not all Django/Python .py, except for __init__.py, are imported when Django server first runs.

