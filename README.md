REST FRAMEWORKS

Serialization
  1.use serializers.Serializer

  class SnippetSerializer(serializers.Serializer):
        #defines the fields that get serialized/deserialized.

        #define how fully fledged instances are created or modified when calling serializer.save()
        def create(self, validated_data):

        def update(self, instance, validated_data):

  2.serializers.ModelSerializer
  #An automatically determined set of fields.
  #Simple default implementations for the create() and update() methods.

  class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')


View
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def snippet_detail(request, pk):
      """
      Retrieve, update or delete a code snippet.
      """
      try:
        snippet = Snippet.objects.get(pk=pk)
      except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

      if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

      elif request.method == 'PUT':
      serializer = SnippetSerializer(snippet, data=request.data)
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      elif request.method == 'DELETE':
        snippet.delete()


        return Response(status=status.HTTP_204_NO_CONTENT)

Wrappers on API view
1. @api_view decorator for function based views
2. APIView class for class-based views

Why Wrappers: check request instances make sure you receive
              adding context in response
              return 405 Method Not Allowed, check input behavior
              handle ParseError exception when accessing request.data


class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#use mixins
#building our view using GenericAPIView, and adding in ListModelMixin and CreateModelMixin.
class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


#generics class-based views

class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


Authentication & permissions
1.Code snippets are always associated with a creator.
2.Only authenticated users may create snippets.
3.Only the creator of a snippet may update or delete it.
4.Unauthenticated requests should have full read-only access.

1.Add field to represent the user who created code
owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
highlighted = models.TextField()
