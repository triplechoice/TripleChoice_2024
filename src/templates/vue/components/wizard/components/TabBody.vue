<template>
  <div>
    <div class="card">
      <div class="card-body">
        <component ref="tabComponent" :is="tab"></component>
      </div>
    </div>
    <div class="card-footer text-end bg-white border-0 px-0" style="border-top: none">
      <button v-if="tabState.prevState" class="btn px-4 btn-primary mr-2" @click="prevPage">
        Back
      </button>
      <button v-if="tabState.nextState" class="btn px-4 btn-primary" @click="nextPage">
        Next
      </button>
      <button v-else class="btn px-4 btn-primary" @click="submitPartForm">
        Submit
      </button>
    </div>
    <!-- Button trigger modal -->
    <button type="button" id="loginBtnModal" class="btn btn-primary" style="display: none" data-bs-toggle="modal"
            data-bs-target="#loginModal" data-backdrop="static" data-keyboard="false">
      Launch demo modal
    </button>

    <!-- Modal -->
    <div class="modal fade" id="loginModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
         aria-labelledby="staticBackdropLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">{{ authenticationModalTitle }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <LoginForm v-if="show_login" ref="login" @login_submitted="login_form_subbmitted"></LoginForm>
            <registration-form v-else ref="registration"></registration-form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button v-if="show_login" @click="$refs.login.submit()" type="button" class="btn btn-primary">Sign In
            </button>
            <button v-else @click="registarionFormSubmit()" type="button" class="btn btn-primary">Submit</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>

import Specification       from "../components/Specification";
import Comment             from "../components/Comment";
import ContactInfo         from "../components/ContactInfo";
import LoginForm           from "../components/LoginForm";
import Submit              from "../components/Submit";
import {mapGetters}        from 'vuex';
import auth                from "../../../mixins/auth";
import requestSubmitHelper from "../../../mixins/auth"
import Swal                from 'sweetalert2'
import RegistrationForm    from "./RegistrationForm";

export default {
  name      : "TabBody",
  components: {RegistrationForm, Submit, ContactInfo, Comment, Specification, LoginForm},
  mixins    : [auth, requestSubmitHelper],
  props     : ['tab', 'part', 'order_id'],
  data() {
    return {
      logged_in_contact_form  : {},
      tabState                : {
        nextState   : '',
        prevState   : '',
        currentState: '',
        currentIndex: ''
      },
      tabList                 : Object.entries(this.$parent.$refs.tabList.tabs),
      tabListInfo             : Object.values(this.$parent.$refs.tabList.tabs),
      authenticationModalTitle: "Sign In",
      show_login              : true
    }
  },
  computed: {
    ...mapGetters([
      'form', 'parts', 'commentForm', 'contactForm', 'submitForm', 'getIsLoggedIn', 'getIsRegisterClicked'
    ])
  },
  mounted() {
    this.handle_logged_in_user()
    this.setTabState()
  },
  methods: {
    async handle_logged_in_user() {
      await this.checkAuth()
      if (this.authData.username) {
        this.logged_in_contact_form.first_name  = this.authData.first_name
        this.logged_in_contact_form.last_name   = this.authData.last_name
        this.logged_in_contact_form.email       = this.authData.email
        this.logged_in_contact_form.phone       = this.authData.phone
        this.logged_in_contact_form.companyName = this.authData.company_name

        this.$store.commit('setContactForm', this.logged_in_contact_form)
        this.$store.commit('setIsLoggedIn', true)
        let tempTabs = {...this.$parent.$refs.tabList.tabs}
        delete tempTabs.ContactInfo
        this.$parent.$refs.tabList.tabs = tempTabs
      } else {
        this.$store.commit('setIsLoggedIn', false)
      }
    },

    async contactFormAuth() {

      const contactFormData = this.$refs.tabComponent._computedWatchers.contactForm.value
      let formdata          = {
        "email"   : contactFormData.email,
        "password": contactFormData.password
      }
      await axios.post('/api/api_login/', formdata).then(res => {

        if (res.data.is_logged_in != "no_user_found") {
          this.$refs.tabComponent.login_form_subbmitted(res.data.is_logged_in)
        }
        if (res.data.is_logged_in == "no_user_found") {
          this.$parent.$refs.tabList.switchTab(this.tabState.nextState)
        }
      })

    },
    async nextPage() {
      if (this.tabState.currentState == "Specification") {
        this.$refs.tabComponent.$v.parts.$touch();
        if (!this.$refs.tabComponent.$v.$error) {
          this.$store.commit('setParts', this.parts);
          this.$parent.$refs.tabList.switchTab(this.tabState.nextState)
        }
      } else if (this.tabState.currentState == "Comment") {
        this.$refs.tabComponent.$v.commentForm.$touch();
        if (!this.$refs.tabComponent.$v.$error) {
          this.$store.commit('setCommentForm', this.commentForm);
          this.$parent.$refs.tabList.switchTab(this.tabState.nextState)
        }
      } else if (this.tabState.currentState == "ContactInfo") {
        if (this.$refs.tabComponent.contactForm.email) {
          await this.$refs.tabComponent.checkExistenceUser()
        }
        this.$refs.tabComponent.$v.contactForm.$touch();
        if (!this.$refs.tabComponent.$v.$error) {
          this.$store.commit('setContactForm', this.contactForm)

          await this.contactFormAuth()

        }
      }
    },
    prevPage() {
      this.$parent.$refs.tabList.switchTab(this.tabState.prevState)
    },
    setTabState() {
      this.tabList.forEach((tab, index) => {
        const tabData = this.$parent.$refs.tabList.tabs[tab[0]];
        if (tab[0] === this.tab) {
          if (index != 0) {
            this.tabState.prevState = this.tabList[index - 1][0];
          } else {
            this.tabState.prevState = ''
          }
          this.tabState.currentState = tabData.title;
          if (index < (this.tabList.length - 1)) {
            this.tabState.nextState = this.tabList[index + 1][0];
          } else {
            this.tabState.nextState = ''
          }
        }
        if (tab[0] === this.tabState.currentState) {
          this.tabState.currentIndex = this.tabList[index][1].iconText
        }
        setTimeout(() => {
          if (tab[1].iconText < this.tabState.currentIndex) {
            this.$parent.$refs.tabList.tabs[tab[0]].isIcon = true
          } else {
            this.$parent.$refs.tabList.tabs[tab[0]].isIcon = false
          }
        }, 300)

      })
    },
    submitPartForm() {
      this.$refs.tabComponent.$v.submitForm.$touch();
      if (!this.$refs.tabComponent.$v.$error) {
        if (this.getIsLoggedIn) {
          this.requestSubmitHelper(true)
        } else {
          document.querySelector("#loginBtnModal").click();
        }
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
        this.$store.commit('setIsLoggedIn', true)
      } else {
        this.$store.commit('setIsLoggedIn', false)
      }
    },
    registarionFormSubmit() {
      this.$refs.registration.$v.contactForm.$touch();
      this.$refs.registration.emailValidation()
      if (!this.$refs.registration.$v.contactForm.$error) {
        this.requestSubmitHelper()
      }
    },
    login_form_subbmitted(message) {
      if (message == "not_logged_in" || message == "no_user_found") {
        Toast.fire({
          text: "please enter valid email or password",
          icon: "error",
        })
      } else if (message == "logged_in") {
        if (!this.getIsLoggedIn) {
          this.is_logged_in();
        }
        window.location.href = '/request/submit/helper'
      }

    },
    toogle_login() {
      this.authenticationModalTitle = "Sign In"
      this.show_login               = true
    },
    toogle_register() {
      this.authenticationModalTitle = "Create an account"
      this.show_login               = false
    },
  }
  ,
  watch: {
    tab: function (newVal, oldVal) {
      this.setTabState();
    }
  }
  ,
}

</script>

<style scoped>

</style>