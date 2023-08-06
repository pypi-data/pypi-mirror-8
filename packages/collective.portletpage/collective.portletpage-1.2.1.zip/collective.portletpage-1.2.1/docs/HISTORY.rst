Changelog
=========

1.2.1 (2014-10-29)
------------------

- Restored text field in the content view
  [keul]
- Fixed MANIFEST file
  [keul]

1.2 (2014-06-03)
----------------

- Do not break content view when a portlet is missing, but skip it
  (as Plone columns do)
  [keul]

- Fix permission for "Manage Portlets" action. Now, the green edit-bar is
  only shown to users with appropriate permissions.
  [thet]

- Added Spanish translation.
  [macagua]

- German translations.
  [thet]

- Change "Portlet Page" type registration, use actions.xml for
  "Manage Portlets" object tab and fix multiple buttons in edit-bar issue.
  [thet]

- Update templates to Plone 4 style and render it in content-core macro.
  [thet]

- PEP 8 Cleanups.
  [thet]

- Added French translation.
  [bouchardsyl]

1.1 (2011-12-20)
----------------

- fixed related items in view for Plone 4.1 compatibility.
  [fdelia]

- register as linkable object for TinyMCE (close `#2`__).
  [keul]

- restored logical order of first and secondo column in XHTML (close `#1`__).
  [nekorin]

- included "Site Administrator" in the rolemap.xml.
  [keul]

__ http://plone.org/products/collective.portletpage/issues/2
__ http://plone.org/products/collective.portletpage/issues/1

1.1b2 (2011-08-23)
------------------

- restored Plone 3 compatibility
  [keul]

- Plone 4.1 compatibility
  [keul]

- updated translation to be Plone 4.1 compatible; this will probably
  make some label untranslable on Plone 3
  [keul]

1.1b1 (2011-05-27)
------------------

- changed ``content_meta_type`` from ``Portlet Page`` to ``PortletPage``
  that was breaking sorting (see `#8161`__).
  [keul]

- removed from ``IPortletPage`` interface the ``subtitle`` field, not
  used anywhere.
  [keul]

- added ``portletPageColumn`` class to every portlet column.
  [keul]

- title field is not required anymore.
  [keul]

- when not provided, title, description and body are not shown in the
  view (this partially deprecate the need of additional products
  like `redturtle.portletpage.views`__).
  [keul]

- added a CSS ``clear`` rule at the last column.
  [nekorin]

- added a CSS rules for hack Sunburst behaviour with DD elements
  (see `#11840`__)
  [nekorin]

- do not display a portlets container if empty.
  [keul]

- added translation support, both i18n and locales
  (i18n is the only way right now to translate some stuff).
  [keul]

- changed the "*Portlets*" action tab to "*Manage portlet*".
  [keul]

- changes the ``i18n:domain`` of the configure.zcml of the
  browser module to "plone" (this is not formally right but,
  again, is needed for really translate views name).
  [keul]

- expanded left or right column if one of the two is missing,
  filling all space available.
  [keul]

- the Plone 4 "Hide" portlet now works also there.
  [keul]

- updated tests to reflect changes

__ http://dev.plone.org/plone/ticket/8161
__ http://plone.org/products/redturtle.portletpage.views
__ https://dev.plone.org/plone/ticket/11840

1.0 (unreleased)
----------------

- Add metadata.xml to the default-profile.
  [WouterVH]

- Add MANIFEST.in
  [WouterVH]

1.0b3 (2010-03-15)
------------------

- using style_slot instead of css_slot
  (name changed in plonetheme.sunburst which is default for plone4)
  [fRiSi]
