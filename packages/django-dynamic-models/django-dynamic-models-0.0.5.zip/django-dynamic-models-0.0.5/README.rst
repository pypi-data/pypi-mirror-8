=====
Django Dynamic Models
=====

Django Dynamic Models is a app that enable change model fields if other other apps models.

Detailed documentation is in the "docs" directory.

Install
-----------
```
pip install --upgrade django-dynamic-models
```


Quick start
-----------

1. Add `django_dynamic_models` to your INSTALLED_APPS setting before the apps you need change models like this::

    INSTALLED_APPS = (
        ...
        'django_dynamic_models',
        'app_with_models',
        'app_with_changes',
    )


2. Define your model your want to change from another apps
    
    import django_dynamic_models as dymodels
    app_label = 'app_label'

    class ArticleBase(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=50)   
        
        class Meta:
            abstract  = True
        
        def __unicode__(self):
            return u'%s' % self.name  

    Article = dymodels.change.load('Article', ArticleBase, app_label)

3. In the app need a model change add a file named 'models_changes_registry.py' and add her the new fileds

    import django_dynamic_models as dymodels
    from django.db import models
    
    dymodels.change.register('Article', **{
        'brand' : models.CharField(max_length=30, blank = True, null = True),        
    })

