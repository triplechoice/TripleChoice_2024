<template>
  <div class="d-flex featured-parts-section flex-column h-50 justify-content-end">
    <div class="row justify-content-center mb-3">
      <div class="col-md-6">
        <h3 class="text-primary text-center title">Technical Parts Procurement</h3>
        <carousel
            :autoplay="true"
            :nav="false"
            :margin="15"
            :loop="true"
            :responsive="{0:{items:1},600:{items:3},991:{items:3}}"
        >

<!--          <div class="item">-->
<!--            <img src="../../../assets/p-1.png">-->
<!--            <p class="text-center">Compressor</p>-->
<!--          </div>-->
<!--          <div class="item">-->
<!--            <img src="../../../assets/p-2.png">-->
<!--            <p class="text-center">Pump</p>-->
<!--          </div>-->
<!--          <div class="item">-->
<!--            <img src="../../../assets/p-3.png">-->
<!--            <p class="text-center">Valves</p>-->
<!--          </div>-->
          <div class="item">
            <img src="../../../assets/p-4.png">
            <p class="text-center">Pump</p>
          </div>
          <div class="item">
            <img src="../../../assets/p-5.png">
            <p class="text-center">Compressor</p>
          </div>
          <div class="item">
            <img src="../../../assets/p-3.png">
            <p class="text-center">Valves</p>
          </div>
        </carousel>
      </div>
    </div>
  </div>

</template>

<script>
import carousel from 'vue-owl-carousel'

export default {
  name: "mainSlider",
  components: { carousel },
}
</script>

<style scoped>

</style>