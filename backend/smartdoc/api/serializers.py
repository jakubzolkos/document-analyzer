from rest_framework.serializers import Serializer, FileField, ReadOnlyField, SerializerMethodField, CharField
from .models import Document


class DocumentSerializer(Serializer):

    file_name = CharField(max_length=200)
    file_type = CharField(max_length=200)
    file_size = SerializerMethodField()

    class Meta:

        model = Document
        fields = ['file_name', 'file_type', 'file_size']

    def get_file_size(self, obj):

        x = obj.file_size
        y = 512000
        if x < y:
            value = round(x/1000, 2)
            ext = ' kb'
        elif x < y*1000:
            value = round(x/1000000, 2)
            ext = ' Mb'
        else:
            value = round(x/1000000000, 2)
            ext = ' Gb'

        return str(value)+ext