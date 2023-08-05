========================================================
accept-types - Use the correct accept type for a request
========================================================

``accept-types`` helps your application respond to a HTTP request in a way that a client prefers.
The ``Accept`` header of an HTTP request informs the server which MIME types the client is expecting
back from this request, with weighting to indicate the most prefered. If your server can respond in
multiple formats (e.g.: JSON, XML, HTML), the client can easily tell your server which is the
prefered format without resorting to hacks like '&amp;format=json' on the end of query strings.


Usage
=====

``get_best_match``
------------------

When provided with an ``Accept`` header and a list of types your server can respond with, this function
returns the clients most prefered type. This function will only return one of the acceptable types you
passed in, or ``None`` if no suitable type was found:

.. code:: python

	from accept_type import get_best_match

	def get_the_info(request):
		info = gather_info()

		return_type = get_best_match(request.META.get('HTTP_ACCEPT'), ['text/html', 'application/xml', 'text/json'])

		if return_type == 'application/xml':
			return render_xml(info)

		elif return_type == 'text/json':
			return render_json(info)

		elif return_type == 'text/html':
			return render_html(info)

		elif return_type == None:
			return HttpResponse406()

``parse_header``
----------------

When provided with an ``Accept`` header, this will parse it and return a sorted list of the clients
accepted mime types. These will be instances of the ``AcceptableType`` class.

.. code:: python

	>>> from accept_type import parse_header
	>>> parse_header('text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	['text/html, weight 1', 'application/xhtml+xml, weight 1', 'application/xml, weight 0.9', '*/*, weight 0.8']

``AcceptableType``
------------------

``AcceptableType`` instances represent one of the types that a client is willing to accept. This
type could include wildcards, to match more than one MIME type.

.. code:: python

	>>> from accept_type import AcceptableType
	>>> type = AcceptableType('image/*;q=0.9')
	AcceptableType
	>>> type.mime_type
	'image/*'
	>>> type.weight
	0.9
	>>> type.matches('image/png')
	True
	>>> type.matches('text/html')
	False

