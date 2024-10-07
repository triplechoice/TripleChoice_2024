<template>
  <div>
    <SearchParts ref="searchParts"></SearchParts>
    <div class="installer-wizard">
      <div class="div">
        <TabList ref="tabList" v-show="loaded"></TabList>
        <div class="wizard-bar"></div>
      </div>
      <TabBody ref="tabBody" :tab="activeTab" :part="part" :order_id="order_id"></TabBody>
    </div>
    <h1>hehehehehe</h1>

  </div>
</template>

<script>
import SearchParts from "../frontend/homepage/Index";
import TabList from "./components/TabList";
import TabBody from "./components/TabBody";
import {mapGetters} from 'vuex'

export default {
  name      : "index.vue",
  props     : ['part', 'order_id'],
  components: {
    TabBody,
    TabList,
    SearchParts
  },
  data() {
    return {
      activeTab: 'Specification',
      loaded   : false,
    }
  },
  computed: {
    ...mapGetters(['parts', 'contactForm', 'commentForm', 'submitForm'])
  },
  mounted() {
    this.loaded = true;
  },
  method: {}
}
</script>

<style scoped>

</style>