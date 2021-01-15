from CMS.apps.detail.views.Generics.Connector import Connector
from CMS.apps.equipment.models import Networkequipment


class ConfigMangeGenerics(Connector):
    # 设备详情配置管理通用类
    def commit(self, ip, options):
        try:
            equipment = Networkequipment.objects.get(ip=ip)
            user = equipment.user
        except Exception as e:
            print(e)
            raise Exception('查找不到指定IP的用户：' + str(e))
        try:
            m = self.connect(ip=ip, user=user)
            if options.get('attempt') is True:
                # 提交试运行
                persist = options.get('persist')
                if persist is None or persist == '':
                    persist = None
                m.commit(confirmed=options.get('attempt'), timeout=options.get('timeout'), persist=persist)
            else:
                # 提交非试运行
                persist_id = options.get('persist_id')
                if persist_id is not None and persist_id != '':
                    # 提交连接断开前的试运行
                    print(persist_id is None)
                    m.commit(confirmed=True, persist_id=persist_id)
                else:
                    # 直接提交，或直接提交当前连接试运行
                    print(' 直接提交，或直接提交当前连接试运行')
                    m.commit()
        except Exception as e:
            print(e)
            raise Exception(e)
