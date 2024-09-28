<template>

  <div class="m-3">
    <div class="row">


      <div class="col-6">
        <label class="typo__label"> Request</label>
        <multiselect v-model="requests" track-by="order_id" label="order_id"
                     placeholder="Select one" :options="request_list" :searchable="true" :allow-empty="false"
                     @select="getRequestReviews($event)">

        </multiselect>
        <div>
          <label class="typo__label">Reviews</label>
          <multiselect v-model="reviews" tag-placeholder="Add this as new tag" placeholder="Search or add a tag"
                       label="title" track-by="id" :options="review_list" :multiple="true" :taggable="true"
          ></multiselect>

        </div>

        <button type="button" class="btn btn-primary mt-5" @click="onSubmit"> Submit</button>

      </div>


    </div>

  </div>


</template>

<script>
import Multiselect from 'vue-multiselect'


export default {
  name: "create",

  components: {
    Multiselect
  },
  props: ["selected_request_id", "selected_reviews"],

  data() {
    return {
      requests: "",
      request_list: [],
      reviews: [],
      review_list: []
    }
  },
  mounted() {
    this.getRequests()
    if (this.selected_request_id) {
      this.getSelectedData()
    }
  },

  methods: {
    getRequests() {
      axios.get('/api/request/')
          .then(res => {
            res.data.results.map(e => {
              this.request_list.push({id: e.id, order_id: e.order_id})
            })
          })
    },

    getRequestReviews($event) {
      this.review_list = []
      this.reviews = []
      axios.get('/api/request_reviews/' + $event.order_id)
          .then(res => {
            res.data.map(e => {
              this.review_list.push({id: e.id, title: e.title})
            });
          })
    },
    onSubmit(option) {
      if (this.reviews.length <= 0) {
        Toast.fire({
          icon: "error",
          title: "Fill the form"
        })
        return
      }
      let reviews = []
      this.reviews.map(e => {
        reviews.push(e.id)
      });
      let data = {
        request_id: this.requests.id,
        reviews: reviews
      }
      axios.post('/api/request_reviews_create/', data)
          .then(res => {
            Toast.fire({
              icon: "success",
              title: "Fill the form"
            })
            let url = `${window.location.origin}/super-admin/order/selectedrequestreview/`;
            window.location.href = url
          })
          .catch(e => {
            Toast.fire({
              icon: "error",
              title: e
            })
          })
    },
    getSelectedData() {
      let pre_selcted_request = JSON.parse(this.selected_request_id)
      this.requests = {id: pre_selcted_request.id, order_id: pre_selcted_request.order_id}
      this.getRequestReviews(this.requests)

      if (this.selected_reviews) {
        let pre_selected_reviws = JSON.parse(this.selected_reviews)
        pre_selected_reviws.map(review => {
          this.reviews.push({id: review.id, title: review.title})
        })
      }
    }
  }
}
</script>

<style scoped>

</style>