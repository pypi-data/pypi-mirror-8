Changelog
=========

0.7.0
-----

* The try of a Django 1.7 support.

0.6.4
-----

* Only using ``from PIL import Image`` imports to also support Pillow as PIL
  replacement.

0.6.3
-----

* Fixing issue with limiting select popup by multiple media type.

0.6.2
-----

* Fixing issue with limiting select popup by media type.

0.6.1
-----

* Fixing issues with media preview in the admin.

0.6.0
-----

* Django 1.4 compatibility.
* Use django-taggit instead of django-tagging.

0.5.6
-----

* Various south fixes.

0.5.5
-----

* Adding ``django-sortedm2m`` as dependency.

0.5.4
-----

* Fixing PIL import issue. Falling back to ``Image`` if ``PIL`` is not in the
  path.

0.4.1
-----

* Adding ``count`` field to Download model.
