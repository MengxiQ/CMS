# 基于NETCONF的配置管理系统
网络设备的配置管理系统，项目的主要功能是实现对设备的管理，编写配置脚本利用网络配置协议对设备进行配置收集和配置下发；设计友好的客户端方便管理员管理网络设备的降低网络配置复杂度，还实现了网络拓扑图的监控和展示、配置测试工具、批量配置工具（虽然脚本很强大，但是并不方便，鼠标点点比运行脚本和命令行要舒服很多）。

> 暂只支持华为CE12800和CE6800系列的交换机，因为只有这两个型号交换机可在虚拟仿真平台模拟，并且在官网有比较完整的Netconfig API文档。

系统基于简单的模板管理的方法，原理上只要系统中导入模板，设备提供接口，那么系统就可以纳管该设备（实际上大部分厂家并不提供...）

<img src="doc\images\设备列表.png" alt="设备列表" style="zoom:50%;" />
<img src="doc\images\设备列表.png" alt="" style="zoom:50%;" />
<img src="doc\images\拓扑监控和展示.png" alt="" style="zoom:50%;" />
<img src="doc\images\模板管理.png" alt="" style="zoom:50%;" />
<img src="doc\images\批量配置流程.png" alt="" style="zoom:50%;" />
<img src="doc\images\批量配置流程-截图.png" alt="" style="zoom:50%;" />
<img src="doc\images\XML测试工具.png" alt="" style="zoom:50%;" />
<img src="doc\images\模板列表.png" alt="" style="zoom:50%;" />
<img src="doc\images\系统用户管理.png" alt="" style="zoom:50%;" />

## 进入设备的配置界面
<img src="doc\images\config\设备基本信息.png" alt="" style="zoom:50%;" />
<img src="doc\images\config\接口列表.png" alt="" style="zoom:50%;" />
<img src="doc\images\config\接口配置.png" alt="" style="zoom:50%;" />
<img src="doc\images\config\路由配置.png" alt="" style="zoom:50%;" />
<img src="doc\images\config\路由统计分析.png" alt="" style="zoom:50%;" />
<img src="doc\images\config\下发测试任务.png" alt="" style="zoom:50%;" />
<img src="doc\images\config\配置管理.png" alt="" style="zoom:50%;" />
<img src="doc\images\config\设置维护.png" alt="" style="zoom:50%;" />







