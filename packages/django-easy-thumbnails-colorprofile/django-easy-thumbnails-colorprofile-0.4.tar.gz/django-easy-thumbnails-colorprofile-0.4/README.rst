INSTALL
=======

put easy_thumbnails_watermark in INSTALLED_APPS

::

    INSTALLED_APPS = (
        'easy_thumbnails_colorprofile',
    )

add the preprocesor in your settings

::

    from easy_thumbnails.conf import Settings as easy_thumbnails_defaults

    THUMBNAIL_PROCESSORS = easy_thumbnails_defaults.THUMBNAIL_PROCESSORS + (
        'easy_thumbnails_colorprofile.thumbnail_processors.colorprofile_processor',
    )


Credits
=======

I copied various code from http://stackoverflow.com/questions/11041044/python-pil-convert-jpg-from-adobergb-to-srgb

