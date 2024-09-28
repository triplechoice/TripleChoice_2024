<template>
  <div>
    <SearchParts ref="searchParts"></SearchParts>
    <section class="section">
      <div class="container">
        <div class="columns">
          <div class="column is-8 is-offset-2">
            <horizontal-stepper
                ref="stepper"
                :steps="demoSteps"
                @completed-step="completeStep"
                @active-step="isStepActive"
                @stepper-finished="submitPartForm"
                @clicking-back="clickedBack"
            >
            </horizontal-stepper>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
<script>
import HorizontalStepper from 'vue-stepper';
import Specification from './component/Specification.vue';
import Comment from './component/Comment.vue';
import ContactInfo from './component/ContactInfo.vue';
import SubmitPage from './component/SubmitPage.vue';
import SearchParts from '../homepage/Index'
import {mapGetters} from 'vuex'

import auth from '../../../mixins/auth'

export default {
  components: {
    HorizontalStepper, SearchParts
  },
  mixins: [auth],
  props: ['part', 'order_id'],
  data() {
    return {
      logged_in_contact_form: {},
      completeForm: {},
      demoSteps: [
        {
          icon: 'note',
          name: 'first',
          title: 'Specification',
          component: Specification,
          completed: false

        },
        {
          icon: 'mail',
          name: 'second',
          title: 'Comment',
          component: Comment,
          completed: false
        },
        {
          icon: 'person',
          name: 'third',
          title: 'Contact Info',
          component: ContactInfo,
          completed: false
        },
        {
          icon: 'forward',
          name: 'fourth ',
          title: 'Submit',
          component: SubmitPage,
          completed: false
        }
      ],
    }
  },
  computed: {
    ...mapGetters(['parts', 'contactForm', 'commentForm', 'submitForm'])
  },
  async mounted() {
    this.$store.commit('emptyForm')
    await this.handle_logged_in_user()
    let currentStep = JSON.parse(localStorage.getItem('currentStep'));
    if (currentStep) {
      this.$refs.stepper.currentStep.index = currentStep.index
      this.$refs.stepper.currentStep.name = this.demoSteps[currentStep.index].name
      if (currentStep.index == this.demoSteps.length - 1) {
        this.$refs.stepper.finalStep = true
      }
      localStorage.removeItem('currentStep')
    }
  },
  methods: {
    clickedBack() {
      this.$refs.stepper.canContinue = true;
    },
    // Executed when @completed-step event is triggered
    completeStep(payload) {
      this.demoSteps.forEach((step) => {
        if (step.name === payload.name) {
          step.completed = true;
        }

      })
    },
    // Executed when @active-step event is triggered
    isStepActive(payload) {
      this.demoSteps.forEach((step) => {
        if (step.name === payload.name) {
          if (step.completed === true) {
            step.completed = false;
          }
        }
      })
    },
    submitPartForm() {
      let formData = this.formData()

      if (this.order_id != 'None') {
        axios.put('/api/request/update/' + this.order_id, formData)
            .then(res => {
              this.$store.commit('emptyForm')
              window.location.href = '/user/requests/'
            })
            .catch(err => {
              Toast.fire({
                text: err.response.data.detail,
                icon: "error",
              });
              this.$store.commit('emptyForm')
            })
      } else {
        axios.post('/api/request/', formData)
            .then(res => {
              this.$store.commit('emptyForm')

              if (res.data.is_logged_in ) {

                window.location.href = '/user/requests/?template=request-detaials'
              } else {

                let text = "order submitted please check your  email for account activation"


                Toast.fire({
                  text: text,
                  icon: "success",
                }).then(value => {
                      window.location.href = '/'
                    }
                );
              }

            })
            .catch(err => {

              Toast.fire({
                text: err.response.data[0],
                icon: "error",
              });

            })
      }

    },
    formData() {
      return {
        "answer": this.parts,
        "comment": this.commentForm.comment,
        "contact_info": this.contactForm,
        "quantity": this.submitForm.quantity,
        "type": this.submitForm.type,
        "part": this.parts.id
      }
    },

    async handle_logged_in_user() {
      await this.checkAuth()
      if (this.authData.username) {
        this.logged_in_contact_form.first_name = this.authData.first_name
        this.logged_in_contact_form.last_name = this.authData.last_name
        this.logged_in_contact_form.email = this.authData.email
        this.logged_in_contact_form.phone = this.authData.phone
        this.logged_in_contact_form.companyName = this.authData.company_name

        this.$store.commit('setContactForm', this.logged_in_contact_form)
        this.demoSteps = this.demoSteps.filter(function (el) {
          return el.name != "third";
        });

      }

    }


  }
}
</script>