<!--
 * @Author: caojing
 * @Date: 2017-10-20 09:29:55
 * @LastEditors: weilixing
 * @LastEditTime: 2020-11-25 10:57:15
 -->
<template>
  <div class="topoComponent">
    <!-- 头部标题栏-->
    <div v-show="editable" class="svgHead">
      <ul class="svgHeadItemLst">
        <li
          v-for="(ele,key) in svgToolbar"
          :key="ele.className"
          class="svgHeadItem"
          :class="{'active':ele.isActive}"
          :title="ele.name"
          @mousedown="selectToolbar(key)"
        >
          <i class="svgHeadItemImg" :class="ele.iron " />
        </li>
<!--        <li class="svgHeadItem" title="重新渲染" @click="svgMainKey += 1"><i class="el-icon-refresh" /></li>-->
      </ul>
      <!--      <span style="font-size: 14px">{{ topoData.name }}</span>-->
      <label style="font-size: 12px; font-weight: normal">名称：<el-input v-model="topoData.name" style="width: 180px" size="mini" /></label>
      <ul class="svgHeadItemLst">
        <el-popconfirm title="是否保存该拓扑？" @onConfirm="clickSave">
          <el-button slot="reference" icon="el-icon-finished" type="primary" size="mini">保存</el-button>
        </el-popconfirm>
      </ul>
    </div>
    <div class="svgMain">
      <!--  左侧侧边栏-->
      <v-shapebar
        v-show="editable"
        :shape-node-lst-data="toolBarData"
        @selected="selectedEquipment"
        @click="dragShapeNode"
      />

      <div :id="'topoId'+topoId" ref="topoWrap" class="topoWrap" @contextmenu.prevent="RClick">
        <svg
          class="topoSvg"
          :width="svgAttr.width"
          :height="svgAttr.height"
          :viewBox="svgAttr.viewX+' '+svgAttr.viewY+' '+svgAttr.width+' '+svgAttr.height"
          :class="{'hand':svgAttr.isHand,'crosshair':svgAttr.isCrosshair}"
          @mousedown.stop="mousedownTopoSvg($event)"
        >
          <defs>
            <pattern id="Pattern" x="0" y="0" width="100" height="100" patternUnits="userSpaceOnUse">
              <line
                v-for="ele in gridData"
                :key="ele.id"
                :x1="ele.x1"
                :x2="ele.x2"
                :y1="ele.y1"
                :y2="ele.y2"
                :stroke="ele.color"
                :stroke-width="ele.strokeWidth"
                :opacity="ele.opacity"
              />
            </pattern>
          </defs>
          <!-- 节点和连线 的阴影-->
          <!-- 连线的阴影导致的出现选中状态下连线消失的bug -->
          <defs>
            <filter id="f1" x="0" y="0" width="200%" height="200%">
              <feOffset result="offOut" in="SourceGraphic" dx="4" dy="4" />
              <feColorMatrix
                result="matrixOut"
                in="offOut"
                type="matrix"
                values="0.2 0 0 0 0 0 0.2 0 0 0 0 0 0.2 0 0 0 0 0 1 0"
              />
              <feGaussianBlur result="blurOut" in="matrixOut" stdDeviation="2" />
              <feBlend in="SourceGraphic" in2="blurOut" mode="normal" />
            </filter>
          </defs>
          <rect fill="url(#Pattern)" :width="svgAttr.width" :height="svgAttr.height" />
          <g>
            <!-- node间关系连线connectorsG -->
            <!-- 改变线条是否显示在node的下面还是上面：原理：连接g标签在节点之上，则显示在下方，反之；增加属性判断显示上面的还是下面的g连线            -->
            <g
              v-for="(ele,key) in topoData.connectors"
              v-if="ele.type === 'Line'"
              :key="ele.id"
              class="connectorsG"
              :class="{active:ele.isSelect}"
              @mousedown.stop="selectConnectorLine(key)"
            >
              <g v-if="ele.status === '在线'">
                <!-- 连接线（直线）-->
                <line
                  class="connectorLine"
                  :stroke-width="ele.strokeW"
                  :stroke="ele.color"
                  :x1="ele.sourceNode.x + (ele.sourceNode.width/2) "
                  :y1="ele.sourceNode.y + (ele.sourceNode.height/2)"
                  :x2="ele.targetNode.x + (ele.targetNode.width/2)"
                  :y2="ele.targetNode.y + (ele.targetNode.height/2)"
                />
                <!--流动的连接线-->
                <g v-if="!editable">
                  <defs>
                    <marker
                      id="arrow"
                      markerWidth="10"
                      markerHeight="10"
                      orient="auto"
                      markerUnits="strokeWidth"
                      refX="0"
                      refY="2"
                    >
                      <path d="M0,0 L0,4 L5,2 z" fill="#336699" />
                    </marker>
                  </defs>
                  <line
                    class="connectorLine"
                    :stroke-width="ele.strokeW"
                    :stroke="ele.color"
                    :x1="ele.sourceNode.x + (ele.sourceNode.width/2) "
                    :y1="ele.sourceNode.y + (ele.sourceNode.height/2)"
                    :x2="ele.sourceNode.x + (ele.targetNode.x - ele.sourceNode.x)/2 + (ele.targetNode.width/2)"
                    :y2="ele.sourceNode.y + (ele.targetNode.y - ele.sourceNode.y)/2 + (ele.targetNode.height/2)"
                    marker-end="url(#arrow)"
                  >
                    <animate
                      attributeName="x2"
                      begin="0s"
                      dur="5s"
                      :from="ele.sourceNode.x + (ele.sourceNode.width/2)"
                      :to="ele.sourceNode.x + (ele.targetNode.x - ele.sourceNode.x)/2 + (ele.targetNode.width/2)"
                      calcMode="linear"
                      repeatCount="indefinite"
                    />
                    <animate
                      attributeName="y2"
                      begin="0s"
                      dur="5s"
                      :from="ele.sourceNode.y + (ele.sourceNode.height/2)"
                      :to="ele.sourceNode.y + (ele.targetNode.y - ele.sourceNode.y)/2 + (ele.targetNode.height/2)"
                      calcMode="linear"
                      repeatCount="indefinite"
                    />
                  </line>
                  <line
                    class="connectorLine"
                    :stroke-width="ele.strokeW"
                    :stroke="ele.color"
                    :x1="ele.targetNode.x + (ele.targetNode.width/2) "
                    :y1="ele.targetNode.y + (ele.targetNode.height/2)"
                    :x2="ele.sourceNode.x + (ele.targetNode.x - ele.sourceNode.x)/2 + (ele.targetNode.width/2)"
                    :y2="ele.sourceNode.y + (ele.targetNode.y - ele.sourceNode.y)/2 + (ele.targetNode.height/2)"
                    marker-end="url(#arrow)"
                  >
                    <animate
                      attributeName="x2"
                      begin="0s"
                      dur="5s"
                      :from="ele.targetNode.x + (ele.targetNode.width/2)"
                      :to="ele.sourceNode.x + (ele.targetNode.x - ele.sourceNode.x)/2 + (ele.targetNode.width/2)"
                      calcMode="linear"
                      repeatCount="indefinite"
                    />
                    <animate
                      attributeName="y2"
                      begin="0s"
                      dur="5s"
                      :from="ele.targetNode.y + (ele.targetNode.height/2)"
                      :to="ele.sourceNode.y + (ele.targetNode.y - ele.sourceNode.y)/2 + (ele.targetNode.height/2)"
                      calcMode="linear"
                      repeatCount="indefinite"
                    />
                  </line>
                </g>
              </g>
              <g v-else>
                <line
                  class="connectorLine"
                  :stroke-width="ele.strokeW"
                  :stroke="editable ? ele.color : (ele.status === '在线' ? ele.color : 'red')"
                  :x1="ele.sourceNode.x + (ele.sourceNode.width/2) "
                  :y1="ele.sourceNode.y + (ele.sourceNode.height/2)"
                  :x2="ele.targetNode.x + (ele.targetNode.width/2)"
                  :y2="ele.targetNode.y + (ele.targetNode.height/2)"
                />
              </g>
              <!--            两个点的线条的中心点xc=x1+(x2-x1)/2 ,yc同理，记得加上node的长或者高  -->
              <!--    流动的线条-->
              <!--              <line-->
              <!--                class="lineMove1"-->
              <!--                :stroke-width="4"-->
              <!--                :stroke="ele.color"-->
              <!--                :x1="ele.sourceNode.x + (ele.sourceNode.width/2) "-->
              <!--                :y1="ele.sourceNode.y + (ele.sourceNode.height/2)"-->
              <!--                :x2="ele.targetNode.x + (ele.targetNode.width/2)"-->
              <!--                :y2="ele.targetNode.y + (ele.targetNode.height/2)"-->
              <!--              />-->
              <!--              <line-->
              <!--                class="lineMove2"-->
              <!--                :stroke-width="4"-->
              <!--                :stroke="ele.color"-->
              <!--                :x2="ele.sourceNode.x + (ele.sourceNode.width/2) "-->
              <!--                :y2="ele.sourceNode.y + (ele.sourceNode.height/2)"-->
              <!--                :x1="ele.targetNode.x + (ele.targetNode.width/2)"-->
              <!--                :y1="ele.targetNode.y + (ele.targetNode.height/2)"-->
              <!--              />-->

