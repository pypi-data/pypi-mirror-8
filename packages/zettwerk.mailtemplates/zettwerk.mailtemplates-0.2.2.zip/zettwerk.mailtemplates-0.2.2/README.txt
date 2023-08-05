Introduction
============

Create mail templates in plone.

If you want to send emails out of plone, you need to create a custom template or method. With this extension it is possible to create mail templates and send them without the need of programming. Nevertheless there is an api to send such created templates by code. For choosing the recipients you can filter by users or groups. In addition there are also extensible user filter, queried through the zca.

Installation
============

Add zettwerk.mailtemplates to your buildout eggs::

  eggs = ..
         zettwerk.mailtemplates

After running buildout and starting the instance, you can install Zettwerk Mailtemplates via portal_quickinstaller to your instance.

Use-Case
========

Go to the plone configuration and click on the Zettwerk Mailtemplates link, listed under the custom extensions. Use plone's add menu to add a template. Enter a title (which results in the mail subject) and a mail body text. Also set the template-id.

Click on "portal_mail_templates" on the breadcrumb. Now you can filter the recipients by username or group selection. Try the simulate button the get a list of the selected recipients. Hit the send button to send the mail(s).

By filtering a group, you can provide an additional filter. These are registered utilities for zettwerk.mailtemplates.interfaces.IMessageTemplateUserFilter - see the configure.zcml and the utility with the name "registration_reminder" for an example. This on returns only users which have never logged in to your plone site.

Recursive Groups
================

By selecting a group only the toplevel group members are used. If the group contains other groups, there members are not used.

Override Plone's default templates
==================================

It is common to customize Plone's default templates for registration and password reset. zettwerk.mailtemplates supports this through the web - no need to add custom template overrides via code. Just add a template with id 'registration' or 'password_reset' and it is used - that's all.

Todos
=====

* Tests and api documentation needed.
