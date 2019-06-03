from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User
'''
The first thing we need to get started on our Web API
is to provide a way of serializing and deserializing the
snippet instances into representations such as json.

class SnippetSerializer(serializers.Serializer):
    #defines the fields that get serialized/deserialized.
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)

    #control how the serializer should be displayed in certain circumstances,
    #such as when rendering to HTML. The {'base_template': 'textarea.html'} flag
    #above is equivalent to using widget=widgets.Textarea on a Django Form class.

    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    #define how fully fledged instances are created or modified when calling serializer.save()

    def create(self, validated_data):

        #Create and return a new `Snippet` instance, given the validated data.

        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):

        #Update and return an existing `Snippet` instance, given the validated data.

        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


#more concise
#An automatically determined set of fields.
#Simple default implementations for the create() and update() methods.
#so if you want to custormize the way how to create and update serializer you can use serializers.Serializer
class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')
'''

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = User
        fields = ('id', 'username', 'snippets','owner')
