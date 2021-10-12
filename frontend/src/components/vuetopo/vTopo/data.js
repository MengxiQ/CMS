import connectorRules from '@/components/vuetopo/config/connectorRules' // 连线包含关系规则
export const data = {
  data() {
    return {
      isAcitveNode: {}, // 保存鼠标左右键点击的点
      lineDefaultColor: '#6699CC',
      svgMainKey: 0,
      isShowPanel: false, // 是否在外面强制显示属性框
      sourceInterfacesLoading: true, // 是否显示加载源接口
      connectorTemp: { // 暂时保存新增连接信息
        'id': '',
        'type': 'Line',
        'strokeW': 2,
        'color': '',
        'targetNode': {
          'x': 0,
          'y': 0,
          'id': '',
          'width': 50,
          'height': 50,
          'ip': '',
          'port': ''
        },
        'sourceNode': {
          'x': 0,
          'y': 0,
          'id': '',
          'width': 0,
          'height': 0,
          'ip': '',
          'port': ''
        },
        'isSelect': true
      },
      sourceInterfaces: [],
      targetInterfaces: [],
      flag: {
        isEditName: false,
        addConnectVisible: false
      },
      toolBarData: [],
      keyFormRules: {
        key: [
          { required: true, message: '请输入key值', trigger: 'blur' }
        ],
        value: [
          { required: true, message: '请输入value值', trigger: 'blur' }
        ]
      },
      connectorRules: connectorRules, // 节点间关系的规则
      selectNodeData: {},
      selectNodeIndex: 0,
      topoId: '',
      svgAttr: { width: 0, height: 0, isHand: false, viewX: 0, viewY: 0, minW: 0, minH: 0, isCrosshair: false },
      activeNames: ['1'],
      svgToolbar: [
        { name: '默认模式', className: 'toolbar-default', isActive: true, iron: 'el-icon-position' },
        { name: '框选模式', className: 'toolbar-rectangle_selection', isActive: false, iron: 'el-icon-crop' }
        // {name:'放大',className:'toolbar-zoomin',isActive:false},
        // {name:'缩小',className:'toolbar-zoomout',isActive:false},
        // {name:'恢复出厂设置',className:'toolbar-zoomreset',isActive:false}
      ],
      shapebarMoveNode: {
        left: 0,
        top: 0,
        name: '',
        icon: '',
        isShow: false
      },
      svgTopo: {
        isMoveover: false
      },
      selectionBox: {
        x: 0,
        y: 0,
        width: 0,
        height: 0,
        isShow: false
      },
      connectorWSelf: 15, // 自连连线的宽度
      connectorW: 15, // 非自连连线宽度
      containTop: 30, // 包含关系的子node距离父node
      containLeft: 22, // 包含关系的左右距离
      classchoose: false,
      connectingLine: {
        x1: 0,
        y1: 0,
        x2: 0,
        y2: 0,
        isConnecting: true,
        sourceNode: '',
        endNode: ''
      },
      marker: {
        xmarkerY: 0,
        xmarkerX: 0,
        ymarkerX: 0,
        ymarkerY: 0,
        isMarkerShow: false
      },
      gridData: [
        { x1: 0, x2: 100, y1: 20, y2: 20, color: '#c0c0c0', strokeWidth: 1, opacity: 0.3, id: 1 },
        { x1: 0, x2: 100, y1: 40, y2: 40, color: '#c0c0c0', strokeWidth: 1, opacity: 0.3, id: 2 },
        { x1: 0, x2: 100, y1: 60, y2: 60, color: '#c0c0c0', strokeWidth: 1, opacity: 0.3, id: 3 },
        { x1: 0, x2: 100, y1: 80, y2: 80, color: '#c0c0c0', strokeWidth: 1, opacity: 0.3, id: 4 },
        { x1: 20, x2: 20, y1: 0, y2: 100, color: '#c0c0c0', strokeWidth: 1, opacity: 0.3, id: 5 },
        { x1: 40, x2: 40, y1: 0, y2: 100, color: '#c0c0c0', strokeWidth: 1, opacity: 0.3, id: 6 },
        { x1: 60, x2: 60, y1: 0, y2: 100, color: '#c0c0c0', strokeWidth: 1, opacity: 0.3, id: 7 },
        { x1: 80, x2: 80, y1: 0, y2: 100, color: '#c0c0c0', strokeWidth: 1, opacity: 0.3, id: 8 },
        { x1: 100, x2: 100, y1: 0, y2: 100, color: '#c0c0c0', strokeWidth: 2, opacity: 0.6, id: 9 },
        { x1: 0, x2: 100, y1: 100, y2: 100, color: '#c0c0c0', strokeWidth: 2, opacity: 0.6, id: 10 }
      ]
    }
  }
}
