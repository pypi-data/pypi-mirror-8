Introduction
============

This is an add-on adapter for `RedTurtle Video`__ product for Plone. For additional documentation see
the main product's page.

Add this to your Plone installation for beeing able to use `Vimeo`__ video link as valid
URLs for "Video link" content type.

__ http://plone.org/products/redturtle.video
__ http://www.vimeo.com/

Autoplay
--------

You can enabled the Vimeo video autoplay in two ways:

* Use the YouTube ``autoplay=1`` parameter in the video URL
  you are saving in Plone.
  
  This is a permanent autoplay: the editor choose to autoplay the video at every visit
* Call the RedTurtle video content with the ``autoplay=1`` parameter.
  
  This is a user choice autoplay: who links the Plone content choose to auto
  start it.