<!--              /**-->
<!--              * 连线方式一共7种情况-->
<!--              */-->
              <!-- 自连 -->
              <!--              <path-->
              <!--                class="connectorLine"-->
              <!--                :class="{'defaultStrokeColor':!ele.color,'defaultStrokeW':!ele.strokeW}"-->
              <!--                :stroke="ele.color"-->
              <!--                :stroke-width = "ele.strokeW"-->
              <!--                v-if="ele.sourceNode.id == ele.targetNode.id"-->
              <!--                :d="'M'+(ele.sourceNode.x + ele.sourceNode.width)+','+(ele.sourceNode.y + ele.sourceNode.height / 2)+-->
              <!--                'h'+connectorWSelf+-->
              <!--                'v'+(-(ele.sourceNode.height / 2 + connectorWSelf))+-->
              <!--                'h'+ (-(ele.sourceNode.width +  2 * connectorWSelf)) +-->
              <!--                'v'+(ele.sourceNode.height / 2 + connectorWSelf) +-->
              <!--                'H' + (ele.targetNode.x)"-->
              <!--                ></path>-->
              <!-- 非自连:1.sourceNode 的右侧箭头X <= targetNode的左侧箭头X -->
              <!--              <path-->
              <!--                class="connectorLine"-->
              <!--                :class="{'defaultStrokeColor':!ele.color,'defaultStrokeW':!ele.strokeW}"-->
              <!--                :stroke="ele.color"-->
              <!--                :stroke-width = "ele.strokeW"-->
              <!--                v-if="ele.sourceNode.id != ele.targetNode.id &&-->
              <!--                (ele.sourceNode.x +ele.sourceNode.width) < ele.targetNode.x"-->
              <!--                :d="'M'+(ele.sourceNode.x + ele.sourceNode.width)+','+(ele.sourceNode.y + ele.sourceNode.height / 2) +-->
              <!--                'h'+ (ele.targetNode.x - ele.sourceNode.x - ele.sourceNode.width) / 2 +-->
              <!--                'V' + (ele.targetNode.y + ele.targetNode.height / 2) +-->
              <!--                'H' + ele.targetNode.x"-->
              <!--                ></path>-->
              <!-- 非自连：
              2.sourceNode 的右侧箭头X >= targetNode的左侧箭头X
              (1) 且 sourceNode的高度 < targetNode的高度 且 高度未重叠-->
              <!--              <path-->
              <!--                class="connectorLine"-->
              <!--                :class="{'defaultStrokeColor':!ele.color,'defaultStrokeW':!ele.strokeW}"-->
              <!--                :stroke="ele.color"-->
              <!--                :stroke-width = "ele.strokeW"-->
              <!--                v-if="ele.sourceNode.id != ele.targetNode.id &&-->
              <!--                (ele.sourceNode.x + ele.sourceNode.width) >= ele.targetNode.x &&-->
              <!--                (ele.sourceNode.y + ele.sourceNode.height ) < ele.targetNode.y"-->
              <!--                :d="'M'+(ele.sourceNode.x + ele.sourceNode.width)+','+(ele.sourceNode.y + ele.sourceNode.height / 2) +-->
              <!--                'h'+connectorWSelf+-->
              <!--                'v'+(ele.sourceNode.height / 2 + (ele.targetNode.y - ele.sourceNode.y -  ele.sourceNode.height) / 2) +-->
              <!--                'H'+(ele.targetNode.x - connectorWSelf) +-->
              <!--                'V'+(ele.targetNode.y + ele.targetNode.height / 2) +-->
              <!--                'h'+connectorWSelf"-->
              <!--                ></path>-->

              <!-- 非自连：
              2.sourceNode 的右侧箭头X >= targetNode的左侧箭头X
                (2) 且 sourceNode的高度 > targetNode的高度 且 高度未重叠-->
              <!--              <path-->
              <!--                class="connectorLine"-->
              <!--                :class="{'defaultStrokeColor':!ele.color,'defaultStrokeW':!ele.strokeW}"-->
              <!--                :stroke="ele.color"-->
              <!--                :stroke-width = "ele.strokeW"-->
              <!--                v-if="ele.sourceNode.id != ele.targetNode.id &&-->
              <!--                (ele.sourceNode.x + ele.sourceNode.width) >= ele.targetNode.x &&-->
              <!--                (ele.targetNode.y + ele.targetNode.height) < ele.sourceNode.y"-->
              <!--                :d="'M'+(ele.sourceNode.x + ele.sourceNode.width)+','+(ele.sourceNode.y + ele.sourceNode.height / 2) +-->
              <!--                'h'+connectorWSelf+-->
              <!--                'V'+(ele.sourceNode.y-(ele.sourceNode.y - ele.targetNode.y - ele.targetNode.height) / 2) +-->
              <!--                'H'+ (ele.targetNode.x - connectorWSelf) +-->
              <!--                'V'+(ele.targetNode.y + ele.targetNode.height / 2) +-->
              <!--                'H'+ele.targetNode.x"-->
              <!--                ></path>-->
              <!--
              非自连：
              2.sourceNode 的右侧箭头X >= targetNode的左侧箭头X
              (3) sourceNode的箭头y < = targetNode的箭头
            sourceNode 的y < targetNode的y < = (sourceNode 的y + sourceNode的height) 或者 sourceNode的y介于其间
              高度重叠-->
              <!--              <path-->
              <!--                class="connectorLine"-->
              <!--                :class="{'defaultStrokeColor':!ele.color,'defaultStrokeW':!ele.strokeW}"-->
              <!--                :stroke="ele.color"-->
              <!--                :stroke-width = "ele.strokeW"-->
              <!--                v-if="ele.sourceNode.id != ele.targetNode.id &&-->
              <!--                (ele.sourceNode.x + ele.sourceNode.width) >= ele.targetNode.x &&-->
              <!--                (ele.sourceNode.y + ele.sourceNode.height/2) <= (ele.targetNode.y + ele.targetNode.height / 2) &&-->
              <!--                ((ele.targetNode.y <= (ele.sourceNode.y + ele.sourceNode.height) && ele.targetNode.y >= ele.sourceNode.y) ||-->
              <!--                (ele.sourceNode.y <= (ele.targetNode.y + ele.targetNode.height) && ele.sourceNode.y >= ele.targetNode.y)-->
              <!--                )"-->
              <!--                :d="'M'+(ele.sourceNode.x + ele.sourceNode.width)+','+(ele.sourceNode.y + ele.sourceNode.height / 2)+'h'+connectorWSelf +-->
              <!--                'V'+ ((ele.sourceNode.y-ele.targetNode.y ) <= 0? (ele.sourceNode.y - connectorWSelf) : (ele.targetNode.y -connectorWSelf)) +-->
              <!--                'H' + (ele.targetNode.x - connectorWSelf) +-->
              <!--                'V' +(ele.targetNode.y + ele.targetNode.height / 2) +-->
              <!--                'H' + ele.targetNode.x"-->
              <!--                ></path>-->
              <!--
              非自连：
              2.sourceNode 的右侧箭头X > targetNode的左侧箭头X
              (3) 且 sourceNode的高度 < targetNode的高度 且
              sourceNode的起点 > targetNode的终点 且
              高度重叠-->
              <!--              <path-->
              <!--                class="connectorLine"-->
              <!--                :class="{'defaultStrokeColor':!ele.color,'defaultStrokeW':!ele.strokeW}"-->
              <!--                :stroke="ele.color"-->
              <!--                :stroke-width = "ele.strokeW"-->
              <!--                v-if="ele.sourceNode.id != ele.targetNode.id &&-->
              <!--                (ele.sourceNode.x + ele.sourceNode.width) >= ele.targetNode.x &&-->
              <!--                (ele.sourceNode.y + ele.sourceNode.height/2) > (ele.targetNode.y + ele.targetNode.height / 2) &&-->
              <!--                ((ele.targetNode.y <= (ele.sourceNode.y + ele.sourceNode.height) && ele.targetNode.y >= ele.sourceNode.y) ||-->
              <!--                (ele.sourceNode.y <= (ele.targetNode.y + ele.targetNode.height) && ele.sourceNode.y >= ele.targetNode.y)-->
              <!--                )"-->
              <!--                :d="'M'+(ele.sourceNode.x + ele.sourceNode.width)+','+(ele.sourceNode.y + ele.sourceNode.height / 2)+'h'+connectorWSelf +-->
              <!--                'V'+ ((ele.sourceNode.y  + ele.sourceNode.height-ele.targetNode.y -ele.targetNode.height ) >= 0? (ele.sourceNode.y+ele.sourceNode.height + connectorWSelf) : (ele.targetNode.y+ele.targetNode.height +connectorWSelf)) +-->
              <!--                'H' + (ele.targetNode.x - connectorWSelf) +-->
              <!--                'V' +(ele.targetNode.y + ele.targetNode.height / 2) +-->
              <!--                'H' + ele.targetNode.x"-->
              <!--                ></path>-->
            </g>
            <!--  节点-->
            <g
              v-for="(ele,key) in topoData.nodes"
              :key="ele.id"
              class="nodesG"
              :class="{isSelect:ele.isSelect,hoverShowConnectorArror:editable,hoverShowNodetooltip: !editable}"
              :transform="'translate('+ele.x+','+ele.y+')'"
              @mouseover.stop="mouseoverNode(key,$event)"
              @mousedown.stop="dragSvgNode(key,ele,$event)"
              @mouseout.stop="mouseoutLeftConnector(key)"
            >
              <rect
                x="0"
                y="0"
                rx="2"
                ry="2"
                :width="ele.width"
                :height="ele.height"
                class="reactClass"
                :class="{'node-alarm': ele.status === '离线'}"
              />
              <!-- <text  v-if="ele.classType == 'T1'" class="nodeName" x="5" y="15">{{ele.classType}}</text> -->
              <text v-if="ele.classType === 'T1'" class="nodeName" x="5" y="15">{{ ele.name }}</text>
              <!--              :xlink:href="ele.icon"-->
              <image
                v-if="ele.classType === 'T1'"
                class="nodeImg"
                href="@/assets/topo/switch.svg"
                :x="ele.width - 18"
                :y="3"
                height="15px"
                width="15px"
              />
              <!--:xlink:href="ele.icon"-->
              <image
                v-if="ele.classType == 'T2'"
                class="nodeImg"
                href="@/assets/topo/switch.svg"
                :x="-2"
                :y="-2"
                height="54px"
                width="55px"
              />
              <image
                v-if="ele.status === '离线'"
                class="nodeImg"
                href="@/assets/topo/er/rings.svg"
                :x="-25"
                :y="-25"
                height="100px"
                width="100px"
              />
              <!--              x:y= 7，35px -->
              <text v-if="ele.classType == 'T2'" class="nodeName" x="0" :y="ele.height + 14">
                {{ ele.name }}
              </text>
              <!--           显示连接点   :class="{'connector':ele.isLeftConnectShow}"-->
              <g
                class="connectorArror"
                :transform="'translate('+ele.width/2+','+ele.height/2+')'"
              >
                <circle r="8" cx="0" cy="0" class="circleColor" />
                <!--                <line x1="-3" y1="-5" x2="4" y2="0.5" stroke="#fff"/>-->
                <!--                <line x1="4" y1="-0.5" x2="-3" y2="5" stroke="#fff"/>-->
              </g>
              <!--              <g class="connectorArror" :class="{'connector':ele.isLeftConnectShow}" :transform="'translate('+ele.width/2+','+'-0'+')'">-->
              <!--                <circle r="8" cx="0" cy="0" class="circleColor"></circle>-->
              <!--                <line x1="-3" y1="-5" x2="4" y2="0.5" stroke="#fff"></line>-->
              <!--                <line x1="4" y1="-0.5" x2="-3" y2="5" stroke="#fff"></line>-->
              <!--              </g>-->
              <!--       显示连接点        :class="{'connector':ele.isRightConnectShow}"-->
              <g
                class="connectorArror"
                :transform="'translate('+ele.width/2+','+ele.height/2+')'"
                @mousedown.stop="drawConnectLine(key,$event)"
              >
                <circle r="8" cx="0" cy="0" class="circleColor" />
                <!--                <line x1="-3" y1="-5" x2="4" y2="0.5" stroke="#fff"/>-->
                <!--                <line x1="4" y1="-0.5" x2="-3" y2="5" stroke="#fff"/>-->
              </g>
              <!--              <g class="connectorArror" :class="{'connector':ele.isRightConnectShow}" :transform="'translate('+ele.width/2+','+ele.height+')'" @mousedown.stop="drawConnectLine(key,$event)">-->
              <!--                <circle r="8" cx="0" cy="0" class="circleColor"></circle>-->
              <!--                <line x1="-3" y1="-5" x2="4" y2="0.5" stroke="#fff"></line>-->
              <!--                <line x1="4" y1="-0.5" x2="-3" y2="5" stroke="#fff"></line>-->
              <!--              </g>-->
            <!-- 弹出框
                            :class="{: !editable}"
            -->
              <g
                class="isShowNodetooltip"
              >
                <!-- 提示框的阴影-->
                <defs>
                  <filter id="NodetooltipShadow" x="0" y="0" width="200%" height="200%">
                    <feOffset result="offOut" in="SourceAlpha" dx="1" dy="1" />
                    <feGaussianBlur result="blurOut" in="offOut" stdDeviation="2" />
                    <feBlend in="SourceGraphic" in2="blurOut" mode="normal" />
                  </filter>
                </defs>
                <!--  方框-->
                <rect
                  :x="ele.width/1.5"
                  :y="ele.height/1.5"
                  rx="2"
                  ry="2"
                  width="150"
                  height="200"
                  class="Nodetooltip"
                  filter="url(#NodetooltipShadow)"
                />
                <g
                >
                  <text
                    :x="(ele.width/1.5) +10 "
                    :y="(ele.height/1.5) + 20"
                    fill="#606266"
                    font-size="12"
                  >
                    <tspan :x="(ele.width/1.5) +10 " :y="(ele.height/1.5) + 20">名称: {{ele.name}}</tspan>
                    <tspan :x="(ele.width/1.5) +10 " :y="(ele.height/1.5) + 50">类型: {{ele.netype}}</tspan>
                    <tspan :x="(ele.width/1.5) +10 " :y="(ele.height/1.5) + 80">IP: {{ele.ip}}</tspan>
                    <tspan :x="(ele.width/1.5) +10 " :y="(ele.height/1.5) + 110">状态: {{ele.status}}</tspan>
                  </text>
                </g>
              </g>
            </g>
            <!-- 动态绘制的连线 -->
            <g>
              <line
                v-show="connectingLine.isConnecting"
                :x1="connectingLine.x1"
                :y1="connectingLine.y1"
                :x2="connectingLine.x2"
                :y2="connectingLine.y2"
                stroke="#42b983"
                stroke-width="4"
              />
            </g>
          </g>
          <line
            id="xmarker"
            :class="{isMarkerShow:marker.isMarkerShow}"
            class="marker"
            x1="0"
            :y1="marker.xmarkerY"
            :x2="marker.xmarkerX"
            :y2="marker.xmarkerY"
          />
          <line
            id="ymarker"
            :class="{isMarkerShow:marker.isMarkerShow}"
            class="marker"
            :x1="marker.ymarkerX"
            y1="0"
            :x2="marker.ymarkerX"
            :y2="marker.ymarkerY"
          />
          <rect
            v-show="selectionBox.isShow"
            :x="selectionBox.x"
            :y="selectionBox.y"
            :width="selectionBox.width"
            :height="selectionBox.height"
            stroke-dasharray="5,5"
            stroke-width="1"
            stroke="#222"
            fill="rgba(170,210,232,0.5)"
          />
        </svg>
        <!--        右侧属性框 v-show="editable"-->
        <v-topo-attr-panel
          :editable="editable"
          :is-show-panel="isShowPanel"
          :topo-data="topoData"
          :v-select-node-data="selectNodeData"
          @changeshow="changeShowPanel"
        />
      </div>
    </div>
    <div
      v-if="shapebarMoveNode.isShow"
      class="moveNode nodeMoveCss"
      :style="{ left:shapebarMoveNode.left + 'px', top: shapebarMoveNode.top + 'px' }"
    >
      <div class="shapeIcon">
        <img class="shapeIconImg" :src="shapebarMoveNode.icon">
      </div>
      <div class="shapeName">{{ shapebarMoveNode.name }}</div>
    </div>

    <!--    添加连接关系-->
    <el-dialog
      style="text-align: left"
      title="添加连接关系"
      :visible.sync="flag.addConnectVisible"
      width="60%"
      :before-close="handleCloseAddConnect"
    >
      <div slot="title"><span
        class="el-dialog__title"
        style="border-left: 4px #66b1ff solid; padding-left: 5px"
      >添加连接关系</span></div>
      <el-form label-position="left">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="">
              <div slot="label"><i class="el-icon-attract">源设备</i></div>
              <el-select v-model="connectorTemp.sourceNode.id" filterable placeholder="请先选择源设备">
                <el-option
                  v-for="(item,key) in nodes"
                  :key="key"
                  :label="item.name+'('+item.ip+')'"
                  :value="item.id ? item.id : ''"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="源接口">
              <div slot="label"><i class="el-icon-attract">源接口</i></div>
              <!--                       :remote-method="SearchInterfaces"-->
              <el-select
                v-model="connectorTemp.sourceNode.port"
                filterable

                @focus="SearchInterfacesById(connectorTemp.sourceNode.id,'sourceInterfaces')"
              >
                <div slot="empty">
                  <div v-if="sourceInterfacesLoading" style="height: 20px; padding: 10px; color: rgb(96,98,102);">
                    <i class="el-icon-loading" />Loading...
                  </div>
                </div>
                <el-option
                  v-for="(item,key) in sourceInterfaces"
                  :key="key"
                  :label="item.name"
                  :value="item.name ? item.name : ''"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="目标设备">
              <div slot="label"><i class="el-icon-aim">目标设备</i></div>
              <el-select v-model="connectorTemp.targetNode.id" filterable placeholder="请先选择目标设备">
                <el-option
                  v-for="(item,key) in nodes"
                  :key="key"
                  :label="item.name+'('+item.ip+')'"
                  :value="item.id ? item.id : ''"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="">
              <div slot="label"><i class="el-icon-aim">目标接口</i></div>
              <el-select
                v-model="connectorTemp.targetNode.port"
                filterable

                @focus="SearchInterfacesById(connectorTemp.targetNode.id,'targetInterfaces')"
              >
                <div slot="empty">
                  <div v-if="sourceInterfacesLoading" style="height: 20px; padding: 10px; color: rgb(96,98,102);">
                    <i class="el-icon-loading" />Loading...
                  </div>
                </div>
                <el-option
                  v-for="(item,key) in targetInterfaces"
                  :key="key"
                  :label="item.name"
                  :value="item.name ? item.name : ''"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <p style="color: #6f7180">tips: 请先选择设备再选择接口。</p>
      </el-form>
      <!--      <span class="Vertical-Separator-Lines"></span>-->
      <span slot="footer" class="dialog-footer">
        <el-button @click="flag.addConnectVisible = false">取 消</el-button>
        <el-button type="primary" @click="flag.addConnectVisible = false">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>

