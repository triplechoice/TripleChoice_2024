 <template>
  <div style="padding: 2rem 3rem; text-align: left;">
    <div class="field border p-3">
      <div class="row">
        <div class="col-6">
          <div class="form-group mb-3">
            <label class="label">Quantity<span class="text-danger">*</span></label>
            <input type="number" :class="($v.submitForm.quantity.$error) ? 'border-danger' : ''" class="form-control"
                   v-model="submitForm.quantity">
            <p v-if="$v.submitForm.quantity.$error" class="help text-danger">This quantity is required</p>
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
import {required, decimal} from 'vuelidate/lib/validators'
import {mapGetters} from 'vuex'

export default {
  props : ['clickedNext', 'currentStep'],
  mixins: [validationMixin],
  data() {
    return {}
  },
  validations: {
    submitForm: {
      quantity: {
        required,
        decimal
      },
      type    : {
        required,
      },
    }
  },
  watch      : {
    "submitForm": {
      deep   : true,
      handler: function (newVal) {
        this.$store.commit('setSubmitForm', newVal);
      },
    },
    $v          : {
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
        this.$v.submitForm.$touch();
      }
    }
  },
  computed   : {
    ...mapGetters(['submitForm'])
  },
  activated() {
    this.touchForm()
  },
  methods: {
    touchForm() {
      if (this.$v.invalid) this.$v.submitForm.$touch();
      if (!this.$v.$invalid) {
        this.$emit('can-continue', {value: true});
      } else {
        this.$emit('can-continue', {value: false});
      }
    },
  }
}
</script>