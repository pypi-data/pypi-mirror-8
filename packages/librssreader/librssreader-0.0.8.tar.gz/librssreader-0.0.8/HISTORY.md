#History

##v0.1.0 - not yet publish 
- Make API domain configurable
- Support Inoreader API by default

# History of libgreader

##v0.8.0 - 
- Make API endpoint configurable

##v0.7.0 - 2013/03/18
- Now requires Requests > 1.0 (Requests now used for all HTTP requests)
- Python 3.3 Compatibility (Test suite passes for Python 2.6, 2.7, and 3.3)
- Deprecate OAuth 1.0 auth method (Google deprecated it April 20, 2012 https://developers.google.com/accounts/docs/OAuth )
- RIP Google Reader :(

##v0.6.3 - 2013/02/20
- Add support for add/remove tag transaction abi- lity, to mass edit tags on on an Item
- Add since/until argument support for many Container calls
- Add support for loadLimit argument with feed Containers loadItems() call

##v0.6.2 - 2012/10/11
- Fix broken post() method with OAuth2 auth, https://github.com/askedrelic/libgreader/issues/11

##v0.6.1 - 2012/08/13
- cleanup sdist package contents, to not include tests
- Remove httplib2 as a require import unless you are using GAPDecoratorAuthMethod

##v0.6.0 - 2012/08/10
* OAuth2 support
* Deprecating OAuth support
* Added auth support for Google App Engine with GAPDecoratorAuthMethod
* Internal code re-organization

##v0.5 - 2010/12/29
* Added project to PyPi, moved to real Python project structure
* Style cleanup, more tests

##v0.4 - 2010/08/10
Lot of improvements : 

* Manage special feeds (reading-list, shared, starred, friends...)
* Manage categories (get all items, mark as read)
* Manage feeds (get items, unread couts, mark as read, "fetch more")
* Manage items (get and mark read, star, share)

and:

* oauth2 not required if you don't use it
* replacing all xml calls by json ones

##v0.3 - 2010/03/07
* All requests to Google use HTTPS
* CLeaned up formatting, should mostly meet PEP8
* Fixed random unicode issues
* Added licensing

##v0.2 - 2009/10/27
* Moved all get requests to private convenience method
* Added a few more basic data calls

##v0.1 - 2009/10/27
* Connects to GR and receives auth token correctly.
* Pulls down subscription list.
