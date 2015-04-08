from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from kehko.general_permissions import IsCompanyAdmin

from actions.models import Action
from actions.serializers import ActionSerializer
from causes.models import Cause, CauseMembers
from companies.models import Company

class CompanyActions(generics.ListCreateAPIView):
    model = Action
    serializer_class = ActionSerializer
    authentication_classes = (JSONWebTokenAuthentication, )

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(), )
        else:
            return (IsCompanyAdmin(), )

    def get_queryset(self):
        return Action.objects.filter(cause_member__company__slug=self.kwargs.get('slug'))

    def post(self, request, *args, **kwargs):
        obj = Company.objects.get(slug=self.kwargs.get('slug', None))
        self.check_object_permissions(request, obj)
        #see if there's such a cause
        try:
            cause_pk = request.data.get('cause')
            cause = Cause.objects.get(pk=cause_pk)
        except:
            return Response({
                'status': "400",
                'message': "No such cause"
            }, status=status.HTTP_400_BAD_REQUEST)
        #see if they are already members of a cause
        try:
            cause_member = CauseMembers.objects.get(company=obj, cause=cause)
        #if not, make them a causemember
        except:
            cause_member = CauseMembers.objects.create(company=obj, cause=cause)
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(cause_member=cause_member)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': "400",
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


