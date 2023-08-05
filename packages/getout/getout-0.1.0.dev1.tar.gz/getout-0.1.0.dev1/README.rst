A Python Library to Read Outlinks For A Given URL
==================================================
You can either use this package as a command line tool like:

    getout -u http://datafireball.com

Or you can use functions from this library inside your python code like ::

    #!/usr/bin/python
    import getout
    outlinks = getout.getoutlinks('http://datafireball.com')
