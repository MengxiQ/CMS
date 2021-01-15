from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from CMS.apps.detail.views.Generics.configTools import ConfigTools
from CMS.apps.tools.testTools import ping_host


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


def dictToObj(dictObj):
        if not isinstance(dictObj, dict):
            return dictObj
        d = Dict()
        for k, v in dictObj.items():
            d[k] = dictToObj(v)
        return d


class xmlToolView(GenericAPIView, ConfigTools):

    def post(self, request, *args, **kwargs):
        ip = request.data.get('ip')
        user = request.data.get('user')
        action = request.data.get('action')
        sendCodeData = request.data.get('sendCodeData')
        # ping 状态监测
        if not ping_host(ip):
            return Response({'msg': 'ping超时，无法下发配置，请确保设备在线.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif action['name'] == 'get':
            try:
                m = self.connect(ip, dictToObj(user))
                # 返回data标签里的数据
                reply_xml = str(m.get(filter=sendCodeData))
                return Response({'data': reply_xml}, status=status.HTTP_200_OK)
            except Exception as e:
                print('下发报文出错.', e)
                return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif action['name'] == 'get-config':
            try:
                m = self.connect(ip, dictToObj(user))
                # 返回data标签里的数据
                reply_xml = str(m.get_config(source=action['source'], filter=sendCodeData))
                return Response({'data': reply_xml}, status=status.HTTP_200_OK)
            except Exception as e:
                print('下发报文出错.', e)
                return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif action['name'] == 'edit-config':
            try:
                m = self.connect(ip, dictToObj(user))
                # 返回data标签里的数据
                reply_xml = str(m.edit_config(target=action['source'], config=sendCodeData))
                return Response({'data': reply_xml}, status=status.HTTP_200_OK)
            except Exception as e:
                print('下发报文出错.', e)
                return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'msg': '没有选择正确的配置动作.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

