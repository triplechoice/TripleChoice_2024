<template>
  <div class="d-flex justify-content-between tab-list">
      <div class="align-items-center d-flex flex-column tab"
           v-for="(tab, index) in tabs"
           :key="index"
           :class="[{'done' : tab === activeTab || tab.check}, {'activeCheck' : tab.isIcon === true}]"
           :title="tab.title">
        <!-- TODO::click tablist heading-->
          <!-- @click="switchTab(index)"-->
        <div class="circle-box d-flex align-items-center justify-content-center">
          <i v-if="tab.isIcon" :class="tab.icon" class=" position-absolute text-white"></i>
          <span v-else>{{tab.iconText}}</span>
        </div>
        <div class="tab-title mt-2 mt-sm-3" >{{ tab.title }}</div>
      </div>
  </div>
</template>

<script>
export default {
  name: "TabList",
  data() {
    return {
      tabs     : {
        'Specification': {
          title: 'Specification',
          icon : 'fas fa-check',
          check: false,
          form : 'parts',
          iconText:1,
          isIcon: false
        },
        'Comment'      : {
          title: 'Comment',
          icon : 'fas fa-check',
          check: false,
          form : "commentForm",
          iconText:2,
          isIcon: false
        },
        'Submit'   : {
          title: 'Submit',
          icon : 'fas fa-check',
          check: false,
          form : "submitForm",
          iconText:3,
          isIcon: false
        },
      },
      activeTab: {},
    }
  },
  mounted() {
    this.activeTab = this.tabs.Specification;
    // console.log(this.activeTab, 'mounted')
  },
  methods: {
    switchTab(index, a) {
      this.activeTab         = this.tabs[index];
      this.$parent.activeTab = index;
    }
  },
}
</script>

<style scoped>

</style>
