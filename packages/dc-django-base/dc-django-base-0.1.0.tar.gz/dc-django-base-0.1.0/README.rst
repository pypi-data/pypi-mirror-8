DC Django Base
==============

Installation
------------

Settings
````````

Start the site's settings by importing the ``base_settings`` file.

    from dcbase.base_settings import *

Refer to this file to see the complete list of settings that are included by default. The following are settings that your 
site **must** provide:

* BASE_DIR (typically ``os.path.dirname(os.path.dirname(__file__))``)
* SECRET_KEY (source the production key from a secure place, **not** a text file in a public source repository)
* ROOT_URLCONF
* WSGI_APPLICATION
* DATABASES
* EMAIL_BACKEND (consider using ``django.core.mail.backends.console.EmailBackend`` for testing)

Add the site's apps to ``INSTALLED_APPS`` by prepending them to the base apps::

    INSTALLED_APPS = (
        'some_app',
        'allauth.socialaccount.providers.google',
    ) + INSTALLED_APPS

Other "list" settings can be modified in a similar way. 

Because the order of middleware is important it may be required to copy and modify the entire ``MIDDLEWARE_CLASSES`` setting
to inject a new middleware class in the middle of the list.

Urls
````

Include the following urls in the site's urlconf::

    url(r'', include('dcbase.urls')),

Templates
`````````

Create a ``base.html`` in the root of your templates directory. Extend ``dcbase/base.html`` and override
blocks that are global to your site. For example::

    {% extends "dcbase/base.html" %}
    
    {% block headerBarBrand %}My Site Brand{% endblock %}
    {% block footerBar %}
        Footer content!
    {% endblock %}

Templates
---------

DC-Base provides templates to override and include.

Base
````

The ``dcbase/base.html`` provides the basic page framework and layout. Provide your site's base template by extending this template
and overriding the following blocks.

- **pageTitle**: title of the page, as it will appear in the browser window's title bar
- **style**: inline CSS to include in the page style tag. you need to include your own enclosing \<style> element.
- **head**: extra content to include in the page head tag. use this to link external css, add meta tags, etc.
- **headerBarBrand**: content for the "brand" link in the upper right, usually the app title or site logo
- **headerBarBrandLink**: target of the "brand" link, usually the app's home page. default is site root.
- **headerBarRight**: extra nav items (\<li>'s) to include on the right side of the header bar
- **content**: the main content of the page. should normally start with a div with class "container" or "container-fluid"
- **footerBar**: content for the footer nav bar. this is a bootstrap navbar so the content here should probably be a \<ul>
- **script**: any additional scripts or script links the page needs. inline scripts must supply their own enclosing \<script> tag

Narrow Dialog Base
~~~~~~~~~~~~~~~~~~

Extend from ``dcbase/base-narrow-dialog.html`` for any page that is just a single, vertical form or dialog. Override the following
blocks to provide the dialog content:

- **panelHeading**: title of the dialog panel. include any required \<h*> tags.
- **panelType**: the type of panel (e.g. success, danger, etc.). default is "default"
- **panelBody**: content of the dialog panel

Forms
`````

Include ``dcbase/form.html`` or ``dcbase/form-horizontal.html`` to create consistently styled forms. These templates expect a context
variable called ``form``.

Set the ``autofocus`` context variable to the id of a form field which should be automatically focused when the page loads. For example::

    {% include "dcbase/form.html" with autofocus="id_important_field" %}

User Profiles
-------------

Create app-specific user profile data by following these instructions. 

Create a database model to encapsulate the profile data. Give it a ``OneToOneField`` to the ``User`` model and call it ``user``.

Create a ``ModelForm`` to update the new profile model.

Create a URL to the view that will edit the new profile model. To be consistent with other profile urls it should be in the form
of ``^accounts/profile/edit/CATEGORY/$``, where CATEGORY is unique to your app.  Make sure the url has a name, such as
``account_profile_edit_CATEGORY``.

Create the view for the above URL. The view class should look similar to this::

    @profile_form_view()
    class ProfileEditCATEGORYView(ProfileEditFormView):
        form_class = MyProfileForm
        profile_nav_name = _('Nav Name')
        profile_panel_name = _('Panel Name')
        profile_edit_url = reverse_lazy('account_profile_edit_CATEGORY')
    
    profileEditCATEGORYView = login_required(ProfileEditCATEGORYView.as_view())

The class-level attribute are:

* **profile_nav_name**: the title that will appear on the user profile navigation bar
* **profile_panel_name**: the title that will appear on the panel that holds the form
* **profile_edit_url**: URL to the page that allows editing of this profile model

After these things are done a new pane will appear in the user's profile edit page. This new page will contain the form for the
apps profile model.

New users will automatically get an instance of the new profile model in the database. If this is a new profile model for a site
with existing users then be sure to use a database migration to create an instance for every existing user.

