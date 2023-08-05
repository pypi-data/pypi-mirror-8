Changelog
=========

2.1.0 (2014-10-10)
------------------

- Removed old deprecated code [keul]
- Added skinswitcher, now handle skin switch in Plone and not Apache.
  This will fix issue with Plone 4.1.5 and up [keul] 
- Added MANIFEST file [keul]

2.0.0 (2011-07-29)
------------------

* First public release
* Plone 4 (maybe also 3.3 but not 3.2 or lower for sure) compatibility [keul]
* z3c.autoincude support [keul]
* Bye bye p4a.subtyper [keul]
* Changed logo viewlet: Plone 3.3 and above already refer to INavigationRoot [keul]
* Removed the getNavigationRoot patch, as ticket #8787 has been closed [keul]
* Now also JavaScript registry refer to subsite root, this fix JavaScript errors in the
  frontend [keul]

1.0.3 (2009-01-28)
------------------

* The traversal adapter was raising a lot of conflict error because all of the requests
  were trying to apply the INavigationRoot on the subsite [keul]

1.0.2 (2008-12-11)
------------------

* Applied a monkey patch for fixing a bug in the getNavigationRoot method of plone.
  See https://dev.plone.org/plone/ticket/8787 [keul]

1.0.1 (2008-12-05)
------------------

* Added support to browser layer CSS [amleczko]

1.0.0 (2008-11-18)
------------------

* Initial release

