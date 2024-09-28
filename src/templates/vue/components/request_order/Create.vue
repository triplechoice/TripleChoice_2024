<template>
  <div class="card">
    <div class="card-body">
      <form @submit.prevent="checkOut">
        <table class="table">
          <thead>
          <tr>
            <th scope="col">Part</th>
            <th scope="col">Lead Time</th>
            <th scope="col">Cost</th>
            <th scope="col">Quantity</th>
            <th scope="col">Subtotal</th>
          </tr>
          </thead>
          <tbody>
          <tr>
            <td>{{ this.request_obj.part.title }}</td>
            <td>{{ this.review_obj.lead_time }} {{ this.review_obj.unit }}</td>
            <td>{{ this.review_obj.cost }}</td>
            <td><input type="number" v-model="quantity" min="1" @keyup="calculate_subtotal"></td>
            <td>{{ this.subtotal }}</td>
          </tr>
          </tbody>
        </table>
        <input type="submit" value="Check Out" class="btn btn-primary mt-2">
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name : "Create",
  props: ["request_id", "review_id"],
  data() {
    return {
      review_obj : {},
      request_obj: {},
      subtotal   : 0,
      quantity   : 0
    }
  },
  mounted() {
    this.get_data()
    this.get_review()
  }
  ,
  methods: {
    async get_data() {
      await axios.get(`/api/get_request/${this.request_id}`).then(res => {
        this.request_obj = res.data
      }).catch(err => {
      })
    },
    async get_review() {
      await axios.get(`/api/get_review/${this.review_id}`).then(res => {
        this.quantity   = res.data.quantity
        this.review_obj = res.data
        let url         = window.location.search.substring(1);
        if (url) {
          let params    = new URLSearchParams(url);
          this.quantity = params.get("quantity")
        }
        this.calculate_subtotal()
      }).catch(err => {

      })
    },
    calculate_subtotal() {
      this.subtotal = this.quantity * this.review_obj.cost
    },
    async checkOut() {
      if (this.quantity < 1) {
        Toast.fire({
          text: 'Quantity must be greater than 1',
          icon: 'error'
        })
      } else {
        await axios.get(`/request-checkout/?request_id=${this.request_id}&&review_id=${this.review_id}`).then(
            res => {
              window.location.href
                  = `/request-checkout/?request_id=${this.request_id}&&quantity=${this.quantity}&&review_id=${this.review_id}`
            }
        ).catch()
      }

    }
  }
}
</script>
