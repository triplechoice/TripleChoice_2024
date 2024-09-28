<template>
  <div style="padding: 2rem 3rem; text-align: left;">
    <div class="row justify-content-between border p-3">
      <div class="col-md-6 col-xs-12" v-for="(specification, index1) in parts.partclassification_set">
        <div class="card">
          <div class="card-header bg-success text-white">
            {{ specification.classification.title }}
          </div>
          <div class="card-body">
            <div class="form-group mb-3"
                 v-for="(partclassificationattribute_set, index2) in specification.partclassificationattribute_set">
              <label class="label">{{ partclassificationattribute_set.attribute.title }} <span
                  v-if="partclassificationattribute_set.is_optional != 'True' && specification.is_optional != 'True'" class="text-danger">*</span></label>
              <div class="input-group inline-group">
                <input v-model="partclassificationattribute_set.attribute.value"
                       v-if="{'text':'text', 'number':'number'}[partclassificationattribute_set.attribute.type]"
                       :type="partclassificationattribute_set.attribute.type" class="form-control" style="width: 60%">
                <select v-if="partclassificationattribute_set.attribute.unit.length > 0"
                        v-model="partclassificationattribute_set.attribute.unit_value" class="form-select mx-2">
                  <option value="" selected>Select</option>
                  <option v-for="(unit, index2) in partclassificationattribute_set.attribute.unit" :value="unit.id">
                    {{ unit.title }}
                  </option>
                </select>


              </div>
              <select v-model="partclassificationattribute_set.attribute.value"
                      v-if="partclassificationattribute_set.attribute.type == 'select' " class="form-select">
                <option value="">unit</option>
                <template v-if="partclassificationattribute_set.attribute.options">
                  <option v-model="partclassificationattribute_set.attribute.unit.value"
                          v-for="option in partclassificationattribute_set.attribute.options.split(',')"
                          :value="option">
                    {{ option }}
                  </option>
                </template>
              </select>

              <!--              test code -->
              <!--              <p v-if="$v.parts.partclassification_set.$each.$iter[index1].$error" class="help text-danger">-->
              <!--                This name is required</p>-->
              <p v-if="$v.parts.partclassification_set.$each.$iter[index1].partclassificationattribute_set.$each.$iter[index2].attribute.value.$error"
                 class="help text-danger">

                This name is required</p>


                   <p v-if="$v.parts.partclassification_set.$each.$iter[index1].partclassificationattribute_set.$each.$iter[index2].attribute.unit_value.$error"
                 class="help text-danger">

                please select a unit</p>


            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>
<script>
import {validationMixin} from 'vuelidate'
import {required, email, minLength, requiredUnless} from 'vuelidate/lib/validators'
import {mapGetters} from 'vuex'

export default {
  props: ['clickedNext', 'currentStep'],
  mixins: [validationMixin],
  data() {
    return {
      order_id: ''
    }
  },
  validations() {
    return {
      parts: {
        partclassification_set: {
          $each: {
            partclassificationattribute_set: {
              required: function (value, object) {
                if (object.is_optional == "True") {   //  True value is passed as string  so checked as string
                  for (let attr of object.partclassificationattribute_set) {
                    attr.attribute.is_optional = true
                  }
                } else {
                  for (let attr of object.partclassificationattribute_set) {
                    if (attr.is_optional == "True") {     //  True value is passed as string  so checked as string
                      attr.attribute.is_optional = true
                    } else {
                      attr.attribute.is_optional = false
                    }
                  }
                }
                return true
              },
              $each: {
                attribute: {
                  value: {
                    required: function (value, object) {
                      if (value.length > 0) {
                        return true
                      }
                      return object.is_optional
                    },
                  },
                  unit_value: {
                    required: function (value, object) {

                      if (object.unit.length <=0){
                        return true
                      }
                      if(object.value.length <= 0 ){
                        return true
                      }

                      if(value > 0) {
                        return true
                      }

                      return false
                    }
                  }
                }
              },
            }
          }
        }
      }
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
      deep: true
    },
    clickedNext(val) {
      if (val === true) {
        this.$v.parts.$touch();
      }
    }
  },
  computed: {
    ...mapGetters(['form', 'parts']),
  },
  deactivated() {
    this.$store.commit('setParts', this.parts);
  },
  activated() {
    // this.touchForm()
  },
  mounted() {
    this.order_id = this.$parent.$parent.order_id
    if (this.order_id != "None") {
      this.getOrderPart();
    } else {
      this.getPart();
    }
    if (!this.$v.$invalid) {
      this.$emit('can-continue', {value: true});
    } else {
      this.$emit('can-continue', {value: false});
    }
  },
  methods: {
    getPart() {
      let partSlug = window.location.pathname.split("/")[2]
      axios.get(`/api/part/${partSlug}`)
          .then(res => {
            if (this.parts && this.parts.slug != partSlug) {
              // this.parts = res.data
              this.$store.commit('setParts', res.data)
            }
          })


    },
    getOrderPart() {
      axios.get('/api/request/part/' + this.order_id)
          .then(res => {
            this.$store.commit('setParts', res.data.answer)
            this.$store.commit('setCommentForm', res.data.comment)
            this.$store.commit('setSubmitForm', {'quantity': res.data.quantity, 'type': res.data.type})
          })
          .catch(err => {

            this.order_id = ''
                Toast.fire({
                  text:  err.response.data.detail,
                  icon  : "error",
                 });
          })
    },

    touchForm() {
      if (this.$v.parts) {
        this.$v.parts.$touch();
      }

      if (!this.$v.$invalid) {
        this.$emit('can-continue', {value: true});
      } else {
        this.$emit('can-continue', {value: false});
      }
    },
  },
}
</script>
