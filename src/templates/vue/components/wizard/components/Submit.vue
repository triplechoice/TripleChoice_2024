<template>
  <div>
    <!--    <contact-info ref="contactInfo"></contact-info>-->
    <div class="field border shadow-sm p-3">
      <div class="row">
        <div class="col-12 col-sm-6">
          <div class="form-group mb-3">
            <label class="label">Quantity<span class="text-danger">*</span></label>
            <input type="number" :class="($v.submitForm.quantity.$error) ? 'border-danger' : ''" class="form-control"
                   v-model="submitForm.quantity">
            <p v-if="!$v.submitForm.quantity.mustBeGreaterThanOne && $v.submitForm.quantity.$model !== ''"
               class="help text-danger">Quantity must be greater than 1</p>
            <p v-else-if="$v.submitForm.quantity.$error" class="help text-danger">This quantity is required</p>
          </div>
          <div class="form-group mb-3">
            <label class="label">Zip Code<span class="text-danger">*</span></label>
            <input type="text" :class="($v.submitForm.zip_code.$error) ? 'border-danger' : ''" class="form-control"
                   v-model="submitForm.zip_code">
            <p class="help text-danger" v-if="!$v.submitForm.zip_code.minLength">zip code should be at least
              {{ $v.submitForm.zip_code.$params.minLength.min }} digits.</p>
            <p v-else-if="$v.submitForm.zip_code.$error" class="help text-danger">This zip code is required</p>
          </div>
        </div>
        <div class="col-12">
          <div class="form-group mb-3 mt-4 ">
            <div class="form-check form-check-inline">
              <input :class="($v.submitForm.type.$error) ? 'border-danger' : ''" class="form-check-input" checked
                     type="radio" name="type" id="type1"
                     value="query" v-model="submitForm.type">
              <label class="form-check-label" for="type1">For Query</label>
            </div>
            <div class="form-check form-check-inline">
              <input :class="($v.submitForm.type.$error) ? 'border-danger' : ''" class="form-check-input" type="radio"
                     name="type" id="type2" value="quote" v-model="submitForm.type">
              <label class="form-check-label" for="type2">For Quote</label>
            </div>
            <p v-if="$v.submitForm.type.$error" class="help text-danger">This type is required</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {validationMixin} from 'vuelidate'
import {required, integer, minLength} from 'vuelidate/lib/validators'
import {mapGetters} from 'vuex'
import ContactInfo from "@/components/wizard/components/ContactInfo";


const mustBeGreaterThanOne = (value) => value > 0

export default {
  name: "SubmitForm",
  components: {ContactInfo},
  mixins: [validationMixin],
  computed: {
    ...mapGetters(['submitForm'])
  },
  data() {
    return {}
  },
  validations: {
    submitForm: {
      quantity: {
        required,
        integer,
        mustBeGreaterThanOne
      },
      zip_code: {
        required,
        minLength: minLength(5)
      },
      type: {
        required,
      },
    }
  },
  watch: {
    $v: {
      handler: function (val) {
      },
      deep: true
    },
  },
}
</script>

<style scoped>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  opacity: 1;

}

</style>