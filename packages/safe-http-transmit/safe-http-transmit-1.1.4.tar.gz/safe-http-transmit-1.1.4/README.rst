==================
Safe HTTP Transmit
==================

Provides a function, `transmit`, that tries retries a http call  multiple times.

Also, an annoying bug with urllib is when it returns results from multiple 
classes  (urllib2.HTTPError, socket.error, urllib2.URLError). 
Safe HTTP Transmit unifies all error types and they inherit from a HttpLoadError class. 


