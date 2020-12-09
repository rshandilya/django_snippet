####### Middle Ware ################
# Middelware cass structure
class CoffeehouseMiddleware(object):
	def __init__(self, get_response):
		self.get_response = get_response
        # One-time configuration and initialization on start-up

	def __call__(self, request):
		# Logic executed on a request before the view (and other middleware) is called.
		# get_response call triggers next phase
		response = self.get_response(request)
		# Logic executed on response after the view is called.
		# Return response to finish middleware sequence
		return response

	def process_view(self, request, view_func, view_args, view_kwargs):
		# Logic executed before a call to view
		# Gives access to the view itself & arguments
	
	def process_exception(self,request, exception):
		# Logic executed if an exception/error occurs in the view
	
	def process_template_response(self,request, response):
		# Logic executed after the view is called,
		# ONLY IF view response is TemplateResponse.
