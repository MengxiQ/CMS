import xmltodict
from ncclient import manager
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from CMS.apps.tools.testTools import ping_host


class xmlToolView(GenericAPIView):
    ip = ''
    user = {}
    action = {}
    sendCodeData = ''

    def post(self, request, *args, **kwargs):
        self.ip = request.data.get('ip')
        self.user = request.data.get('user')
        self.action = request.data.get('action')
        self.sendCodeData = request.data.get('sendCodeData')
        print(self.action)
        print(self.sendCodeData)
        # ping 状态监测
        if not ping_host(self.ip):
            return Response({'msg': 'ping超时，无法下发配置，请确保设备在线.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif self.action['name'] == 'get-config':
            return self.getConfig()
            # print(data)
            # return Response({'data': data}, status=status.HTTP_200_OK)
        elif self.action['name'] == 'edit-config':
            return self.editConfig()
            # print(data)
            # return Response({'data': data}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': '没有选择正确的配置动作.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def getConfig(self):
        try:
            connect = manager.connect(host=self.ip, port=self.user['port'], username=self.user['username'],
                                      password=self.user['password'], hostkey_verify=False,
                                      device_params={'name': self.user['device_params']},
                                      allow_agent=False, look_for_keys=False)
            with connect as m:
                reply_obj = m.get_config(source=self.action['source'], filter=self.sendCodeData)
                # reply_json_data = xmltodict.parse(str(reply_obj))
                print(reply_obj)
                reply_xml = str(reply_obj)
                print(reply_xml)
        except Exception as e:
            print('下发报文出错.', e)
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'data': reply_xml}, status=status.HTTP_200_OK)

    def editConfig(self):
        try:
            connect = manager.connect(host=self.ip, port=self.user['port'], username=self.user['username'],
                                      password=self.user['password'], hostkey_verify=False,
                                      device_params={'name': self.user['device_params']},
                                      allow_agent=False, look_for_keys=False)
            with connect as m:
                reply_obj = m.edit_config(target=self.action['source'], config=self.sendCodeData)
                # reply_json_data = xmltodict.parse(str(reply_obj))
                reply_xml = str(reply_obj)
        except Exception as e:
            print(e)
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'data': reply_xml}, status=status.HTTP_200_OK)
