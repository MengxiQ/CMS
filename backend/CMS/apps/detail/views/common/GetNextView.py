from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from CMS.apps.detail.views.Generics.GetUserInfo import GetUserInfo
from CMS.apps.detail.views.Generics.configTools import ConfigTools


class GetNextView(GenericAPIView, ConfigTools, GetUserInfo):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        ip = request.query_params.get('ip')
        setId = request.query_params.get('setId')
        user, template_xml_string, params = self.getInfo(ip)
        try:
            reply_json_data = self.get_next(ip, user, setId=setId)
            # print('getnext:', reply_json_data)
            setId = reply_json_data['rpc-reply'].get('@set-id')  # 如果不需要分包，则返回None，@set-id: None
            if setId is None:
                data = reply_json_data['rpc-reply']['data']  # 返回装换的json数据
            else:
                # 需要分包处理，返回数据携带到setId
                data = reply_json_data['rpc-reply']['data']
                data['setId'] = setId
        except Exception as e:
            # 下发配置错误需要重新连接设备，保存会话
            # self.restConnect(ip, user)
            print(e)
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'data': data}, status=status.HTTP_200_OK)


