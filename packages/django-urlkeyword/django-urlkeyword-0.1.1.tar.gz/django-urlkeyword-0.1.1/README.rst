==========
urlkeyword
==========

Validate that your slugs do not match a keyword in your url 

---------
Rationale
---------

Suppose you have some of urls like:

- ``country-of-fire/edit/``
- ``country-of-fire/hidden-leaf-village/``
- ``country-of-fire/hidden-leaf-village/edit/``
- ``country-of-fire/forest-of-death/``
- ``country-of-fire/forest-of-death/edit/``

If the feudal lords of the Country of Fire decided to found a new village, you would kindly try to suggest them to avoid names like ``edit`` or ``delete``; they probably won't understand anything about technological constraints, but your suggestion could be nonetheless welcome.

Instead of trying to explain why it's not a good idea to found "Edit" (though maybe "Edit Village" may be acceptable), you may just write a piece of software that will not let anybody register any place suchly named. This is called validation_.

.. _validation: https://docs.djangoproject.com/en/dev/ref/validators/

-----
Usage
-----

Modify your ``settings.py`` to include the list of words you want to use as keywords::

    # settings.py

    URL_KEYWORDS = ('new', edit', 'delete')

Then add the validator to your slug field::

    # models.py

    from urlkeyword import validate_url_keyword

    class Village(Model):
        code = models.SlugField(max_length=20, validators=[validate_url_keyword])
