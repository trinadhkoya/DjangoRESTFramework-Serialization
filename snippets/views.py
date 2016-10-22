from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from snippets.models import Snippets
from snippets.serializers import SnippetSerializer


class JSONResponse(HttpResponse):


    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def snippet_list(request):

        if request.method == 'GET':
            snippets = Snippets.objects.all()
            serializer = SnippetSerializer(snippets, many=True)
            return JSONResponse(serializer.data)
        elif request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = SnippetSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data, status=201)
            return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request,pk):

        snippet=Snippets.objects.get(pk=pk)

        if request.method=='GET':
            serializer=SnippetSerializer(snippet)
            return JSONResponse(serializer.data)

        elif request.method=='PUT':
            data=JSONParser().parse(request)
            serializer=SnippetSerializer(snippet,data=data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data)
            return JSONResponse(serializer.errors,status=400)

        elif request.method=='DELETE':
            snippet.delete();
            return HttpResponse(status=204)
