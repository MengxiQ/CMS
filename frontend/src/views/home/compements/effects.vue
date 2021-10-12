<template>
  <div>
    <div class="wrap">
      <div class="cube">
        <div class="outer before"><div class="content-text">OSPF</div></div>
        <div class="outer after"><div class="content-text">IP</div></div>
        <div class="outer right"><div class="content-text">BGP</div></div>
        <div class="outer left"><div class="content-text">INTERFACES</div></div>
        <div class="outer top"><div class="content-text">VLAN</div></div>
        <div class="outer bottom"><div class="content-text">ROUTE</div></div>
        <div class="inner cube-inner-before"><div class="content-text-inner">NETCONF</div></div>
        <div class="inner cube-inner-after"><div class="content-text-inner">NETCONF</div></div>
        <div class="inner cube-inner-right"><div class="content-text-inner">NETCONF</div></div>
        <div class="inner cube-inner-left"><div class="content-text-inner">NETCONF</div></div>
        <div class="inner cube-inner-top"><div class="content-text-inner">NETCONF</div></div>
        <div class="inner cube-inner-bottom"><div class="content-text-inner">NETCONF</div></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Effects',
}
</script>

<style scoped>
/*最外层容器样式*/
.wrap {
  /*width: 200px;*/
  /*height: 200px;*/
  margin: 0px auto;
  position: relative;
  z-index: 1000;
}
.surface {
  /*height: 100%;*/
  /*width: 100%;*/
  /*display: flex;*/
  /*justify-content: center;*/
  /*align-items: center;*/
  /*align-content: space-between;*/

}
/*包裹所有容器样式*/
.cube{
  width: 400px;
  height: 400px;
  /*大两百：hover的容错率*/
  padding: 100px;
  margin: 0 auto;
  position: relative;
  transform-style: preserve-3d;
  transform: rotateX(-30deg) rotateY(-80deg);
  -webkit-animation: rotate 20s infinite;
  animation-timing-function: linear;
}

.cube .outer {
  position: absolute;
  width: 200px;
  height: 200px;
  opacity: 0.8;
  transition: all 0.3s;
}
.cube .outer:hover {
  background: gold;
  transform: scale(1.2);
}
.cube .before {
  transform: rotateY(0deg) translateZ(100px);
  background: rgb(244,81,108);
}
.cube .after {
  transform: translateZ(-100px) rotateY(180deg);
  background: rgb(54,163,247);
}
.cube .left{
  transform: rotateY(90deg) translateZ(100px);
  background: rgb(64,201,198);
}
.cube .right{
  transform: rotateY(-90deg) translateZ(100px);
  background: #CCFF66;
}
.cube .top{
  transform: rotateX(90deg) translateZ(100px);
  background: purple;
}
.cube .bottom{
  transform: rotateX(-90deg) translateZ(100px);
  background: pink;
}
.cube:hover .before {
      transform: rotateY(0deg) translateZ(200px);
  }
.cube:hover .after {
  transform: translateZ(-200px) rotateY(180deg);
}
.cube:hover .left{
  transform: rotateY(90deg) translateZ(200px);
}
.cube:hover .right{
  transform: rotateY(-90deg) translateZ(200px);
}
.cube:hover .top{
  transform: rotateX(90deg) translateZ(200px);
}
.cube:hover .bottom{
  transform: rotateX(-90deg) translateZ(200px);
}
.pic{
  width: 200px;
  height: 200px;
}

@-webkit-keyframes rotate{
  from{
    transform: rotateX(0deg) rotateY(0deg);
  }
  to{
    transform: rotateX(360deg) rotateY(360deg);
  }
}

.inner {
  height: 100px;
  width: 100px;
  background-color: #1482f0;
  border: white 1px solid;
}
.cube-inner-before {
  transform: rotateY(0deg) translateZ(50px) translateX(50px) translateY(50px);
  /*background: red;*/
}
.cube-inner-after {
  transform: translateZ(-50px) rotateY(180deg) translateX(-50px) translateY(-50px);
  /*background: blue;*/
}
.cube-inner-left{
  transform: rotateY(90deg) translateZ(100px) translateX(0px) translateY(-250px);
  /*background: green;*/
}
.cube-inner-right{
  transform: rotateY(-90deg) translateZ(0px) translateY(-150px);
  /*background: yellow;*/
}
.cube-inner-top{
  transform: rotateX(90deg) translateZ(400px) translateX(50px);
  /*background: purple;*/
}
.cube-inner-bottom{
  transform: rotateX(-90deg) translateZ(-400px) translateX(50px);
  /*background: pink;*/
}

.content-text {
  text-align: center;
  /*height: 50px;*/
  width: 100%;
  padding:75px 0;
  font-size: 30px;
  color: #f9f9f9;
}
.content-text-inner {
  padding: 50px 10px;
  font-size: 15px;
  color: white;
}
</style>
