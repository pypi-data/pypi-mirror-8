[![Stories in Ready](https://badge.waffle.io/changer/cmsplugin-fbgallery.png?label=ready&title=Ready)](https://waffle.io/changer/cmsplugin-fbgallery)
cmsplugin-fbgallery
===================

[![Build Status](https://travis-ci.org/changer/cmsplugin-fbgallery.png?branch=master)](https://travis-ci.org/changer/cmsplugin-fbgallery)

Django CMS plugin for facebook album gallery

This projects helps integrate Facebook album into your Django CMS based website. The plugin provide superb performance compared to the Ajax based alternatives and works even on IE > 6 without any issues. Also, with caching enabled it loads fast without any lag.


## Installation:

Add the following line into your `requirements.txt` file:

```bash
https://github.com/changer/cmsplugin-fbgallery/archive/v1.0.2.zip
```
And add the page id in your settings file:

```py
INSTALLED_APPS = (
                  `cmsplugin_fbgallery`,
                  )
                  
FB_PAGE_ID = '125976107506398'# Get the page Id from facebook album you want to use.
# It is usually the page_id part of the album URL. 
https://www.facebook.com/media/set/?set=a.369541803149826.<album_info>.<page_id>&type=3 

```


Once, done add a block into the django template where you want to use the plugin to work, preferably in
base.html:

```html
{% placeholder facebook-gallery %}
```

## Usage:

In order to use, add the plugin into the intended placeholder and add facebook album Id and Album name in the admin and save the plugin and page. Once done, you will have the gallery up and running for you. 

### Finding Album ID:

A facebook Album URL contains the information about the Page ID and Album ID, Here is how you calculate the Album ID:

If URL is: https://www.facebook.com/media/set/?set=a.369541803149826.1073741825.125976107506398&type=3

Your Album ID is: 125976107506398_1073741825 .

Once you find album id of one album, find others is as easy as increasing the count by 1, as facebook assign new album by adding one at a time. So if you have another album, its album id must be 125976107506398_1073741826.

## Scope:

The future versions with bring in more cleanup and fixes to the plugin.

## Bugs/Issues:

Create an issue here with proper detail: https://github.com/changer/cmsplugin-fbgallery/issues 


## Inspirations/Credits:

This projects seeks some inspirations from the work of [@dantium](https://github.com/dantium) and [@driesdesmet](https://github.com/driesdesmet) on django-fbgallery but adapts it to more CMS plugin way.
