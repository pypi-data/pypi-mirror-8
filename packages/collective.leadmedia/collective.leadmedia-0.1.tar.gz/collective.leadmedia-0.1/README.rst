Features
============

- Adds a slideshow to dexterity folderish types
- Easy to adapt to custom dexterity types
- Easy to upload multiple images using drag and drop
- Easy to include youtube and vimeo videos in the slideshow

- Adds a media view that shows the first image of the slideshow in folders and collections
- Slideshow shows image description as caption
- Uses slick carousel by Ken Wheeler (adaptable to other carousels)

|eventview|

.. |eventview| image:: http://dev.intk.com/lead_media_screen_view.png

How it works
============

An administrator can choose which types are upgraded with slideshow functionality by adding a 'slideshow' behaviour via the 'Site Setup’/'Dexterity content types’. A folder named ’slideshow’ appears inside of items with slideshow behaviour. Using drag and drop functionality multiple images can be uploaded to the slideshow folder. A slideshow with the several images appears automatically in the view of any item that contains more than one image int the ‘slideshow' folder. In case the folder contains only one image, the view shows the image but not the next/previous buttons. In case the folder contains no images, the slideshow does not appear in the page.

Videos from YouTube and Vimeo can also be added to the slideshow. Create an item of type link inside the slideshow folder pointing to the video on youtube or Vimeo. Make sure the URL is a canonic YouTube or Vimeo url.

Implementation details
===================================
- Folderish content types are adapted with ICanContainMedia interface that provides MediaHandling class. This class adds functionallity to set the leading media.
- There is two FieldIndex and metadata added to portal_catalog: hasMedia (True/False) and leadMedia (UID of the leading picture).
- An event handler is added to folderish content types and is triggered on modified events. This event updates the indexes in the portal_catalog.

Dependencies
============

- collective.folderishtypes
- collective.slickslideshow
- collective.quickupload
- collective.FolderContentsPortletManager

How to use a different carousel?
===================================

The list of images available in the slideshow folder are being returned by the view /slideshowListing.

The view returns a json with the following format::
	
	{
	     url: image URL,
	     UID: Object UID
	}

The details of each image are being returned by the view http://url/to/image/get_slideshow_item

This view returns a json with the following format::
	
	{
	     type: The type of the item
	     description: Item description
	     title: Item title
	}

These views can be reached by AJAX calls.
Use your carousel API to add the slides. 

Todo
============

- Use collective.upload once is ready for production;
- Add collective.quickupload portlet automatically to Folder contents portlet manager
- Slideshow behaviour should only be added to folderish types
- How to retrieve the picture that appears as leading while using lead media a more efficient or correctly way?

Changelog
============

0.1 (2014-11-12)
-------------------

- Initial release