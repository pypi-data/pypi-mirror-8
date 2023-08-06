Introduction
============

This package aims to bring some improvements to make working with wtforms easier.

This package currently allows you to render entire forms.

Support for rendering wtform widgets with bootstrap and foundation are currently supported.


Example::

    class MyForm(Form):
        # special property we use to specify order fields should
        # be shown
        _order = ['age']
        age = IntegerField(u'Age')

    form = MyForm(req.POST)
    from wtforms_extras import render_form
    render_form(form, style='bootstrap')

    # or just a field
    from wtforms_extras import render_field
    render_form(form, 'age', style='bootstrap')


Changelog
=========

1.0 - 2014-11-13
----------------

- initial release