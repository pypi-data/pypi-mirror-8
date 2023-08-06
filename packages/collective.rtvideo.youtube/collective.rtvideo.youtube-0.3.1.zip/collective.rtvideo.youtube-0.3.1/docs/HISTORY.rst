Changelog
=========

0.3.1 (2014-12-01)
------------------

- Always load the https version of resources URL
  [keul]
- Fixed non-XHTML usage of ``allowfullscreen`` attribute
  [keul]


0.3.0 (2014-07-21)
------------------

* Added a video object id (for usability reason)
  [keul]
* If the YouTube URL contains the ``autoplay=1`` parameter
  or if the RedTurtle video contents is called with the same
  param, autoplay on video will be enabled
  [keul]
* If the request url use autoplay, some accessibility/usability
  improvements are added to the page, for simply keyboard controls
  [keul]
* Removed the secondary template, just use one template for standard
  and shortened embedding
  [keul]
* Fixed Python import for Plone 4.3 (same problem of ticket `#14`__)
  [bhenker, keul]

__ https://github.com/RedTurtle/redturtle.video/pull/14

* Replaced object tag with iframe [cekk]

0.2.0 (2012-09-04)
------------------

* Fixed egg dependency only to ``redturtle.video``
  [keul]
* add getThumb method to return a default thumbnail image to redturtle.video on
  IRemoteVideo creation. This is a new feature of redturtle.video 0.8 and up.
  [lucabel]
* Add a new div around object tag in video template, new param and transparency.
  So you can be able to set correctly a z-index on this div and solve overlap
  problem with other elements on Internet Explorer.
  [lucabel]

0.1.0 (2011-05-12)
------------------

* Initial release (moved out from ``redturtle.video``)
* Support new ``youtu.be`` URLs

