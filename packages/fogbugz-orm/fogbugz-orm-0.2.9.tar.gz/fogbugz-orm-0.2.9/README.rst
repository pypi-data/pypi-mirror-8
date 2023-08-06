**fogbugz-orm - FogBugz ORM wrapper around the FogBugz XML API**

This is a python interface to the `FogBugz XML API`_
`FogBugz`_ (http://www.fogcreek.com/fogbugz/) issue tracker. It wraps the
`FogBugzPy`_ python interface, which provides non-typed python binding via
`BeautifulSoup`_. As well as type conversion, this ORM interface provides
direct JSON serialization of the FogBugz data using the `jsontree`_ module.

.. warning::
   It is HIGHLY recommended that you use an SSL connection to the FogBugz
   server for secure authentication.

Project Links:

* `Documentation <http://pythonhosted.org/fogbugz-orm/>`_
* `PyPi <https://pypi.python.org/pypi/fogbugz-orm>`_
* `GitHub <https://github.com/dougn/fogbugz-orm>`_

External Links:

* `FogBugz`_
* `FogBugz XML API`_
* `FogBugzPy`_
* `FogBugzPy on PyPi <https://pypi.python.org/pypi/fogbugz/>`_
* `BeautifulSoup`_
* `jsontree`_

.. _FogBugz: http://www.fogcreek.com/fogbugz/
.. _FogBugz XML API: http://fogbugz.stackexchange.com/fogbugz-xml-api
.. _FogBugzPy: https://developers.fogbugz.com/default.asp?W199
.. _BeautifulSoup: http://www.crummy.com/software/BeautifulSoup/bs3/documentation.html
.. _jsontree: http://pythonhosted.org/jsontree/

Quick Start
===========

**Comparing FogBugzPy to FogBugz-ORM**

Example code from `FogBugzPy`_ documentation:

.. code:: python

    resp = fb.search(cols="ixBug,sTitle")
    
    for case in resp.cases.findAll('case'):
        print "%s: %s" % (case.ixbug.string, 
                          case.stitle.string.encode('UTF-8'))
                          
Equivalent FogBugz-ORM code:

.. code:: python
    
    cases = fb.search(cols="ixBug,sTitle")
    
    for case in cases:
        print "%d: %s" % (case.ixBug, case.sTitle)
                          
* You can access the array of cases directly as a list.
* The column names are referred to in their proper mixed case matching the API
  as they must be for the cols argument; ``ixBug``, ``sTitle``.
* The data is extracted and properly converted; ``ixBug`` is an integer, and
  ``sTitle`` is a UTF-8 converted string.


**Get all the cases from the 'To Be Closed' filter and close them.**

.. code:: python

    import fborm
    
    ### login form 1
    fbo = fborm.FogBugzORM('https://hostname/', secret_token)
    
    ### Find the 'To Be Closed' filter
    filters = fbo.listFilters()
    for filt in filters:
        if filt.sName == 'To Be Closed':
            break
    
    ### Set it as the current filter
    fbo.setCurrentFilter(filt)
    
    ### Get all cases in that filter
    cases = fbo.search()
    
    ### Make sure they are closed
    for case in cases:
        if not case.fOpen:
            continue
        if 'Active' in case.sStatus:
            fbo.resolve(ixBug=case.ixBug)
        fbo.close(ixBug=case.ixBug)
    


**Create a new case**

.. code:: python

    import fborm
    import jsontree
    
    ### login form 2
    fbo = fborm.FogBugzORM('https://hostname/', username=u, password=p)
    
    bug = jsontree.jsontree()
    bug.sCategory = 'Bug'
    bug.sProject = 'My Project'
    bug.sArea = 'Some Area'
    bug.sTitle = 'The title of the bug'
    bug.tags = ['tag1', 'tag2', 'tag3']
    bug.sEvent = """
        Some nice long comment for the change being made
    """
    
    ixBug = fbo.new(bug)



**List some data**

.. code:: python

    import fborm
    
    fbo = fborm.FogBugzORM('https://hostname/')
    ### login form 3
    fbo.logon(username=u, password=p)
    
    people = fbo.listPeople()
    projects = fbo.listProjects()
    areas = fbo.listAreas()
    areas_in_proj = fbo.listProjects(ixProject=projects[0].ixProject)
    
    ### if you are using the CustomFields plugin
    custom_field_names = fbo.listCustomFieldNames()
    


**CustomFields Plugin Data**

The CustomFields plugin allows you to add yor own elements to cases in
`FogBugz`_. These elements are added to the `FogBugz XML API`_ with a prefix
and a unique magic string suffix. Also, any punctuation is transformed,
so you will need to look up what your custom field is with
:py:meth:`fborm.FogBugzORM.listCustomFieldNames`. Once you know that,
you can simplify your code by setting a ``namemap`` for the returned data.
This means that if you have multiple servers with the same CustomFields,
they will have different names in the API. Having a per-server ``namemap``
greatly simplifies your code.

.. code:: python

    import fborm
    
    ### Mapping of code name to what it is in the FogBugz XML API.
    custom_field_map = dict(
        sBranch = 'plugin_customfields_at_fogcreek_com_branchg83'
    )
    
    ### fborm type mapping between the FogBugz XML API element to python type
    ### only list the items you want returned.
    fbBugType = dict(
        ixBug = fborm.fbint,
        sTitle = fborm.fbstring,
        sBranch = fborm.fbstring,
        dtOpened = fborm.fbdatatime,
    )
    
    ### supply a ``namemap`` for mapping custom fields to more friendly
    ### in code names.
    fbo = fborm.FogBugzORM('https://hostname/', namemap=custom_field_map)
    ### login form 4
    fbo.token = secret_token
    
    ### All the cases in the last week
    bugs = fbo.search(q='opened:"This Week"', casetype=fbBugType)
    for bug in bugs:
        print bug.ixBug, bug.sBranch, bug.dtOpened.isoformat(), bug.sTitle
        
        ### if it is for the 'feature_x' branch, set it to be 'feature_xy'
        if sBranch == 'feature_x':
            bug.sBranch = 'feature_xy'
            bug.sEvent = "The 'feature_x' branch was merged into 'feature_xy'"
            del bug['dtOpened'] # only admins can set this.
            fbo.edit(bug, fbBugType)


