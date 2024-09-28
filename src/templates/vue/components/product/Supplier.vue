<template>
  <div class="container">
    <form @submit.prevent="onSubmit">
      <label class="form-label">Select Suppliers</label>
      <multiselect v-model="selectedSupplier" tag-placeholder="Add this as new tag"
                   placeholder="Search or add a supplier"
                   label="username" track-by="username" :options="suppliers" :multiple="true" :taggable="true"
                   @click="addSupplier"></multiselect>
      <input class="mt-2" type="submit" value="save">
    </form>
  </div>

</template>

<script>
import Multiselect from 'vue-multiselect'

export default {
  name      : "Supplier",
  components: {
    Multiselect
  },
  props     : ['user_id', 'part_id'],
  data() {
    return {
      selectedSupplier: [],
      suppliers       : []
    }
  },
  mounted: function () {
    axios.get('/api/part/supplier/',
        {
          params:
              {
                part_id: this.part_id
              }
        }).then(
        res => {
          this.selectedSupplier = res.data.part_suppliers
          this.suppliers = res.data.suppliers
        }
    ).catch(e => {
    })
  },
  methods: {
    addSupplier(newSupplier) {
      const supplier = {
        id      : newSupplier.id,
        username: newSupplier.username
      }
      this.suppliers.push(supplier)
      this.selectedSupplier.push(supplier)
    },
    onSubmit() {
      let s_ids = []
      for (const supplier of this.selectedSupplier) s_ids.push(supplier.id)
      axios.post('/api/part/supplier/', {'suppliers': s_ids, 'part_id': this.part_id}).then(
          window.location.href = "/super-admin/product/part/"
      ).catch()
    }
  }
}
</script>

<style scoped>

</style>