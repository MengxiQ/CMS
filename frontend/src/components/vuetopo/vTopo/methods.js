import { createTopology, pingHost } from '@/api/views/topology'

export const methods = {
  methods: {
    GenNonDuplicateID(randomLength) {
      return Number(Math.random().toString().substr(3, randomLength) + Date.now()).toString(36)
    },
    canConnectorTo(curNodeType, connectorToNodeType, connectorType) {
      // 当需要包含和连线规则的时候 清除以下注释
      let canConnector = false
      if (connectorType === 'Link') {
        this.connectorRules.forEach((ele, key) => {
          if (ele.type === curNodeType) {
            ele.canLinkToType.forEach((el, index) => {
              if (el === connectorToNodeType) canConnector = true
            })
          }
        })
      } else if (connectorType === 'Contain') {
        this.connectorRules.forEach((ele, key) => {
          if (ele.type === curNodeType) {
            ele.canBeContainedType.forEach((el, index) => {
              if (el === connectorToNodeType) canConnector = true
            })
          }
        })
      }
      // canConnector = true
      return canConnector
    },
    // 拖拽shapeBar中的node
    dragShapeNode(nodeData, key, event) {
      // console.log(nodeData)
      const NODE = nodeData[key]
      const toolbarName = NODE.type
      // const toolbarIcon = NODE.icon //拖动的图标
      const topoEle = this.$(`#topoId${this.topoId}`)
      const svgOffsetLeft = topoEle.find('.topoSvg').offset().left
      const svgOffsetTop = topoEle.find('.topoSvg').offset().top
      const svgWidth = topoEle.find('.topoSvg').width()
      const svgHeight = topoEle.find('.topoSvg').height()
      let isContainSvgArea = false
      document.onmousemove = (event) => {
        const mouseX = event.clientX // 当前鼠标位置
        const mouseY = event.clientY
        const nodeX = event.clientX - svgOffsetLeft + this.$(document).scrollLeft() + this.svgAttr.viewX // svg最终位置
        const nodeY = event.clientY - svgOffsetTop + this.$(document).scrollTop() + this.svgAttr.viewY
        isContainSvgArea = false
        /**
         * 减去侧边栏宽度 和 头部高度
         * **/
        let sidebarWidht = this.$('#sidebar').width()
        const headerHeight = this.$('#navbar').height()
        const tagViewHeight = this.$('#tags-view-container').height()
        if (window.innerWidth < 1010) {
          sidebarWidht = 0
          // headerHeight = 0
        }
        /**
         * 拖动shapeBar中图表 图标的位置
         * **/
        this.shapebarMoveNode.left = mouseX + 4 + this.$(document).scrollLeft() - sidebarWidht // 鼠标位置 + 文档滚动的距离
        this.shapebarMoveNode.top = mouseY + 4 + this.$(document).scrollTop() - (headerHeight + tagViewHeight)
        this.shapebarMoveNode.name = toolbarName
        // this.shapebarMoveNode.icon = toolbarIcon
        this.shapebarMoveNode.icon = require('@/assets/topo/switch.svg')
        this.shapebarMoveNode.isShow = true
        this.marker.isMarkerShow = false
        // 鼠标滑入svg区域内显示标尺并显示标尺正确位置
        if (mouseX >= svgOffsetLeft &&
          mouseX <= (svgOffsetLeft + svgWidth) &&
          mouseY >= (svgOffsetTop - this.$(document).scrollTop()) &&
          mouseY <= (svgOffsetTop + svgHeight - this.$(document).scrollTop())
        ) {
          this.marker.isMarkerShow = true
          isContainSvgArea = true
          const n1 = Math.floor(nodeX / 20) // grid宽高的整数倍
          const n2 = Math.floor(nodeY / 20)
          this.marker.xmarkerY = n2 * 20
          this.marker.ymarkerX = n1 * 20
        }
      }
      document.onmouseup = (event) => {
        document.onmousemove = null
        document.onmouseup = null
        // 判断鼠标在svg区域
        if (isContainSvgArea) {
          const TOPODATA = this.topoData
          const type = NODE.type
          // let name = NODE.type+'_'+ NODE.num
          const name = NODE.name
          NODE.num++
          const id = GenNonDuplicateID(5)
          const nodeEndX = this.marker.ymarkerX
          const nodeEndY = this.marker.xmarkerY
          const svgNode = {
            name,
            type,
            ip: NODE.ip,
            netype: NODE.netype,
            id: id,
            status: NODE.status,
            x: nodeEndX,
            y: nodeEndY,
            icon: NODE.icon,
            width: NODE.width,
            height: NODE.height,
            initW: NODE.width,
            initH: NODE.height,
            classType: NODE.classType,
            isLeftConnectShow: false,
            isRightConnectShow: false,
            containNodes: [],
            attrs: []
          }
          this.marker.isMarkerShow = false // 标尺取消显示

          // 创建了一个节点
          console.log('添加了一个设备！')
          this.topoData.nodes.push(svgNode) // 创建一个svg Node
          this.toolBarData.splice(key, 1)
          // 计算是否与某个节点重叠
          for (let i = (TOPODATA.nodes.length - 1); i >= 0; i--) {
            const node = TOPODATA.nodes[i]
            if (node.x <= nodeEndX && nodeEndX <= (node.x + node.width) && nodeEndY >= node.y && node.y + node.height >= nodeEndY && node.id !== id) {
              const canBeContain = this.canConnectorTo(NODE.type, node.type, 'Contain') // 判断是否能被包含在目标元素中
              if (canBeContain) {
                const connectorId = this.GenNonDuplicateID(3)
                const connector = {
                  id: connectorId,
                  type: 'Contain',
                  sourceNode: {
                    id: id
                  },
                  targetNode: {
                    id: node.id
                  },
                  isSelect: false
                }
                TOPODATA.connectors.push(connector)
                node.containNodes.push(id) // 如果有嵌套关系，就在父节点放入子节点id
                this.refreshRowAndOuterNode(svgNode) // 刷新并列节点位置和父节点宽高
                this.refreshConnectorsData()
                break
              }
            }
          }
        }
        // 重新初始toolbarMoveNode的值
        this.shapebarMoveNode.left = 0
        this.shapebarMoveNode.top = 0
        this.shapebarMoveNode.name = ''
        this.shapebarMoveNode.icon = ''
        this.shapebarMoveNode.isShow = false
      }

      // 生成唯一id值
      function GenNonDuplicateID(randomLength) {
        return Number(Math.random().toString().substr(3, randomLength) + Date.now()).toString(36)
      }
    },
    // 1.取消选中的node节点 2. 移动viewbox
    mousedownTopoSvg(event) {
      const mouseX0 = event.clientX // 鼠标点击下的位置
      const mouseY0 = event.clientY
      const startViewX = this.svgAttr.viewX
      const startViewY = this.svgAttr.viewY
      const startSvgW = this.svgAttr.width
      const startSvgH = this.svgAttr.height
      const svgMinW = this.svgAttr.minW
      const svgMinH = this.svgAttr.minH
      let selectionBoxX = 0
      let selectionBoxY = 0
      this.cancelAllNodesSelect() // 取消所有节点选中
      this.cancelAllLinksSelect() // 取消连线选中
      if (this.svgToolbar[1].isActive) {
        const topoEle = this.$(`#topoId${this.topoId}`)
        selectionBoxX = event.clientX - topoEle.find('.topoSvg').offset().left + this.$(document).scrollLeft() + this.svgAttr.viewX
        selectionBoxY = event.clientY - topoEle.find('.topoSvg').offset().top + 4 + this.$(document).scrollTop() + this.svgAttr.viewY
        this.selectionBox.isShow = true
        this.selectionBox.x = selectionBoxX
        this.selectionBox.y = selectionBoxY
      }
      // 移动viewbox位置
      document.onmousemove = (event) => {
        const disX = event.clientX - mouseX0
        const disY = event.clientY - mouseY0
        const endSvgW = startSvgW - disX
        const endSvgH = startSvgH - disY

        if (this.svgToolbar[1].isActive) {
          const selectionW = Math.abs(disX)
          const selectionH = Math.abs(disY)
          this.svgAttr.isCrosshair = true
          if (disX <= 0) {
            this.selectionBox.x = selectionBoxX + disX
          } else {
            this.selectionBox.x = selectionBoxX
          }
          if (disY <= 0) {
            this.selectionBox.y = selectionBoxY + disY
          } else {
            this.selectionBox.y = selectionBoxY
          }
          this.selectionBox.width = selectionW
          this.selectionBox.height = selectionH
          return false
        }
        this.svgAttr.isHand = true
        this.svgAttr.viewX = (startViewX <= disX) ? 0 : startViewX - disX // 根据鼠标移动的位移，得到视图移动位移
        this.svgAttr.viewY = (startViewY <= disY) ? 0 : startViewY - disY
        this.svgAttr.width = (endSvgW < svgMinW) ? svgMinW : endSvgW // 动态设置svg宽高
        this.svgAttr.height = (endSvgH < svgMinH) ? svgMinH : endSvgH
        this.marker.xmarkerX = this.svgAttr.width
        this.marker.ymarkerY = this.svgAttr.height
      }
      document.onmouseup = (event) => {
        document.onmousemove = null
        document.onmouseup = null
        this.svgAttr.isHand = false
        this.svgAttr.isCrosshair = false
        // 如果是框选模式
        if (this.svgToolbar[1].isActive) {
          const selectionBoxObj = this.selectionBox
          const sW = selectionBoxObj.width
          const sH = selectionBoxObj.height
          const sX = selectionBoxObj.x
          const sY = selectionBoxObj.y
          this.topoData.nodes.forEach((node, key) => {
            if (sX <= node.x && sY <= node.y && node.x + node.width <= sX + sW && node.y + node.height <= sY + sH) {
              node.isSelect = true
            }
          })
          this.selectionBox.isShow = false
          this.selectionBox.x = 0
          this.selectionBox.y = 0
          this.selectionBox.width = 0
          this.selectionBox.height = 0
        }
      }
    },
    // 拖拽svg中的node
    dragSvgNode(key, node, event) {
      this.isAcitveNode = node
      const CURNODE = this.topoData.nodes[key] // 点击的node对象
      CURNODE.isSelect = true
      this.topoData.nodes.forEach((node, key) => { // 关联属性设置框
        if (node.id === CURNODE.id) {
          this.selectNodeData = node
        }
      })
      // 权限检查
      if (!this.editable) return false // editable[false]（非编辑状态）：svgNode不可移动
      const mouseX0 = event.clientX + this.$(document).scrollLeft()// 鼠标点击下的位置
      const mouseY0 = event.clientY + this.$(document).scrollTop()
      // const CURNODE = this.topoData.nodes[key] // 点击的node对象
      const startX = CURNODE.x // 节点开始位置
      const startY = CURNODE.y
      const curNodeId = CURNODE.id // 当前结点id
      const nodeW = CURNODE.width // 节点 宽高
      const nodeH = CURNODE.height
      const nodeStartPosArr = []
      const moveDis = false
      this.marker.isMarkerShow = true // 显示标尺
      // 把选中的node信息放入数组最后一位，待看结果 可能有bug
      this.topoData.nodes.splice(key, 1)
      this.topoData.nodes.push(CURNODE)
      /** ******优化*********/
      this.putInnerNodeLast(CURNODE) // 递归循环将嵌套节点依次放置，判断包含关系，如果内部有子node，则需要将子node放入数组最后的位置
      // 取消所有节点选中
      this.cancelAllNodesSelect()
      // 取消所有连线选中
      this.cancelAllLinksSelect()
      // 节点选中
      console.log('choice!')
      CURNODE.isSelect = true
      this.storeCurnodeStartPosition(CURNODE, nodeStartPosArr) // 将选择的node的子子节点初始位置保存进去
      this.topoData.nodes.forEach((node, key) => { // 关联属性设置框
        if (node.id === CURNODE.id) {
          this.selectNodeData = node
        }
      })
      document.onmousemove = (event) => {
        let disX = event.clientX - mouseX0 + this.$(document).scrollLeft() // 移动位置
        let disY = event.clientY - mouseY0 + this.$(document).scrollTop()
        let endX = startX + disX // 最终位置
        let endY = startY + disY
        let n1 = Math.floor(endX / 20) // grid宽高的整数倍
        let n2 = Math.floor(endY / 20)
        if (n1 <= 0) n1 = 0
        if (n2 <= 0) n2 = 0
        if (endX <= 0) {
          endX = 0
          disX = -startX
        }
        if (endY <= 0) {
          endY = 0
          disY = -startY
        }
        this.marker.isMarkerShow = true // 显示标尺
        this.marker.xmarkerY = n2 * 20 // 标尺的移动位置，以每格20的距离移动
        this.marker.ymarkerX = n1 * 20
        this.moveContianNode(disX, disY, nodeStartPosArr) // 根据保存的数组数据移动相关节点
        this.refreshConnectorsData() // 及时更新连线数据
      }
      document.onmouseup = (event) => {
        document.onmousemove = null
        document.onmouseup = null
        this.marker.isMarkerShow = false // 隐藏标尺
        const NodeEndX = this.marker.ymarkerX // 最终位置为标尺的位置 最终节点位置
        const NodeEndY = this.marker.xmarkerY
        const disX = NodeEndX - startX
        const disY = NodeEndY - startY
        const mouseDisX = event.clientX - mouseX0
        const mouseDisY = event.clientY - mouseY0
        this.moveContianNode(disX, disY, nodeStartPosArr) // 移动包含着的子节点
        this.drawContainLayout(CURNODE, NodeEndX, NodeEndY, true, nodeStartPosArr, mouseDisX, mouseDisY, startY)
        this.refreshConnectorsData() // 最后刷新连线
      }
    },
    // 绘制contain布局及刷新连线数据
    drawContainLayout(CURNODE, NodeEndX, NodeEndY, isStop, nodeStartPosArr, mouseDisX, mouseDisY, startY) {
      const TOPODATA = this.topoData
      const curNodeId = CURNODE.id
      const nodeW = CURNODE.width
      const nodeH = CURNODE.height
      let originTargetNodeId = '' // 原先的targetNode
      let originTargetNode = {}
      // 预留 ++++ 判断是否能增加包含关系
      const NodePoint1 = [NodeEndX, NodeEndY] // 初始当前节点四个角的位置
      const NodePoint2 = [(NodeEndX + nodeW), NodeEndY]
      const NodePoint3 = [(NodeEndX + nodeW), (NodeEndY + nodeH)]
      const NodePoint4 = [NodeEndX, (NodeEndY + nodeH)]
      // 如果点击的node有contain关系，先记录下targetNode
      TOPODATA.connectors.forEach((ele, key) => {
        if (ele.type === 'Contain' && ele.sourceNode.id === curNodeId) {
          originTargetNodeId = ele.targetNode.id
        }
      })
      if (originTargetNodeId) {
        TOPODATA.nodes.forEach((node, key) => {
          if (node.id === originTargetNodeId) originTargetNode = node
        })
      }
      // 情况一：移出后依然恢复原来的位置，前提：1.移除的距离在一定范围 2.点击的节点有父层包含关系
      const endNodeY = startY + mouseDisY
      if (
        originTargetNode &&
        Math.abs(mouseDisX) <= this.containLeft &&
        endNodeY < originTargetNode.y + originTargetNode.height &&
        endNodeY > originTargetNode.y - CURNODE.height
      ) {
        this.refreshRowAndOuterNode(originTargetNode)
        return false
      }
      // 清除当前node的包含关系
      this.deleteCurNodeContainConnector(CURNODE)
      // 与NodeData对比，判断是否有值与其他Node重合的
      var isContainNode = false
      let overlapTargetNode = {}
      for (let i = (TOPODATA.nodes.length - 1); i >= 0; i--) { // forEach无法跳出循环,暂用for循环
        const targetNode = TOPODATA.nodes[i]
        isContainNode = false // 初始isContainNode为false的值
        if (CURNODE.id !== targetNode.id) { // 排除自身元素
          const minX = targetNode.x
          const maxX = targetNode.x + targetNode.width
          const minY = targetNode.y
          const maxY = targetNode.y + targetNode.height
          const canContianTargetNode = this.canConnectorTo(CURNODE.type, targetNode.type, 'Contain')// 确认是否能被包含
          // 四种包含情况判重合
          if (NodePoint1[0] <= maxX && NodePoint1[0] >= minX && NodePoint1[1] <= maxY && NodePoint1[1] >= minY) isContainNode = true
          if (NodePoint2[0] <= maxX && NodePoint2[0] >= minX && NodePoint2[1] <= maxY && NodePoint2[1] >= minY) isContainNode = true
          if (NodePoint4[0] <= maxX && NodePoint4[0] >= minX && NodePoint4[1] <= maxY && NodePoint4[1] >= minY) isContainNode = true
          if (NodePoint3[0] <= maxX && NodePoint3[0] >= minX && NodePoint3[1] <= maxY && NodePoint3[1] >= minY) isContainNode = true
          if (isContainNode && canContianTargetNode) {
            overlapTargetNode = targetNode
            break
          }
        }
      }
      // 选中的node 有 与其他node 重合
      if (isContainNode) {
        // 关系数组中增加包含关系
        const connectorId = this.GenNonDuplicateID(3)
        const connector = {
          id: connectorId,
          type: 'Contain',
          sourceNode: {
            id: CURNODE.id
          },
          targetNode: {
            id: overlapTargetNode.id
          },
          isSelect: false
        }
        TOPODATA.connectors.push(connector)
        // 如果有嵌套关系，就在父节点放入子节点id
        TOPODATA.nodes.forEach((node, key) => {
          if (node.id == overlapTargetNode.id) node.containNodes.push(CURNODE.id)
        })
        this.refreshRowAndOuterNode(CURNODE) // 刷新并列节点位置和父节点宽高
      }
      // 移动包含着的子节点
      if (isContainNode) {
        nodeStartPosArr.forEach((node, key) => {
          if (node.id == CURNODE.id) {
            const disX = CURNODE.x - node.x
            const disY = CURNODE.y - node.y
            this.moveContianNode(disX, disY, nodeStartPosArr)
          }
        })
      }
      // 如果初始targetNodeId 与现在重合的taregtNodeId不同，让originTargetNode位置重置
      if (originTargetNodeId && originTargetNodeId != overlapTargetNode.id) {
        this.refreshRowAndOuterNode(originTargetNode)
      }
    },
    // 计算是否与其他节点包含
    computedIsContain(CURNODE) {

    },
    // 存入node及其子节点位置信息
    storeCurnodeStartPosition(CURNODE, startNodePosition) {
      const containNodes = CURNODE.containNodes
      startNodePosition.push({ id: CURNODE.id, x: CURNODE.x, y: CURNODE.y })
      if (containNodes.length) {
        containNodes.forEach((nodeId, key) => {
          this.topoData.nodes.forEach((ele, index) => {
            if (ele.id == nodeId) {
              this.storeCurnodeStartPosition(ele, startNodePosition)
            }
          })
        })
      }
    },
    // contain情况下移动子节点位置
    moveContianNode(disX, disY, nodeStartPosArr) {
      nodeStartPosArr.forEach((ele, key) => {
        const storeInfoId = ele.id
        this.topoData.nodes.forEach((node, key) => {
          if (node.id == storeInfoId) {
            node.x = ele.x + disX
            node.y = ele.y + disY
          }
        })
      })
    },
    // 将选中的容器的最内的容器放置在数组最后
    putInnerNodeLast(CURNODE) {
      const curNodeId = CURNODE.id
      this.topoData.connectors.forEach((ele, key) => {
        if (ele.type == 'Contain' && ele.targetNode.id == curNodeId) {
          const childNodeId = ele.sourceNode.id
          this.topoData.nodes.forEach((node, index) => {
            if (node.id == childNodeId) {
              const childNode = node
              this.topoData.nodes.splice(index, 1)
              this.topoData.nodes.push(childNode)
              this.putInnerNodeLast(childNode)
            }
          })
        }
      })
    },

    // 清除当前选中元素的Contain关系
    deleteCurNodeContainConnector(CURNODE) {
      const curNodeId = CURNODE.id
      this.topoData.connectors.forEach((ele, key) => {
        if (ele.type == 'Contain' && ele.sourceNode.id == curNodeId) {
          const targetNodeId = ele.targetNode.id
          // 1.删除cennetors关系
          this.topoData.connectors.splice(key, 1)
          // 2.删除contains 里面的关系
          this.topoData.nodes.forEach((node, key) => {
            if (node.id == targetNodeId) {
              if (node.containNodes.lengthconnector) {
                node.containNodes.forEach((ele, key) => {
                  const targetNode = node
                  if (ele == curNodeId) {
                    targetNode.containNodes.splice(key, 1)
                  }
                })
              }
            }
          })
        }
      })
    },
    // 刷新外部node的宽度（递归） 且 刷新右侧所欲并列节点宽度
    refreshOuterNodeWidth(CURNODE) {
      this.topoData.connectors.forEach((ele, key) => {
        if (ele.sourceNode.id == CURNODE.id && ele.type == 'Contain') {
          const targetNodeId = ele.targetNode.id
          this.topoData.nodes.forEach((node, index) => {
            if (node.id == targetNodeId) {
              node.width = 2 * this.containLeft + CURNODE.width
              node.height = 10 + CURNODE.height + this.containTop
              this.refreshOuterNodeWidth(node)
            }
          })
        }
      })
    },
    // 刷新父节点的宽度 及 其子节点位置
    refreshRowAndOuterNode(TARGETNODE) {
      if (TARGETNODE.containNodes.length > 0) {
        // 重新计算targetnode的宽度
        let sumWidth = 0
        let maxHeight = 0
        TARGETNODE.containNodes.forEach((ele, key) => {
          const containNodeId = ele
          this.topoData.nodes.forEach((node, index) => {
            if (node.id == containNodeId) {
              sumWidth += node.width
              if (node.height > maxHeight) maxHeight = node.height
            }
          })
        })
        sumWidth += (TARGETNODE.containNodes.length + 1) * this.containLeft
        TARGETNODE.width = sumWidth
        TARGETNODE.height = maxHeight + 10 + this.containTop
      } else {
        TARGETNODE.width = TARGETNODE.initW
        TARGETNODE.height = TARGETNODE.initH
      }
      this.topoData.connectors.forEach((ele, key) => {
        let parentNodeId = ''
        const parentNode = {}
        if (ele.sourceNode.id == TARGETNODE.id && ele.type == 'Contain') {
          parentNodeId = ele.targetNode.id
          this.topoData.nodes.forEach((node, key) => {
            if (node.id == parentNodeId) this.refreshRowAndOuterNode(node)
          })
        }
      })

      // 重新计算每个containNode的位置
      this.refreshContainNodesPosition(TARGETNODE)
    },
    // 计算每个containNode的位置
    refreshContainNodesPosition(TARGETNODE) {
      TARGETNODE.containNodes.forEach((ele, key) => {
        const containNodeId = ele
        let containNode
        let preNode
        this.topoData.nodes.forEach((node, index) => {
          if (node.id == containNodeId) {
            containNode = node
          }
        })
        if (key == 0) {
          this.refreshRowNodesPosition(TARGETNODE, containNode, null)
        } else {
          const preNodeIndex = key - 1
          const preNodeId = TARGETNODE.containNodes[preNodeIndex]
          this.topoData.nodes.forEach((node, index) => {
            if (node.id == preNodeId) preNode = node
          })
          this.refreshRowNodesPosition(TARGETNODE, containNode, preNode)
        }
      })
    },
    // 计算并列的nodes位置
    refreshRowNodesPosition(TARGETNODE, CURNODE, PRENODE) {
      if (PRENODE != null) {
        CURNODE.x = PRENODE.x + PRENODE.width + this.containLeft
      } else {
        CURNODE.x = TARGETNODE.x + this.containLeft
      }
      CURNODE.y = TARGETNODE.y + this.containTop
      this.refreshContainNodesPosition(CURNODE)
    },

    // 刷新连线数据
    refreshConnectorsData() {
      this.topoData.connectors.forEach((item, index) => {
        // 更新connectors里的数据
        this.topoData.nodes.forEach((node, key) => {
          if (item.sourceNode.id == node.id) {
            item.sourceNode.width = node.width
            item.sourceNode.height = node.height
            item.sourceNode.x = node.x
            item.sourceNode.y = node.y
          }
          if (item.targetNode.id == node.id) {
            item.targetNode.width = node.width
            item.targetNode.height = node.height
            item.targetNode.x = node.x
            item.targetNode.y = node.y
          }
        })
      })
    },

    // 动态绘制连线
    drawConnectLine(key, event) {
      if (!this.editable) return false // 如果非编辑状态，不可连线
      const CONNECTLINE = this.connectingLine // 绘制连线对象
      const CURNODE = this.topoData.nodes[key] // 当前点击node
      const nodeW = CURNODE.width // 当前node宽高
      const nodeH = CURNODE.height
      const sourceNodeIP = CURNODE.ip
      const sourceNodeX = CURNODE.x
      const sourceNodeY = CURNODE.y
      const mouseX0 = event.clientX
      const mouseY0 = event.clientY
      const topoEle = this.$(`#topoId${this.topoId}`)
      const x1 = event.clientX - topoEle.find('.topoSvg').offset().left - 2 + this.$(document).scrollLeft() + this.svgAttr.viewX // 连线开始位置的位置：鼠标点击的实际位置   为鼠标位置 - 当前元素的偏移值
      const y1 = event.clientY - topoEle.find('.topoSvg').offset().top + 4 + this.$(document).scrollTop() + this.svgAttr.viewY
      CONNECTLINE.isConnecting = true // 显示绘制连线
      CONNECTLINE.x1 = x1
      CONNECTLINE.y1 = y1
      CONNECTLINE.x2 = x1 // 连线终点同样赋值为起点值
      CONNECTLINE.y2 = y1
      CONNECTLINE.sourceNode = CURNODE.id // 将当前点击nodeid值赋给连线起点
      document.onmousemove = (event) => {
        const disX = event.clientX - mouseX0
        const disY = event.clientY - mouseY0
        const x2 = x1 + disX
        const y2 = y1 + disY
        CURNODE.isRightConnectShow = true
        CONNECTLINE.x2 = x2
        CONNECTLINE.y2 = y2
      }
      document.onmouseup = () => {
        document.onmousemove = null
        document.onmouseup = null
        let hasConnected = false // 标记是否已经有过连线
        const CONNECTORS = this.topoData.connectors
        const sourceNodeW = nodeW
        const sourceNodeH = nodeH
        let targetNodeIP = '' // 目标节点相关信息
        let targetNodeW = 0
        let targetNodeH = 0
        let targetNodeX = 0
        let targetNodeY = 0
        let targetNodeType = ''
        let connectType = ''
        if (CONNECTLINE.endNode) { // 正确连线：添加连线信息在connectors中
          // 判断是否有已经有连线的情况
          CONNECTORS.forEach((item, index) => {
            if (item.sourceNode.id == CURNODE.id && item.targetNode.id == CONNECTLINE.endNode && item.type == 'Line') {
              hasConnected = true
            }
          })
          // 未连线情况下增加两者连线
          if (!hasConnected) {
            connectType = 'Line'
            // 获取目标节点宽高
            this.topoData.nodes.forEach((item, index) => {
              if (item.id === CONNECTLINE.endNode) {
                targetNodeIP = item.ip
                targetNodeW = item.width
                targetNodeH = item.height
                targetNodeX = item.x
                targetNodeY = item.y
                targetNodeType = item.type
              }
            })
            const canLinkToTargetNode = this.canConnectorTo(CURNODE.type, targetNodeType, 'Link')
            if (!canLinkToTargetNode) {
              this.$message({
                showClose: true,
                message: CURNODE.type + '类型 不能连接 ' + targetNodeType + '类型',
                type: 'error'
              })
              CURNODE.isRightConnectShow = false // 连线失败：起点右侧箭头暂且设置为消失
              CONNECTORS.forEach((item, key) => { // 连线判断，如果已经有连线起点为当前的node，将起点箭头设置为显示
                this.topoData.nodes.forEach((node, key) => {
                  if (node.id === item.sourceNode.id && item.type === 'Line') node.isRightConnectShow = true
                })
              })
            } else {
              // 类型：包含
              const connectorId = this.GenNonDuplicateID(3)
              /**
               * 创建连接对象
               * **/
              const connector = {
                id: connectorId,
                type: connectType,
                strokeW: 3, // 仅用于Line类型,默认3
                color: this.lineDefaultColor, // 仅用于Line类型，默认颜色
                targetNode: {
                  ip: targetNodeIP,
                  x: targetNodeX,
                  y: targetNodeY,
                  id: CONNECTLINE.endNode,
                  width: targetNodeW,
                  height: targetNodeH,
                  port: ''
                },
                sourceNode: {
                  ip: sourceNodeIP,
                  x: sourceNodeX,
                  y: sourceNodeY,
                  id: CURNODE.id,
                  width: sourceNodeW,
                  height: sourceNodeH,
                  port: ''
                }
              }
              CURNODE.isRightConnectShow = true
              this.topoData.nodes.forEach((item, key) => {
                if (item.id == CONNECTLINE.endNode) item.isLeftConnectShow = true
              })
              CONNECTORS.push(connector)
            }
          }
        } else {
          CURNODE.isRightConnectShow = false // 连线失败：起点右侧箭头暂且设置为消失
          CONNECTORS.forEach((item, key) => { // 连线判断，如果已经有连线起点为当前的node，将起点箭头设置为显示
            this.topoData.nodes.forEach((node, key) => {
              if (node.id == item.sourceNode.id && item.type == 'Line') node.isRightConnectShow = true
            })
          })
        }
        // 绘制连线恢复初始值
        CONNECTLINE.x1 = 0
        CONNECTLINE.y1 = 0
        CONNECTLINE.x2 = 0
        CONNECTLINE.y2 = 0
        CONNECTLINE.isConnecting = false
        CONNECTLINE.sourceNode = ''
        CONNECTLINE.endNode = ''
      }
    },
    // 鼠标滑过node
    mouseoverNode(key, event) {
      this.marker.xmarkerY = this.topoData.nodes[key].y
      this.marker.ymarkerX = this.topoData.nodes[key].x
      this.getConnectLine(key)
    },
    // 获取连线终点时的node的ID值
    getConnectLine(key) {
      this.connectingLine.endNode = this.topoData.nodes[key].id
    },
    // 鼠标划出左侧箭头时，将connectingLine.endNode再次初始化
    mouseoutLeftConnector(key) {
      this.connectingLine.endNode = ''
    },
    // 点击选中连线
    selectConnectorLine(key) {
      // if (!this.editable) return false // 如果非编辑状态 不可点击
      const connectors = this.topoData.connectors
      const nodes = this.topoData.nodes
      const selectLine = this.topoData.connectors[key]
      const lastIndex = connectors.length - 1
      connectors.splice(key, 1)
      connectors.push(selectLine)
      // 取消所有选中样式
      this.cancelAllNodesSelect()
      this.cancelAllLinksSelect()
      selectLine.isSelect = true
      this.$set(connectors, lastIndex, selectLine)
      this.selectNodeData = selectLine // 将点击的连线信息赋值给属性面板
    },
    // 取消所有节点选中
    cancelAllNodesSelect() {
      this.topoData.nodes.forEach((ele, key) => {
        ele.isSelect = false
        this.$set(this.topoData.nodes, key, ele)
      })
      this.selectNodeData = {}
    },
    // 取消所有连线选中
    cancelAllLinksSelect() {
      this.topoData.connectors.forEach((ele, key) => {
        ele.isSelect = false
        this.$set(this.topoData.connectors, key, ele)
      })
      this.selectNodeData = {}
    },
    // 删除node节点及其关系
    deleteNodeAndConnetor() {
      document.onkeydown = (event) => {
        const keycode = event.which // 键盘值
        // 在mac上del的keycode是8,这样又会引起win下输入backspace也会删除
        // if(keycode == 46 || keycode == 8) {
        if (keycode === 46) {
          // 单节点和多选删除节点
          for (let i = 0; i < this.topoData.nodes.length; i++) {
            const node = this.topoData.nodes[i]

            if (node.isSelect) {
              // 将node添加回Shapebar中
              // let node_data = {
              //   type: 'ApplicationModule',
              //   icon: require('@/assets/topo/application.png'),
              //   width: 50, height: 50, num: 1,
              //   classType: node.classType,
              //   name: node.name
              // }
              const node_data = node
              this.toolBarData.push(node_data)

              this.deleteSelectNodeLink(node.id)
              let targetNodeId = ''
              const targetNode = null
              this.topoData.connectors.forEach((ele, key) => {
                if (ele.sourceNode.id == node.id) targetNodeId = ele.targetNode.id
              })
              this.deleteCurNodeContainConnector(node)
              if (targetNodeId) {
                this.topoData.nodes.forEach((node, index) => {
                  if (node.id == targetNodeId) {
                    this.refreshRowAndOuterNode(node)
                  }
                })
              }
              this.topoData.nodes.splice(i, 1)
              // 删除包含关系1.如果有父元素，恢复父元素的宽高位置
              this.deleteCurnodeAndChildnodes(node) // 删除此节点内部所有包含的节点及其关系
              this.refreshNodeArrows() // 刷新节点的左右箭头展示
              i--
              if (this.topoData.nodes.length > 0) {
                this.selectNodeIndex =
                  this.selectNodeData = {}
              } else {
                this.selectNodeIndex = null
                this.selectNodeData = {}
                this.isTopoAttrShow = false
              }
            }
          }

          // 单选删除连线功能
          this.topoData.connectors.forEach((ele, key) => {
            if (ele.isSelect) {
              this.topoData.connectors.splice(key, 1)
              this.refreshNodeArrows()// 重新绘制node节点左右箭头
            }
          })

          this.refreshConnectorsData()
        }
      }
    },
    // 删除选中node的连线
    deleteSelectNodeLink(selectId) {
      const connectorObjArr = this.topoData.connectors
      let connectorsLen = connectorObjArr.length
      for (let i = 0; i < connectorsLen; i++) {
        const connectorObj = connectorObjArr[i]
        // 删除连线
        if (connectorObj.type == 'Line' && (connectorObj.sourceNode.id == selectId || connectorObj.targetNode.id == selectId)) {
          this.topoData.connectors.splice(i, 1)
          i--
          connectorsLen--
        }
      }
    },
    // 删除此节点下所有包含的所有节点
    deleteCurnodeAndChildnodes(CURNODE) {
      this.deleteCurNodeContainConnector(CURNODE)
      if (CURNODE.containNodes.length) {
        CURNODE.containNodes.forEach((containNodeId, key) => {
          const containId = containNodeId
          this.topoData.nodes.forEach((ele, index) => {
            if (ele.id == containId) {
              const curnode = ele
              this.topoData.nodes.splice(index, 1)
              this.deleteSelectNodeLink(containId)
              this.deleteCurnodeAndChildnodes(curnode) // 递归删除内部所有的节点及其关系
            }
          })
        })
      }
    },
    // 重新绘制node节点左右箭头
    refreshNodeArrows() {
      this.topoData.nodes.forEach((topoNode, index) => {
        topoNode.isLeftConnectShow = false
        topoNode.isRightConnectShow = false
      })
      this.topoData.connectors.forEach((ele, key) => {
        const sourceNodeId = ele.sourceNode.id
        const targetNodeId = ele.targetNode.id
        if (ele.type === 'Line') {
          this.topoData.nodes.forEach((topoNode, index) => {
            if (topoNode.id === targetNodeId) topoNode.isLeftConnectShow = true
            if (topoNode.id === sourceNodeId) topoNode.isRightConnectShow = true
          })
        }
      })
    },
    // svg工具栏选择工具
    selectToolbar(key) {
      this.svgToolbar.forEach((ele, key) => {
        ele.isActive = false
      })
      this.svgToolbar[key].isActive = true
    },
    // 保存topo的json数据
    saveTopoJson() {
      // this.$store.commit('saveTopo', this.topoData)
      // console.log(this.topoData)
      const data = {
        name: this.topoData.name,
        nodes: JSON.stringify(this.topoData.nodes),
        connectors: JSON.stringify(this.topoData.connectors)
      }
      if (data.name === undefined || data.name === '') {
        this.$message({ type: 'error', message: '请输入topo名称。' })
      } else {
        createTopology(data).then(res => {
          this.$message({ type: 'success', message: '保存成功。' })
          this.$emit('savesuccess')
        }).catch(error => {
          console.log(error)
          this.$message({ type: 'error', message: '保存失败。' })
        })
      }
      // console.log(JSON.stringify(this.topoData))
    },
    saveTopoImage() {
      let maxW = 0
      let maxH = 0
      const initW = this.svgAttr.width
      const initH = this.svgAttr.height
      this.topoData.nodes.forEach((node, key) => {
        const nodeEndX = node.width + node.x
        const nodeEndY = node.height + node.y
        if (nodeEndX > maxW) maxW = nodeEndX
        if (nodeEndY > maxH) maxH = nodeEndY
      })
      maxW = (maxW < this.svgAttr.minW) ? this.svgAttr.minW : maxW
      maxH = (maxH < this.svgAttr.minH) ? this.svgAttr.minH : maxH
      this.svgAttr.width = maxW + 50
      this.svgAttr.height = maxH + 20
      saveSvgAsPng(document.getElementById('topoSvg'), 'topo.png')
      // 建议使用promise进行优化
      setTimeout(() => {
        this.svgAttr.width = initW
        this.svgAttr.height = initH
      }, 1000)
    },
    // 初始化获取topo组件宽高
    initTopoWH() {
      this.$nextTick(() => {
        // let width = this.this.$refs.topoWrap.offsetWidth - 2
        // let height = this.this.$refs.topoWrap.offsetHeight - 2
        const ele = `#topoId${this.topoId}`
        const topoW = this.$(ele).width()
        const topoH = this.$(ele).height()
        this.marker.xmarkerX = topoW
        this.marker.ymarkerY = topoH
        this.svgAttr.width = topoW
        this.svgAttr.height = topoH
        this.svgAttr.minW = topoW
        this.svgAttr.minH = topoH
        // this.marker.xmarkerX = width
        // this.marker.ymarkerY = height
        // this.svgAttr.width = width
        // this.svgAttr.height = height
        // this.svgAttr.minW = width
        // this.svgAttr.minH = height
      })
    },

    /** 自定义添加的代码**/
    // 点击保存
    clickSave() {
      this.saveTopoJson()
    },
    // 右键删除
    RCdelete() {
      // 遍历所有元素，删除被选中的元素
      for (let i = 0; i < this.topoData.nodes.length; i++) {
        const node = this.topoData.nodes[i]

        if (node.isSelect) {
          this.$message({
            message: '删除节点成功。',
            type: 'success'
          })
          // 将node添加回Shapebar中
          // let node_data = {
          //   type: 'ApplicationModule',
          //   icon: require('@/assets/topo/application.png'),
          //   width: 50, height: 50, num: 1,
          //   classType: node.classType,
          //   name: node.name
          // }
          const node_data = node
          console.log(node)
          this.toolBarData.push(node_data)

          this.deleteSelectNodeLink(node.id)
          let targetNodeId = ''
          this.topoData.connectors.forEach((ele, key) => {
            if (ele.sourceNode.id === node.id) targetNodeId = ele.targetNode.id
          })
          this.deleteCurNodeContainConnector(node)
          if (targetNodeId) {
            this.topoData.nodes.forEach((node, index) => {
              if (node.id === targetNodeId) {
                this.refreshRowAndOuterNode(node)
              }
            })
          }
          this.topoData.nodes.splice(i, 1)
          // 删除包含关系1.如果有父元素，恢复父元素的宽高位置
          this.deleteCurnodeAndChildnodes(node) // 删除此节点内部所有包含的节点及其关系
          this.refreshNodeArrows() // 刷新节点的左右箭头展示
          i--
          if (this.topoData.nodes.length > 0) {
            this.selectNodeIndex =
              this.selectNodeData = {}
          } else {
            this.selectNodeIndex = null
            this.selectNodeData = {}
            this.isTopoAttrShow = false
          }
        }
      }
    },
    handleConfig() {
      const ip = this.isAcitveNode.ip
      if (this.isAcitveNode.status === '在线') {
        const URL = this.$router.resolve({
          path: '/equipmentsManage/detail/' + ip
        })
        window.open(URL.href, '_blank')
        // this.$router.push({ path: '/equipmentsManage/detail/' + ip })
      } else {
        this.$message({ type: 'info', message: '无法配置：' + ip + '  ，状态：[' + this.isAcitveNode.status + '].' })
      }
    },
    handlePing() {
      const ip = this.isAcitveNode.ip
      if (ip !== undefined) {
        // 遍历所有元素，查找被选中的元素
        const notify = this.$notify({
          title: 'ping',
          message: '<i class="el-icon-loading"></i><span>ping ' + ip + '...</span>',
          duration: 0,
          dangerouslyUseHTMLString: true,
          showClose: false
        })
        // for (let i = 0; i < this.topoData.nodes.length; i++) {
        //   const node = this.topoData.nodes[i]
        //   if (node.isSelect) {
        //     ip = node.ip
        //   }
        // }
        const data = {
          ip: ip
        }
        // this.$message('ping')
        pingHost(data).then(res => {
          let lis = ''
          res.data.forEach(item => {
            lis += '<li>' + item + '</li>'
          })
          const ul = '<ul>' + lis + '</ul>'
          this.$message({
            customClass: 'pingMessage',
            dangerouslyUseHTMLString: true,
            duration: 0,
            showClose: true,
            message: ul
          })
          notify.close()
        }).catch(error => {
          console.log(error)
          this.$message({ type: 'error', message: 'ping失败！' })
          notify.close()
        })
      } else {
        this.$message({ type: 'warning', message: '没有选中设备。' })
      }
    },
    // 监听改变显示属性面板
    changeShowPanel(val) {
      this.isShowPanel = val
    },
    // 点击右键
    RClick(event) {
      // console.log(this.selectNodeData,this.selectNodeIndex)

      // 判断是否有选中节点
      // menu  1. 有选中的节点则显示不同的右键菜单
      const editItems = [{
        label: '删除',
        minWidth: 0,
        icon: 'el-icon-delete',
        onClick: () => this.RCdelete()
      },
      // {
      //   label: '添加连接关系',
      //   minWidth: 0,
      //   onClick: () => {
      //     this.flag.addConnectVisible = true
      //   }
      // },
      {
        label: '节点属性',
        minWidth: 0,
        onClick: () => {
          this.isShowPanel = true
        }
      }
      ]
      const viewItems = [
        {
          label: '配置',
          minWidth: 0,
          onClick: () => this.handleConfig()
        },
        {
          label: 'ping',
          minWidth: 0,
          onClick: () => this.handlePing()
        },
        // {
        //   label: '高级ping',
        //   minWidth: 0,
        //   onClick: () => {
        //     this.$message('传递ip地址，打开ping窗口')
        //   }
        // },
        // {
        //   label: 'tracer',
        //   minWidth: 0,
        //   onClick: () => {
        //     this.$message('tracer')
        //   }
        // },
        {
          label: '节点属性',
          minWidth: 0,
          onClick: () => {
            this.isShowPanel = true
          }
        }
      ]
      this.$contextmenu({
        items: this.editable ? editItems : viewItems,
        event,
        customClass: 'class-a',
        minWidth: 0
      })
    },
    // 关闭添加连接窗口
    handleCloseAddConnect(done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done()
          // 点击确认关闭
          // 清空暂存的数据
          this.connectorTemp = { // 暂时保存新增连接信息
            'id': '',
            'type': 'Line',
            'strokeW': 2,
            'color': '#9AC0EE',
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
          }
        })
        .catch(_ => {

        })
    },

    /**
     * 网络请求
     * **/
    // 查询目标设备的接口
    SearchInterfacesById(id, param) {
      // 触发焦点事件 value dom为event事件
      // 触发远程搜索事件, 则为输入的值
      /**
       * ???
       * 1. 监听值的变化？
       * 2. 或者监听点击了选择框？
       * **/

      console.log('loading...', id)
      // 根据id查找到ip
      // console.log('id：'+id)
      // console.log(this)
      let ip = ''
      // console.log(this.connectorTemp.sourceNode)
      // 根据id 查询到指定的node的ip
      this.topoData.nodes.forEach(item => {
        if (item.id === id) {
          ip = item.ip
          return ip
        }
      })
      // console.log('ip', ip)

      if (ip !== '' && ip !== null) {
        // 根据ip向后台查询接口
        this[param] = [
        ]
      } else {
        this.$message({ type: 'warning', message: '请先选择设备！' })
      }
    },
    // 监听选择了那些设备
    selectedEquipment(data) {
      // console.log(data)
      this.toolBarData = data
    }
  }
}
