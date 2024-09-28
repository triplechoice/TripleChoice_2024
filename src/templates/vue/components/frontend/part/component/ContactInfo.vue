<template>
  <div>
    <div class="field">
      <div :class="{ className: data }"></div>
      <div class="d-flex gap-4 p-3 row" v-if="!isAuthenticated">
        <button @click="toogle_login" class="btn btn-primary w-10" :class="{'btn-secondary' : show }">Login</button>
        <button @click="toogle_register" class="btn btn-primary w-10" :class="{'btn-secondary' : show_register }">Register</button>
        <LoginForm v-show="show" @login_submitted="login_form_subbmitted"></LoginForm>
      </div>
      <div class="row" v-show="show_register">
        <div class="col-3">
          <div class="form-group mb-3">
            <label class="label">First name</label>
            <input type="text" :class="($v.contactForm.first_name.$error) ? 'border-danger' : ''" class="form-control "
                   :disabled="isAuthenticated" v-model="contactForm.first_name">
            <!--            <p v-if="$v.contactForm.name.$error" class="help text-danger">This name is required</p>-->
          </div>
        </div>
        <div class="col-3">
          <div class="form-group mb-3">
            <label class="label">Last name</label>
            <input type="text" :class="($v.contactForm.last_name.$error) ? 'border-danger' : ''" class="form-control "
                   :disabled="isAuthenticated" v-model="contactForm.last_name">
            <!--            <p v-if="$v.contactForm.name.$error" class="help text-danger">This name is required</p>-->
          </div>
        </div>
        <div class="col-6">
          <div class="form-group mb-3">
            <label class="label">Email<span class="text-danger">*</span></label>
            <input @blur="emailValidation" type="email" class="form-control"
                   :class="($v.contactForm.email.$error) ? 'border-danger' : ''"
                   v-model="contactForm.email" :disabled="isAuthenticated">
            <p v-if="$v.contactForm.email.$error || emailError" class="help text-danger">This email field is required
              and provide a valid
              email</p>

          </div>
        </div>
        <div class="col-6">
          <div class="form-group mb-3">
            <label class="label">Phone</label>
            <input type="text" class="form-control" :class="($v.contactForm.phone.$error) ? 'border-danger' : ''"
                   v-model="contactForm.phone" :disabled="isAuthenticated">
            <p v-if="$v.contactForm.phone.$error" class="help text-danger">This phone is required</p>
          </div>
        </div>
        <div class="col-6">
          <div class="form-group mb-3">
            <label class="label">Company Name<span class="text-danger">*</span></label>
            <input type="text" class="form-control" :class="($v.contactForm.companyName.$error) ? 'border-danger' : ''"
                   v-model="contactForm.companyName" :disabled="isAuthenticated">
            <p v-if="$v.contactForm.companyName.$error" class="help text-danger">This company name is required</p>
          </div>
        </div>
        <div class="col-6" v-if="!isAuthenticated">
          <div class="form-group mb-3">
            <label class="label">Password<span class="text-danger">*</span></label>
            <input @blur="checkExistenceUser" type="password" class="form-control"
                   :class="($v.contactForm.password.$error) ? 'border-danger' : ''"
                   v-model="contactForm.password">
            <p v-if="$v.contactForm.password.$error" class="help text-danger">This password field is required</p>
          </div>
        </div>
        <div class="col-6" v-if="!isAuthenticated">
          <div class="form-group mb-3">
            <label class="label">Confirm Password</label>
            <input type="password" class="form-control"
                   :class="($v.contactForm.confirmPassword.$error) ? 'border-danger' : ''"
                   v-model="contactForm.confirmPassword">
            <p v-if="$v.contactForm.confirmPassword.$error" class="help text-danger">Confirm password not match </p>
          </div>
        </div>
        <div class="form-group mb-3">
          <button class="btn btn-primary" type="submit">Register</button>
        </div>
      </div>
    </div>


    <div class="row" v-if="!isAuthenticated">
    </div>
  </div>
</template>

<script>
import {validationMixin} from 'vuelidate'
import {required, email, sameAs} from 'vuelidate/lib/validators'
import {mapGetters} from 'vuex'
import auth from '../../../../mixins/auth'

