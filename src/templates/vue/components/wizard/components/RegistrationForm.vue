<template>
  <div class="row" >
        <div class="col-12">
          <div class="border shadow-sm m-1 p-3 row">
            <div class="col-12 col-sm-3">
              <div class="form-group mb-3">
                <label class="label">First name</label>
                <input type="text" :class="($v.contactForm.first_name.$error) ? 'border-danger' : ''"
                       class="form-control "
                       :disabled="isAuthenticated" v-model="contactForm.first_name">
                <!--            <p v-if="$v.contactForm.name.$error" class="help text-danger">This name is required</p>-->
              </div>
            </div>
            <div class="col-12 col-sm-3">
              <div class="form-group mb-3">
                <label class="label">Last name</label>
                <input type="text" :class="($v.contactForm.last_name.$error) ? 'border-danger' : ''"
                       class="form-control "
                       :disabled="isAuthenticated" v-model="contactForm.last_name">
                <!--            <p v-if="$v.contactForm.name.$error" class="help text-danger">This name is required</p>-->
              </div>
            </div>
            <div class="col-sm-6">
              <div class="form-group mb-3">
                <label class="label">Email<span class="text-danger">*</span></label>
                <input id="emailfield" @blur="emailValidation" type="email" class="form-control"
                       :class="($v.contactForm.email.$error) ? 'border-danger' : ''"
                       v-model="contactForm.email" :disabled="isAuthenticated">
                <p v-if="$v.contactForm.email.$error || emailError" class="help text-danger">This email field is
                  required
                  and provide a valid
                  email </p>

              </div>
            </div>
            <div class="col-sm-6">
              <div class="form-group mb-3">
                <label class="label">Phone</label>
                <input type="text" class="form-control" :class="($v.contactForm.phone.$error) ? 'border-danger' : ''"
                       v-model="contactForm.phone" :disabled="isAuthenticated">
                <p v-if="$v.contactForm.phone.$error" class="help text-danger">This phone is required</p>
              </div>
            </div>
            <div class="col-sm-6">
              <div class="form-group mb-3">
                <label class="label">Company Name<span class="text-danger">*</span></label>
                <input type="text" class="form-control"
                       :class="($v.contactForm.companyName.$error) ? 'border-danger' : ''"
                       v-model="contactForm.companyName" :disabled="isAuthenticated">
                <p v-if="$v.contactForm.companyName.$error" class="help text-danger">This company name is required</p>
              </div>
            </div>
            <div class="col-sm-6" v-if="!isAuthenticated">
              <div class="form-group mb-3">
                <label class="label">Password<span class="text-danger">*</span></label>
                <input @blur="checkExistenceUser" type="password" class="form-control"
                       :class="($v.contactForm.password.$error) ? 'border-danger' : ''"
                       v-model="contactForm.password">
                <p v-if="$v.contactForm.password.$error" class="help text-danger">This password field is required</p>
              </div>
            </div>
            <div class="col-sm-6" v-if="!isAuthenticated">
              <div class="form-group mb-3">
                <label class="label">Confirm Password</label>
                <input type="password" class="form-control"
                       :class="($v.contactForm.confirmPassword.$error) ? 'border-danger' : ''"
                       v-model="contactForm.confirmPassword">
                <p v-if="$v.contactForm.confirmPassword.$error" class="help text-danger">Confirm password not match </p>
              </div>
            </div>
            <div class="form-group mb-3">
               <p>If you already have an account <span class="text-primary" @click="$parent.toogle_login" style="cursor:pointer">Sign In </span> here</p>
            </div>
          </div>
        </div>
      </div>
</template>

<script>
import auth                      from "../../../mixins/auth";
import {validationMixin}         from 'vuelidate'
import {mapGetters}              from 'vuex'
import {required, email, sameAs} from 'vuelidate/lib/validators'

export default {
  name: "RegistrationForm",
  mixins    : [validationMixin, auth],
  data() {
    return {
      isAuthenticated: false,
      emailError     : false,
      isExistenceUser: false,
    }
  },
  computed: {
    ...mapGetters(['contactForm'])
  },
  methods:{
     async emailValidation() {
      let params = {
        email: this.contactForm.email
      };
      await axios.get('/api/disposable-email/', {params})
          .then(({data}) => {
            if (data.result === 'yes') {
              this.emailError = true
              this.$v.contactForm.$touch();
            } else {
              this.emailError = false
              this.$v.contactForm.$touch();
            }
          });
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
                this.isExistenceUser       = false
                this.contactForm.existUser = "ssss"
                this.emailError            = false
                this.$v.contactForm.$touch();
              }
            })
            .catch(err => {
              this.isExistenceUser       = false
              this.contactForm.existUser = ""
              this.emailError            = true
              this.$v.contactForm.$touch();
              Toast.fire({
                icon : "error",
                title: "This email has already an account. But password not match"
              })

            })
      }
    },
  },
  validations() {
    const validations = {
      contactForm: {
        first_name     : {},
        last_name      : {},
        email          : {
          required: function (value, obj) {
            if (value.length <= 0) {
              return false
            }
            return !this.emailError
          },
          email,
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
  watch: {
    $v: {
      handler: function (val) {
      },
      deep   : true
    },
  },
}

</script>

<style scoped>

</style>