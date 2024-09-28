<template>

  <div class="card shadow">
    <form @submit.prevent="submitOrder">
      <div class="row">
        <div class="col-12">
          <div class="card-header bg-primary mb-2 text-white py-2">Checkout</div>
        </div>
        <div class="col-6">
          <div class="card shadow">
            <div class="card-header bg-primary mb-2 text-white py-1">Billing Details</div>
            <div class="card-body">
              <div class="row">
                <div class="col-6">
                  <label>First Name</label>
                  <input type="text" :class="($v.billing_info.first_name.$error) ? 'border-danger' : ''"
                         class="form-control " v-model="billing_info.first_name">
                  <p v-if="$v.billing_info.first_name.$error" class="help text-danger">This first name is required</p>
                </div>
                <div class="col-6">
                  <label>Last Name</label>
                  <input type="text" class="form-control" v-model="billing_info.last_name">
                </div>
              </div>
              <div class="row">
                <div class="col-6">
                  <label>Email</label>
                  <input type="email" :class="($v.billing_info.email.$error) ? 'border-danger' : ''"
                         class="form-control" v-model="billing_info.email">
                  <p v-if="$v.billing_info.email.$error" class="help text-danger">This email is required</p>
                </div>
                <div class="col-6">
                  <label>Phone No</label>
                  <input type="text" class="form-control" v-model="billing_info.phone_no">
                </div>
              </div>
              <div class="row">
                <div class="col">
                  <label>Street and Number</label>
                  <input type="text" :class="($v.billing_info.street_no.$error) ? 'border-danger' : ''"
                         class="form-control" v-model="billing_info.street_no">
                  <p v-if="$v.billing_info.street_no.$error" class="help text-danger">This street no is required</p>
                </div>
              </div>
              <div class="row">
                <div class="col">
                  <label>Building, Suit, Unit, Floor, Apartment</label>
                  <input type="text" class="form-control" v-model="billing_info.building_suit_no">
                </div>
              </div>
              <div class="row">
                <div class="col">
                  <label>State</label>
                  <multiselect v-model="billing_state_obj" deselect-label="Remove selected state" track-by="name"
                               label="name"
                               placeholder="Select one" :options="billing_options" :searchable="true"
                               :allow-empty="true">
                    <template slot="singleLabel" slot-scope="{ option }"><strong>{{ option.name }}</strong></template>
                  </multiselect>
                </div>
              </div>
              <div class="row">
                <div class="col-6">
                  <label>City</label>
                  <input type="text" :class="($v.billing_info.city.$error) ? 'border-danger' : ''"
                         class="form-control" v-model="billing_info.city">
                  <p v-if="$v.billing_info.city.$error" class="help text-danger">This city field is required</p>
                </div>
                <div class="col-6">
                  <label>Zip Code</label>
                  <input type="text" :class="($v.billing_info.zip_code.$error) ? 'border-danger' : ''"
                         class="form-control" v-model="billing_info.zip_code">
                  <p v-if="$v.billing_info.zip_code.$error" class="help text-danger">This zip code is required</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!--          Order summary-->

        <div class="col-6">
          <div class="card shadow">
            <div class="card-header bg-primary mb-2 text-white py-1">Order Summary</div>
            <div class="card-body">
              <div class="card">
                <ul class="list-group list-group-flush">
                  <li class="list-group-item d-flex justify-content-between">
                    <label>Quantity</label>
                    <label>{{ this.order_quantity }}</label>
                  </li>
                  <li class="list-group-item d-flex justify-content-between">
                    <label>Subtotal</label>
                    <label>{{ this.subtotal }}</label>
                  </li>
                  <li class="list-group-item d-flex justify-content-between">
                    <label>Tax</label>
                    <label>{{ this.tax }}</label>
                  </li>
                  <li class="list-group-item d-flex justify-content-between">
                    <label>Total</label>
                    <label>{{ this.total }}</label>
                  </li>
                </ul>
              </div>
              <div class="m-2">
                <input @change="showNextBtn($event)" type="checkbox" id="term&condition">
                <label for="term&condition" class="m-2">I have read and agree with the <a target="_blank"
                                                                                          href="https://www.triplechoice.com/pages/terms-of-use">terms
                  &
                  conditions.</a></label>
              </div>
              <div class="d-flex justify-content-between mt-2">
                <button type="button" @click="backBtn" class="btn btn-primary">Back</button>
                <input v-if="!this.next_btn" type="submit" value="Next" class="btn btn-primary "
                       :class="readTerms ? '': 'd-none' ">
                <div v-else class="spinner-border text-success" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
      <!--        Shipping info-->
      <div class="row my-2">
        <div class="col-6">
          <div class="card shadow">
            <div class="card-header bg-primary mb-2 text-white py-1">Shipping Details</div>
            <div class="card-body">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" id="sameaddesscheck" @change="sameAddress($event)">
                <label class="form-check-label" for="sameaddesscheck">Same as billing address</label>
              </div>

              <div class="row">
                <div class="col-6">
                  <label>First Name</label>
                  <input type="text" :class="($v.shipping_info.first_name.$error) ? 'border-danger' : ''"
                         class="form-control" v-model="shipping_info.first_name">
                  <p v-if="$v.shipping_info.first_name.$error" class="help text-danger">This first name is
                    required</p>
                </div>
                <div class="col-6">
                  <label>Last Name</label>
                  <input type="text" class="form-control" v-model="shipping_info.last_name">
                </div>
              </div>
              <div class="row">
                <div class="col-6">
                  <label>Email</label>
                  <input type="email" :class="($v.shipping_info.email.$error) ? 'border-danger' : ''"
                         class="form-control" v-model="shipping_info.email">
                  <p v-if="$v.shipping_info.email.$error" class="help text-danger">This email is required</p>
                </div>
                <div class="col-6">
                  <label>Phone No</label>
                  <input type="text" class="form-control" v-model="shipping_info.phone_no">
                </div>
              </div>
              <div class="row">
                <div class="col">
                  <label>Street and Number</label>
                  <input type="text" :class="($v.shipping_info.street_no.$error) ? 'border-danger' : ''"
                         class="form-control" v-model="shipping_info.street_no">
                  <p v-if="$v.shipping_info.street_no.$error" class="help text-danger">This field is required</p>
                </div>
              </div>
              <div class="row">
                <div class="col">
                  <label>Building, Suit, Unit, Floor, Apartment</label>
                  <input type="text" class="form-control" v-model="shipping_info.building_suit_no">
                </div>
              </div>
              <div class="row">
                <div class="col">
                  <label>State</label>
                  <multiselect v-model="shipping_state_obj" deselect-label="Remove selected state" track-by="name"
                               label="name"
                               placeholder="Select one" :options="shipping_options" :searchable="true"
                               :allow-empty="true">
                    <template slot="singleLabel" slot-scope="{ option }"><strong>{{ option.name }}</strong></template>
                  </multiselect>

                </div>
              </div>
              <div class="row">
                <div class="col-6">
                  <label>City</label>
                  <input type="text" :class="($v.shipping_info.city.$error) ? 'border-danger' : ''"
                         class="form-control"
                         v-model="shipping_info.city">
                  <p v-if="$v.shipping_info.city.$error" class="help text-danger">This city is required</p>
                </div>
                <div class="col-6">
                  <label>Zip Code</label>
                  <input type="text" :class="($v.shipping_info.zip_code.$error) ? 'border-danger' : ''"
                         class="form-control" v-model="shipping_info.zip_code">
                  <p v-if="$v.shipping_info.zip_code.$error" class="help text-danger">This zip code is required</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!--        payment method-->
      <div class="row mb-2">
        <div class="col-6">
          <div class="card shadow">
            <div class="card-header bg-primary mb-2 text-white py-1">Payment Method</div>
            <div class="card-body">
              <div class="form-check">
                <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1"
                       v-model="payment_method" value="stripe" checked>
                <label class="form-check-label" for="flexRadioDefault1">
                  Stripe
                </label>
              </div>
              <!--  <div class="form-check">
                <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1"
                       v-model="payment_method" value="debit">
                <label class="form-check-label" for="flexRadioDefault1">
                  Debit Card
                </label>
              </div>
              <div class="form-check">
                <input v-model="payment_method" class="form-check-input" type="radio" name="flexRadioDefault"
                       id="flexRadioDefault2" value="credit">
                <label class="form-check-label" for="flexRadioDefault2">
                  Credit Card
                </label>
              </div>-->
              <div>
                <StripeElementCard
                    :pk="stripe_pk"
                    @element-blur="stripePayment"
                    @error="onStripeError"
                    ref="stripe"
                    @token="tokenCreated"
                >

                </StripeElementCard>
              </div>
            </div>
          </div>
        </div>
      </div>
    </form>
  </div>

