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
                  <select class="form-control" v-model="billing_info.state">
                    <option>1</option>
                    <option>2</option>
                    <option>3</option>
                  </select>
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
                    <label>{{ this.quantity }}</label>
                  </li>
                  <li class="list-group-item d-flex justify-content-between">
                    <label>Cost</label>
                    <!--                    <label>{{ this.request_obj.cost }}</label>-->
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
              <div class="d-flex justify-content-between mt-2">
                <button type="button" @click="backBtn" class="btn btn-primary">Back</button>
                <input v-if="!this.next_btn" type="submit" value="Next" class="btn btn-primary">
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
                <input class="form-check-input" type="checkbox" id="sameaddesscheck" @click="sameAddress">
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
                  <select class="form-control" v-model="shipping_info.state">
                    <option>1</option>
                    <option>2</option>
                    <option>3</option>
                  </select>
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
              </div>
            </div>
          </div>
        </div>
      </div>
    </form>
  </div>

</template>

<script>
import {validationMixin}            from 'vuelidate'
import {email, maxLength, required} from 'vuelidate/lib/validators'

export default {
  name  : "OrderUpdate",
  props : ['user_id', 'order_id'],
  mixins: [validationMixin],
  data() {
    return {
      subtotal      : 0,
      total         : 0,
      tax           : 0,
      quantity      : 0,
      cost          : 0,
      request_id    : 0,
      billing_info  : {
        first_name      : "",
        last_name       : "",
        email           : "",
        phone_no        : "",
        street_no       : "",
        building_suit_no: "",
        state           : "",
        city            : "",
        zip_code        : ""
      },
      shipping_info : {
        first_name      : "",
        last_name       : "",
        email           : "",
        phone_no        : "",
        street_no       : "",
        building_suit_no: "",
        state           : "",
        city            : "",
        zip_code        : ""
      },
      payment_method: "",
      same_address  : false,
      next_btn      : false
    }
  },
  validations() {
    return {
      billing_info  : {
        first_name      : {required, maxLength: maxLength(255)},
        last_name       : {maxLength: maxLength(255)},
        email           : {required, email, maxLength: maxLength(255)},
        phone_no        : {},
        street_no       : {required, maxLength: maxLength(255)},
        building_suit_no: {maxLength: maxLength(255)},
        state           : {required, maxLength: maxLength(255)},
        city            : {required, maxLength: maxLength(255)},
        zip_code        : {required, maxLength: maxLength(100)}
      },
      shipping_info : {
        first_name      : {required, maxLength: maxLength(255)},
        last_name       : {maxLength: maxLength(255)},
        email           : {required, email, maxLength: maxLength(255)},
        phone_no        : {},
        street_no       : {required, maxLength: maxLength(255)},
        building_suit_no: {maxLength: maxLength(255)},
        state           : {required, maxLength: maxLength(255)},
        city            : {required, maxLength: maxLength(255)},
        zip_code        : {required, maxLength: maxLength(100)}
      },
      payment_method: {required}
    }
  },
  mounted() {
    this.get_data()
  },
  methods: {
    async get_data() {
      await axios.get(`/api/order-info/${this.order_id}`).then(res => {
        this.shipping_info.first_name       = res.data.shipping_address.first_name
        this.shipping_info.last_name        = res.data.shipping_address.last_name
        this.shipping_info.email            = res.data.shipping_address.email
        this.shipping_info.phone_no         = res.data.shipping_address.phone_no
        this.shipping_info.street_no        = res.data.shipping_address.street_no
        this.shipping_info.building_suit_no = res.data.shipping_address.building_suit_no
        this.shipping_info.state            = res.data.shipping_address.state
        this.shipping_info.city             = res.data.shipping_address.city
        this.shipping_info.zip_code         = res.data.shipping_address.zip_code
        this.billing_info.first_name        = res.data.billing_address.first_name
        this.billing_info.last_name         = res.data.billing_address.last_name
        this.billing_info.email             = res.data.billing_address.email
        this.billing_info.phone_no          = res.data.billing_address.phone_no
        this.billing_info.street_no         = res.data.billing_address.street_no
        this.billing_info.building_suit_no  = res.data.billing_address.building_suit_no
        this.billing_info.state             = res.data.billing_address.state
        this.billing_info.city              = res.data.billing_address.city
        this.billing_info.zip_code          = res.data.billing_address.zip_code
        this.payment_method                 = res.data.payment_method
        this.subtotal                       = res.data.subtotal
        this.total                          = res.data.total
        this.tax                            = res.data.tax
        this.quantity                       = res.data.quantity
        this.request_id                     = res.data.request
      }).catch(err => {
        console.log(err.response)
      })
    },
    calculate_subtotal() {
      this.subtotal = this.quantity * this.request_obj.cost
      this.calculate_total()
    },
    calculate_total() {
      this.total = this.subtotal + this.tax
    },
    sameAddress() {
      this.same_address = !this.same_address
      if (this.same_address) {
        this.shipping_info = this.billing_info
      } else {
        this.shipping_info = {
          first_name      : "",
          last_name       : "",
          email           : "",
          phone_no        : "",
          street_no       : "",
          building_suit_no: "",
          state           : "",
          city            : "",
          zip_code        : ""
        }
      }
    },
    backBtn() {
      window.location.href = `/user/orders/`
    },
    submitOrder() {
      this.$v.$touch()
      if (this.$v.payment_method.$error) {
        Toast.fire({
          title: 'Payment method is required',
          icon : 'error'
        })
      } else if (!this.$v.$error) {
        let data = {
          billing_address : this.billing_info,
          shipping_address: this.shipping_info,
          payment_method  : this.payment_method,
          subtotal        : this.subtotal,
          total           : this.total,
          tax             : this.tax,
          quantity        : this.quantity,
          user            : this.user_id,
          request         : this.request_id
        }
        axios.put(`/api/order/${this.order_id}/`, data).then(res => {
          this.next_btn = true
          Toast.fire({
            title: 'Order updated successfully',
            icon : 'success'
          })
          setTimeout(() => {
            window.location.href = '/user/orders/'
          }, 2700);
        }).catch(error => {
          console.log(`/api/order/${this.order_id}/`)
          let msg = "Provide all information properly"
          if (error.response.data.request[0]) msg = "Order for this request already exists"
          Toast.fire({
            title: msg,
            icon : 'error'
          })
        })
      }
    }
  }
}
</script>