import vTopoAttrPanel from './components/vTopoAttrPanel'
import vShapebar from './components/vShapebar/vShapebar'
import { data } from './data'
import { methods } from './methods'
import { props } from './props'

export default {
  components: {
    vTopoAttrPanel,
    vShapebar
  },
  mixins: [props, data, methods],
  computed: {
    nodes() {
      return this.topoData.nodes
    }
  },
  mounted() {
    this.deleteNodeAndConnetor() // 绑定删除Node事件
    this.topoId = this.GenNonDuplicateID(5)
    this.initTopoWH() // 初始化topo组件宽高·
  }
}
</script>
<style scoped lang="less">
@svg-common-color: #336699;
@stroke-width: 2;
@stroke-select-width: 3;
@stroke-select-color: red;
@border-color: #aaaaaa;
@storke-dasharray: 5, 5;
@theme-color: rgb(245, 247, 250);
@theme-border-color: #aaaaaa;
@theme-font-color: #525252;
@Nodetooltip-border-width: 0;
@Nodetooltip-border-color: #066a8b;
@Nodetooltip-fill-color: #f8f8f8;
//垂直分割线
.Vertical-Separator-Lines {
  height: 30%;
  width: 2px;
  background: #3a8ee6;
  position: absolute;
  top: 30%;
  left: calc(50% - 0px);
}

