<template>
  <div>
    <SearchParts ref="searchParts"></SearchParts>
    <div class="installer-wizard matched_data">
      <div class="div">
        <TabList ref="tabList" v-show="loaded"></TabList>
        <div class="wizard-bar"></div>
      </div>
      <TabBody ref="tabBody" :tab="activeTab" :part="part" :order_id="order_id"></TabBody>
    </div>

    <div v-if="pumpData.length > 0" class="row ">
      <div class="col-12">
<!--        <h3>Pump Data</h3>-->
        <h5>Search Results: {{ matchedPumpCount }} Matches out of {{ pumpData.length }} Pump Data</h5>
        <div>
          <table class="table table-striped">
            <thead>
            <tr>
              <th>Pump Name</th>
              <th>Input Flow Rate (GPM)</th>
              <th>Input Head (ft)</th>
              <th>Predicted Head (ft)</th>
              <th>Match Pump</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(data, index) in pumpData" :key="index">
              <td>{{ data['Pump Name'] }}</td>
              <td>{{ data['Input Flow Rate (GPM)'] }}</td>
              <td>{{ data['Input Head (ft)'] }}</td>
              <td>{{ data['Predicted Head (ft)'] }}</td>
              <td>{{ data['Match Pump'] }}</td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SearchParts from "../frontend/homepage/Index";
import TabList from "./components/TabList";
import TabBody from "./components/TabBody";
import {mapGetters} from 'vuex'

export default {
  name: "index.vue",
  props: ['part', 'order_id'],
  components: {
    TabBody,
    TabList,
    SearchParts
  },
  data() {
    return {
      activeTab: 'Specification',
      loaded: false,
    }
  },
  computed: {
    ...mapGetters(['parts', 'contactForm', 'commentForm', 'submitForm', 'pumpData']),
     // Computed property to count the matched pumps
    matchedPumpCount() {
      return this.pumpData.filter(data => data['Match Pump'] === 'Match').length;
    }
  },
  mounted() {
    this.loaded = true;
  },
  created() {
    this.$store.commit('setPumpData', {})
  },
  method: {}
}
</script>

<style scoped>

</style>