</template>

<script>
import {validationMixin} from 'vuelidate'
import {email, maxLength, required} from 'vuelidate/lib/validators'
import {StripeElementCard} from '@vue-stripe/vue-stripe';
import Multiselect from 'vue-multiselect'
import {statesOfUS} from "../utils/usa-states";


export default {
  name: "CheckOut",
  props: ["request_id", "quantity", "user_id", "review_id", "stripe_pk"],
  mixins: [validationMixin],
  components: {
    StripeElementCard,
    Multiselect
  },
  data() {
    return {
      readTerms: false,
      shipping_options: statesOfUS,
      billing_options: statesOfUS,
      shipping_state_obj: {},
      billing_state_obj: {},
      order_quantity: 0,
      request_obj: {},
      review_obj: {},
      subtotal: 0,
      total: 0,
      tax: 0,
      billing_info: {
        first_name: "",
        last_name: "",
        email: "",
        phone_no: "",
        street_no: "",
        building_suit_no: "",
        state: "",
        city: "",
        zip_code: ""
      },
      shipping_info: {
        first_name: "",
        last_name: "",
        email: "",
        phone_no: "",
        street_no: "",
        building_suit_no: "",
        state: "",
        city: "",
        zip_code: ""
      },
      payment_method: "stripe",
      same_address: false,
      next_btn: false,
      stripeToken: '',
      stripeError: {}
    }
  },
  validations() {
    return {
      billing_info: {
        first_name: {required, maxLength: maxLength(255)},
        last_name: {maxLength: maxLength(255)},
        email: {required, email, maxLength: maxLength(255)},
        phone_no: {},
        street_no: {required, maxLength: maxLength(255)},
        building_suit_no: {maxLength: maxLength(255)},
        state: {},
        city: {required, maxLength: maxLength(255)},
        zip_code: {required, maxLength: maxLength(100)}
      },
      shipping_info: {
        first_name: {required, maxLength: maxLength(255)},
        last_name: {maxLength: maxLength(255)},
        email: {required, email, maxLength: maxLength(255)},
        phone_no: {},
        street_no: {required, maxLength: maxLength(255)},
        building_suit_no: {maxLength: maxLength(255)},
        state: {},
        city: {required, maxLength: maxLength(255)},
        zip_code: {required, maxLength: maxLength(100)}
      },
      payment_method: {required}
    }
  },
  mounted() {

    this.get_data()
    this.get_review()
  },
  methods: {
    async get_data() {
      await axios.get(`/api/get_request/${this.request_id}`).then(res => {
        this.request_obj = res.data
        this.order_quantity = this.quantity
      }).catch(err => {
        console.log(err.response.data)
      })
    },
    async get_review() {
      await axios.get(`/api/get_review/${this.review_id}`).then(res => {
        this.review_obj = res.data
        this.calculate_subtotal()
      }).catch(err => {

      })
    },
    async calculate_subtotal() {
      this.subtotal = this.quantity * this.review_obj.cost
      this.calculate_total()
    },
    calculate_total() {
      this.total = this.subtotal + this.tax
    },
    sameAddress(e) {
      this.same_address = e.target.checked
      if (this.same_address) {
        this.shipping_info = this.billing_info
        this.shipping_state_obj = this.billing_state_obj

      } else {
        this.shipping_info = {
          first_name: "",
          last_name: "",
          email: "",
          phone_no: "",
          street_no: "",
          building_suit_no: "",
          state: "",
          city: "",
          zip_code: "",
        }
        this.shipping_state_obj = {}
      }
    },

    backBtn() {
      window.location.href = `/request/${this.request_id}/order_now/${this.review_id}?quantity=${this.quantity}`
    },
    submitOrder() {
      if (this.billing_state_obj.name.length <= 0) {
        this.$v.$touch()
        if (!this.$v.$error) {
          Toast.fire({
            text: "Billing state is required",
            icon: 'error'
          })
        }
      } else if (this.shipping_state_obj.name.length <=0) {
        this.$v.$touch()
        if (!this.$v.$error) {
          Toast.fire({
            text: "Shipping state is required",
            icon: 'error'
          })
        }
      } else {
        if (!this.stripeToken) {
          let error = this.stripeError?.message ?? 'Please make payment first'
          Toast.fire({
            title: error,
            icon: 'error'
          })
          return
        }
        this.$v.$touch()
        if (this.$v.payment_method.$error) {
          Toast.fire({
            title: 'Payment method is required',
            icon: 'error'
          })
        } else if (!this.$v.$error) {
          this.shipping_info.state = this.shipping_state_obj.name
          this.billing_info.state = this.billing_state_obj.name
          let data = {
            billing_address: this.billing_info,
            shipping_address: this.shipping_info,
            request: this.request_id,
            payment_method: this.payment_method,
            subtotal: this.subtotal,
            total: this.total,
            tax: this.tax,
            quantity: this.order_quantity,
            user: this.user_id,
            review: this.review_id,
            unit: this.review_obj.cost_unit
          }
          console.log(data)
          this.next_btn = true
          axios.post('/api/order/', data).then(res => {
            this.next_btn = true
            Toast.fire({
              title: 'Order submitted successfully',
              icon: 'success'
            })
            setTimeout(() => {
              window.location.href = '/user/orders/'
            }, 3000);
          }).catch(error => {
            console.log('error', error.response.data)
            if (error.response.data.detail) {
              Toast.fire({
                title: error.response.data.detail,
                icon: 'error'
              })
            }
            this.next_btn = false
            let msg = "Provide all information properly"
            // if (error.response.data.request[0]) msg = "Order for this request already exists"
            Toast.fire({
              title: msg,
              icon: 'error'
            })
          })
        }

      }
    },
    stripePayment() {
      let res = this.$refs.stripe.submit()
    },
    tokenCreated(token) {
      this.stripeToken = token.id
    },
    onStripeError(error) {
      if (error) {
        this.stripeToken = null;
        this.stripeError = error
      }
    },

    showNextBtn(e) {
      this.readTerms = !!e.target.checked;
    }
  }
}
</script>
