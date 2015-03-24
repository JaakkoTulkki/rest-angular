from rest_framework import generics, status
from rest_framework.response import Response

from values.serializers import ValueSerializer
from values.models import Value

class ValueList(generics.ListCreateAPIView):
    model = Value
    serializer_class = ValueSerializer
    queryset = Value.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        print(repr(serializer))
        if serializer.is_valid():
            Value.objects.create(**serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': "Bad request",
                'message': 'Value could not be created'
            }, status=status.HTTP_400_BAD_REQUEST)