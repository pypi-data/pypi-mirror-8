from django.views.generic.edit import View, FormView
from django.http import HttpResponse, JsonResponse

import markdown

from . import forms
from .settings import MARKDOWNX_MARKDOWN_KWARGS


class MarkdownifyView(View):

    def post(self, request, *args, **kwargs):
        return HttpResponse(markdown.markdown(request.POST['content'], **MARKDOWNX_MARKDOWN_KWARGS))


class ImageUploadView(FormView):
    template_name = "dummy.html"
    form_class = forms.ImageForm
    success_url = '/'

    def form_invalid(self, form):
        response = super(ImageUploadView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response
 
    def form_valid(self, form):
        image_path = form.save()
        response = super(ImageUploadView, self).form_valid(form)

        if self.request.is_ajax():
            data = {}
            data['image_path'] = image_path
            return JsonResponse(data)
        else:
            return response