import LoginForm from "./LoginForm";

export default {
  components: {LoginForm},
  componets : {
    LoginForm
  },

  props : ['clickedNext', 'currentStep'],
  mixins: [validationMixin, auth],
  data() {
    return {
      show           : false,
      isAuthenticated: false,
      emailError     : false,
      isExistenceUser: false,
      show_register  : false
    }
  },
  methods: {
    toogle_login() {
      this.show          = !this.show
      this.show_register = false
    },
    toogle_register() {
      this.show          = false
      this.show_register = !this.show_register
    },
    touchForm() {

      if (this.$v.invalid) this.$v.contactForm.$touch();
      if (!this.$v.$invalid) {

        this.$emit('can-continue', {value: true});
      } else {
        this.$emit('can-continue', {value: false});
      }
    },
    async emailValidation() {
      let params = {
        email: this.contactForm.email
      };
      await axios.get('/api/disposable-email/', {params})
          .then(({data}) => {
            if (data.result === 'yes') {
              this.$emit('can-continue', {value: false});
              this.emailError = true
            } else {
              this.emailError = false
              this.$emit('can-continue', {value: true});
            }
          });
      await this.checkExistenceUser()
    },
    login() {
      window.location.href = '/login?url=' + window.location.pathname;
    },
    async checkExistenceUser() {
      let data = {
        "username": this.contactForm.email,
        "password": this.contactForm.password
      }
      if (data.username !== '' && data.password !== '') {
        await axios.post('/user_exists/', data).then(
            res => {

              if (res.data.success === "success") {
                this.isExistenceUser       = true
                this.contactForm.existUser = "ssss"
              }
            })
            .catch(err => {

              this.isExistenceUser       = false
              this.contactForm.existUser = ""
              // this.touchForm()
            })
      }
    },

    async is_logged_in() {
      await this.checkAuth()
      if (this.authData.username) {
        this.contactForm.first_name  = this.authData.first_name
        this.contactForm.last_name   = this.authData.last_name
        this.contactForm.email       = this.authData.email
        this.contactForm.phone       = this.authData.phone
        this.contactForm.companyName = this.authData.company_name
        this.isAuthenticated         = true
        this.isExistenceUser         = true
      }
      this.touchForm()
    },

    login_form_subbmitted(message) {
      if (message == "not_logged_in") {
        Toast.fire({
          text: "please enter valid email or password",
          icon: "success",
        })
      } else if (message == "logged_in") {
        Toast.fire({
          text: "login successful",
          icon: "success",
        })
            .then(value => {
                  this.is_logged_in()

                  localStorage.setItem('currentStep', JSON.stringify(this.$parent._data.currentStep));
                  window.location.reload()
                }
            );
      }

    },

  },

  computed: {
    ...
        mapGetters(['contactForm'])
  },
  validations() {
    const validations = {
      contactForm: {
        first_name     : {},
        last_name      : {},
        email          : {
          required,
          email
        },
        phone          : {},
        companyName    : {
          required
        },
        password       : {},
        confirmPassword: {},
        existUser      : {}
      }
    };

    if (!this.isAuthenticated) {
      validations.contactForm.password        = {
        required
      }
      validations.contactForm.confirmPassword = {
        sameAsPassword: sameAs('password')
      }
    }
    if (!this.isExistenceUser) {
      validations.contactForm.existUser = {
        required
      }
    }

    return validations;
  },
  async activated() {

    await this.is_logged_in()


    // this.contactForm?.email?.length > 0 ? this.emailValidation() : '';
  },
  async deactivated() {
    this.$store.commit('setContactForm', this.contactForm)
    if (!this.isAuthenticated) {
      await this.emailValidation()
    }
  },
  watch: {
    $v: {
      handler: function (val) {
        if (!val.$invalid) {
          this.$emit('can-continue', {value: true});
        } else {
          this.$emit('can-continue', {value: false});
        }
      },
      deep   : true
    },
    clickedNext(val) {
      if (val === true) {
        this.$v.contactForm.$touch();
      }
    }
  },
}
</script>