Introduction
============

a browser view that redirects to first found items which has catalog index = 'something'

The main purpose of this product is to link to or find content items in Plone from an external website.


An example
===========
My customer has a website with a system from the dark ages.
This system will have indexes that correspond to the indexes on the Plone site.
For example: an Employee ID on site A is the same as the Employee ID on site B.

So how can we link to employee on the Plone site?

This product makes it possible to use an url like

http://plonesite.com/index_redirect?index=indexname&index_value=value

For example, if you have an index in your Plone site called «phone», you can use an URL like

http://plonesite.com/index_redirect?index=phone&index_value=12345678


If there are more than one or zero entries in the catalog where phone=12345678, you will be redirected to:
'/@@search?phone=12345678

