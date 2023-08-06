=====
urlparse3
=====

Urlparse3 is simple and powerful url parsing tool.
Example: 
::

    import urlparse3


    url = 'http://admin:secret@domain.com/path?q=123#anchor'
    parsed_url = urlparse3.parse_url(url)
    print parsed_url.scheme  # http
    print parsed_url.username  # admin
    print parsed_url.password  # secret
    print parsed_url.domain  # domain.com
    print parsed_url.path    # path
    # query is converted into dictionary
    print parsed_url.query  # {'q': '123'}
    print parsed_url.fragment # anchor

    # now add new GET parameter
    parsed_url['name'] = 'alex'
    # and get url back to string representation
    print parsed_url.geturl()  #  
    http://admin:secret@domain.com/path?q=123&name=alex#anchor
