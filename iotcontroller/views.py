# Create your views here.
from django.http import Http404

from rest_framework import  permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from iotcontroller.models import IOTDeviceModel
from iotcontroller.serializers import IOTControllerSerializers


# Create your views here.


class IOTDevicesList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        snippets = IOTDeviceModel.objects.all()
        serializer = IOTControllerSerializers(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = IOTControllerSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModifiedSingleIOTDevice(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #
    def get_object(self, pk):
        try:
            return IOTDeviceModel.objects.get(pk=pk)
        except IOTDeviceModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = IOTControllerSerializers(queryset)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = IOTControllerSerializers(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class IOTControllerViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = IOTControllerModel.objects.all().order_by('-create_at')
#     serializer_class = IOTControllerSerializers
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# class GetStatusDevices(APIView):
#     def get(self, request, format=None):
#         response = {'status': 400, 'data': []}
#         # response_encode = json.dumps(response, ensure_ascii=False)
#         # return HttpResponse(response_encode, content_type="application/json")
#
#     def post(self, request, format=None):
#         response = {}
#         # if parse(request.META['HTTP_USER_AGENT']).is_pc:
#         #     pass
#         # else:
#         try:
#             object_result_devices = [{
#                 'id': i.__getitem__('id').__str__(), 'author': {'name': CustomUser.objects.get(id=i.__getitem__(
#                     'auther_id')).__str__(), 'profile_picture': CustomUser.objects.get(id=i.__getitem__(
#                     'auther_id')).picture_profile.__str__() if CustomUser.objects.get(id=i.__getitem__(
#                     'auther_id')).picture_profile.__str__() else '/media/profile_pictures' '/user.jpg', 'phone_number':
#                                                                     CustomUser.objects.get(id=i.__getitem__(
#                                                                         'auther_id')).phone_number.__str__(), },
#                 'device_name': i.__getitem__('device_name').__str__(),
#                 'device_status': {
#                     "index": IOTController.DEVICE_STATUS[i.__getitem__('device_status')][0],
#                     "value": IOTController.DEVICE_STATUS[i.__getitem__('device_status')][1]},
#
#                 # 'create_at': str(i.__getitem__('create_at')),
#                 # 'modified_at': str(i.__getitem__('modified_at')),
#             } for i in IOTController.objects.all().values().filter()]
#             response['status'] = 200
#             response['data'] = object_result_devices
#             response_encode = json.dumps(response, ensure_ascii=False)
#             return HttpResponse(response_encode, content_type="application/json")
#         except Exception as e:
#             response['status'] = 400
#             response['data'] = [e.__str__()]
#             response_encode = json.dumps(response, ensure_ascii=False)
#             return HttpResponse(response_encode, content_type="application/json")
#
#
# class ChangeStatusDevice(APIView):
#     def get(self, request, format=None):
#         response = {'status': 400, 'data': []}
#         # response_encode = json.dumps(response, ensure_ascii=False)
#         # return HttpResponse(response_encode, content_type="application/json")
#
#     def post(self, request, val, format=None):
#         response = {}
#         try:
#             value = int(val)
#             object_single_device = [{
#                 'id': i.__getitem__('id').__str__(),
#                 'author': {'name': CustomUser.objects.get(id=i.__getitem__('auther_id')).__str__(),
#                            'profile_picture': CustomUser.objects.get(
#                                id=i.__getitem__('auther_id')).picture_profile.__str__() if CustomUser.objects.get(
#                                id=i.__getitem__('auther_id')).picture_profile.__str__() else '/media/profile_pictures'
#                                                                                              '/user.jpg',
#                            'phone_number': CustomUser.objects.get(id=i.__getitem__('auther_id')).phone_number.__str__(),
#                            },
#                 'device_name': i.__getitem__('code_product').__str__(),
#
#                 'device_status': {
#                     "index": IOTController.DEVICE_STATUS[i.__getitem__('device_status')][0],
#                     "value": IOTController.DEVICE_STATUS[i.__getitem__('device_status')][1]},
#                 'modified_at': str(jdatetime.date.fromgregorian(date=i.__getitem__('modified_at'))),
#                 'create_at': str(i.__getitem__('create_at').strftime("%Y-%m-%d")),
#             } for i in IOTController.objects.values().filter(code_product=value)]
#             response['status'] = 200
#             response['data'] = object_single_device
#             response_encode = json.dumps(response, ensure_ascii=False)
#             return HttpResponse(response_encode, content_type="application/json")
#         except Exception as e:
#             response['status'] = 400
#             response['data'] = e
#             response_encode = json.dumps(response, ensure_ascii=False)
#             return HttpResponse(response_encode, content_type="application/json")
#         except:
#             pass
