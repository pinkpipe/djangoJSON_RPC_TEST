from django.shortcuts import render

from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import RPCForm
from json_rpc.json_client import JSONRPCClient, JSONRPCException
from django.conf import settings

# Create your views here.

class RPCView(FormView):
    template_name = 'rpc_form.html'
    form_class = RPCForm
    success_url = reverse_lazy('rpc_form')

    def form_valid(self, form):
        method = form.cleaned_data['method']
        params_str = form.cleaned_data['params']

        try:
            params = [p.strip() for p in params_str.split(',') if p.strip()] if params_str else []
            params = [int(x) if x.isdigit() else x for x in params]
            client = JSONRPCClient(settings.JSONRPC_ENDPOINT, settings.CERTIFICATE, settings.PRIVATE_KEY)
            result = client.call(method, params)
            context = self.get_context_data(form=form, result=result)

        except JSONRPCException as e:
            context = self.get_context_data(form=form, error=str(e))
        except Exception as e:
            context = self.get_context_data(form=form, error=f"Unexpected error: {e}")
        return self.render_to_response(context)