.svgSelectClass {
  filter: url(#f1);
}
.svgSelectLineClass {
  //filter: url(#f1);
  stroke-width: 4px;
  stroke: #42b983;
}

.topoComponent {
  width: 100%;
  box-sizing: border-box;
  background-color: #fff;
  height: 100%;
  display: flex;
  flex-direction: column;
}

/*svgHead工具栏*/
.svgHead {
  width: 100%;
  height: 40px;
  box-sizing: border-box;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: @theme-color;
  border: solid @border-color;
  border-width: 1px 1px 0;
  box-shadow: inset 0 1px 0 0 #fff;

  .svgHeadItemLst {
    display: flex;

    .svgHeadItem {
      padding: 5px 10px;
      border: 1px solid @border-color;
      cursor: pointer;
      list-style: none;
      border-left-width: 0;

      &:hover {
        background-color: #ebebeb
      }

      &:first-child {
        border-left-width: 1px
      }

      &.active {
        background-color: #ebebeb;
        box-shadow: 2px 2px 1px #ccc inset
      }

      .svgHeadItemImg {
        //background: url('src/assets/topo/icons.png');
        width: 16px;
        height: 16px;
        background-size: 479px 16px;

        &.toolbar-default {
          background-position: -16px 0px
        }

        &.toolbar-rectangle_selection {
          background-position: -294px 0px
        }

        &.toolbar-zoomin {
          background-position: -425px 0px
        }

        &.toolbar-zoomout {
          background-position: -444px 0px
        }

        &.toolbar-zoomreset {
          background-position: -462px 0px
        }
      }
    }

    .svgToolBarItem {
      font-size: 13px;
      color: @theme-font-color;
      padding: 5px 10px;
      border-radius: 2px;
      box-sizing: border-box;
      margin-left: 5px;
      cursor: pointer;
      -webkit-user-select: none;
      user-select: none;

      .svgToolBarTxt {
        margin-left: 2px;
      }
    }
  }
}

/*svgMain*/
.svgMain {
  height: 100%;
  box-sizing: border-box;
  display: flex;
  flex: 1;
}

/*移动的node*/
.shapeIcon {
  text-align: center;
  -webkit-user-select: none;
  user-select: none;

  .shapeIconImg {
    width: 28px;
    height: 28px;
    -webkit-user-select: none;
    user-select: none;
  }
}

.shapeName {
  font-size: 12px;
  text-align: center;
  padding: 0 5px;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  -webkit-user-select: none;
  user-select: none;
  color: #000
}

.moveNode {
  position: absolute;
  border: 1px solid @svg-common-color;
  box-sizing: border-box;

  &.nodeMoveCss {
    width: 57px;
    height: 57px;
    background-color: #fff;
    -webkit-user-select: none;
    user-select: none;
    box-sizing: border-box;
    padding: 5px;
  }
}

/*svgMain右侧svg主体区域*/
.topoWrap {
  flex: 1;
  width: 100%;
  box-sizing: border-box;
  border: 1px solid @border-color;
  overflow: hidden;
  position: relative;
  background: #fff;

  .topoSvg {
    box-sizing: border-box;
    background-color: #fff;
    -webkit-user-select: none;
    user-select: none;
    -moz-select: none;
    -ms-select: none;
    -o-select: none;

    &.hand {
      cursor: pointer
    }

    &.crosshair {
      cursor: crosshair;
    }
  }
}

/*svg 节点 连线样式*/
.marker {
  stroke: #3d7ed5;
  stroke-width: 1;
  display: none;

  &.isMarkerShow {
    display: block;
  }
}
.nodesG {
  -webkit-user-select: none;
  user-select: none;
  -moz-select: none;
  -ms-select: none;
  -o-select: none;

  &.isSelect .reactClass {
    stroke-width: @stroke-select-width;
    .svgSelectClass;
  }

  &.isSelect .nodeName {
    font-weight: 500;
  }

  &.hoverShowConnectorArror:hover .connectorArror {
    display: block
  }
  &.hoverShowNodetooltip:hover .isShowNodetooltip {
    display: block;
  }

  .nodeImg {
    -webkit-user-select: none;
    user-select: none;
    -moz-select: none;
    -ms-select: none;
    -o-select: none;
  }

  .nodeName {
    font-size: 12px;
    fill: @svg-common-color;
    -webkit-user-select: none;
    user-select: none;
  }

  .reactClass {
    stroke-width: @stroke-width;
    stroke: @svg-common-color;
    fill: #fff;
    cursor: default;
  }
  .Nodetooltip {
    stroke-width: @Nodetooltip-border-width;
    stroke: @Nodetooltip-border-color;
    fill: @Nodetooltip-fill-color;
    cursor: default;
  }

  .node-alarm {
    --innerRadius: 100px;
    stroke: red;
    fill: #f1b2b2;
  }
  .isShowNodetooltip {
    display: none;
  }
  .connectorArror {
    display: none;

    &.connector {
      display: block;
    }

    .circleColor {
      //fill: @svg-common-color;
      fill: #42b983;
    }
  }
}

.connectorsG {
  .connectorLine {
    fill: none;

    &.defaultStrokeColor {
      stroke: @svg-common-color;
    }

    &.defaultStrokeW {
      stroke-width: @stroke-width;
    }
  }

  &.active .connectorLine {
    //.svgSelectClass;
    .svgSelectLineClass;
  }
}
// 流动线条样式
.lineMove1 {
  stroke: red;
  stroke-dasharray: 10 10;
  animation: rot1 20s linear infinite;
}

@keyframes rot1 {
  100% {
    //stroke-dasharray: 100% 100%;
    stroke-dashoffset: 100%;
  }
}

.lineMove2 {
  stroke: blueviolet;
  stroke-dasharray: 0 100%;
  animation: rot2 8s linear infinite;
}

@keyframes rot2 {
  100% {
    stroke-dasharray: 100% 50%;
  }
}
</style>
<style>
ul, li {
  margin: 0;
  padding: 0;
  list-style: none;
}
.pingMessage {
  /*background: rgb(53, 56, 53);*/
  color: white;
}
.pingMessage>.el-message__icon{
  display: none;
}
.pingMessage>p {
  padding: 0;
  margin: 0;

}
.pingMessage>p>ul>li{
  padding: 5px;
  /*color: rgb(192,192,192);*/
}
.el-collapse-item__header {
  -webkit-user-select: none;
  user-select: none;
  -moz-select: none;
  -ms-select: none;
  -o-select: none;
}

.menu_item_label {
  -webkit-box-flex: 1;
  -ms-flex: 1;
  flex: 1;
  text-align: left;
  padding-left: 5px;
}
</style>
