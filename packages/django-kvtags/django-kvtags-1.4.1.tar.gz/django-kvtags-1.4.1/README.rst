===============
django-kvtags
===============

Extensible tags in Django.

Tags can be associated with any django model. You can add any number of key-value pairs to the tags as you need.


TagManager
============

The best way to use django-kvtags is through TagManager.
First, add TagManager to your model to which you will add tags:

::

    class YourModel(models.Model):
        # your stuff
        objects = models.Manager()
        tags = TagManager()

If you want django-kvtags to use cache when it's available, pass the cache name with cache parameter to TagManager:

::

    class YourModel(models.Model):
        # your stuff
        objects = models.Manager()
        tags = TagManager(cache='default')



add (obj, \**kwargs)
-----------------------
Adds tags matched by kwargs to obj.

add_by_kv (obj, \**kwargs)
-----------------------------
Adds tags whose key-values are matched by kwargs to obj.

remove (obj, \**kwargs)
-------------------------
Removes tags matched by kwargs from obj.

remove_by_kv (obj, \**kwargs)
-------------------------------
Removes tags whose key-values are matched by kwargs from obj.

filter (obj, \**kwargs)
------------------------
Returns QuerySet of Tags bound to obj and matched by kwargs.

get_list (obj)
--------------
Returns a list of Tag model instances bound to obj

get_digest_list (self, obj)
---------------------------
Returns a list of objects which contains digested data of Tags bound to obj.
If cache is available and set, this method stores tag and item-tag dictionaries in the cache in order to make a lot less SQL queries. 


Using API
============

django-kvtags supports `tastypie`_.

TagResource
-------------

::

    # urls.py
    from kvtags.api import TagResource

    tag_resource = TagResource()

    urlpatterns = patterns('',
        # The normal jazz here...
        (r'^api/', include(tag_resource.urls)),
    )

or

::

    # urls.py
    from tastypie.api import Api
    from kvtags.api import TagResource

    your_api = Api(api_name='v1')
    # Your other resources
    your_api.register(TagResource())


    urlpatterns = patterns('',
        # The normal jazz here...
        (r'^api/', include(your_api.urls)),
    )


TaggedItemResource
------------------

TaggedItem has generic relation to your models. If you don't need to resolve the relations,
you can include TaggedItemResource to your API just as you include TagResource.

However, if you want to resolve generic relations, you should create a new class based on
TaggedItemResource by yourself. Then, add the new class to the API as usual.

Example:

::

    # urls.py
    from kvtags.api import TaggedItemResource
    from tastypie.contrib.contenttypes.fields import GenericForeignKeyField
    from yourapp.models import Spam, Egg
    from yourapp.api import SpamResource, EggResource

    class MyTaggedItemResource(TaggedItemResource):
        content_object = GenericForeignKeyField({
            Spam: SpamResource,
            Egg: EggResource
        }, 'content_object')


Adding Tags Field to a Resource
===================================
If you want to add the tags associated with a model to the model's resource, you can do that by using get_list or get_digest_list methods as follow:

::

    class YourModelResource(ModelResource):
        # your stuff
        tags = fields.ListField()
        
        def dehydrate_tags(self, bundle):
            return YourModel.tags.get_digest_list(bundle.obj)


.. _tastypie: https://django-tastypie.readthedocs.org/en/latest/