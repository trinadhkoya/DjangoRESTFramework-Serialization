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


# When request comes like www.example.com/snippets
# it will activate this function do the following
@csrf_exempt
def snippet_list(request):
    if request.method == 'GET':
        snippets = Snippets.objects.all()
        # returns all the snippets objects stored in the database
        serializer = SnippetSerializer(snippets, many=True)
        ''' serializer ->returns all the serializer attributes with thier declarations like we did
        #Example ;
        #id = serializers.IntegerField(read_only=True)'''
        '''
        serializer.data returns
        OrderedDict([
            ('id',1),('title',u'php'),('code',u'<?php\r\n\r\n<h1>Hello</h1>\r\n\r\n?>'),('linenos',
             True),('language','php'),('style','emacs'),etc.......])
        ]),

        '''

        '''
        when it(serializer.data) caught by JSONResponse,it will render the data and produces the response in JSON format
        '''

        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


'''
here it is like http://example.com/1/
1 is equal to pk ,we have assigned that value in url pattern with name <pk>,you can rename it .
i changed with the pk with (key) in both urls.py and in the snippet_detail function as well


'''


@csrf_exempt
def snippet_detail(request, key):


    try:
        snippet = Snippets.objects.get(pk=key)
    except Snippets.DoesNotExist:
        return HttpResponse(status=404)

    '''
    here we are returning snippet object with the given value like /1 or /2 /3
    if the data not found it will throw an exception

    '''

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete();
        return HttpResponse(status=204)
