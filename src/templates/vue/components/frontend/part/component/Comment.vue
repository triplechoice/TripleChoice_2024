<template>
  <div style="padding: 2rem 3rem; text-align: left;">
    <div class="field border p-3">
      <label class="label">Comment</label>
      <div class="control">
        <textarea @keyup="commentText"
                  :class="['input', ($v.commentForm.comment.$error) ? 'border-danger' : '']" class="form-control"
                  v-model="commentForm.comment"></textarea>
      </div>
      <p v-if="$v.commentForm.comment.$error" class="help text-danger">This comment is invalid</p>
    </div>
  </div>
</template>

<script>
import {validationMixin} from 'vuelidate'
import {required, email} from 'vuelidate/lib/validators'
import {mapGetters} from 'vuex'

export default {
  props : ['clickedNext', 'currentStep'],
  mixins: [validationMixin],
  data() {
    return {}
  },
  validations: {
    commentForm: {
      comment: {},
    }
  },
  watch      : {
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

    }
  },
  computed   : {
    ...mapGetters(['commentForm'])
  },
  mounted() {
    this.touchForm();
  },
  activated() {
    this.touchForm()
  },
  methods: {
    touchForm() {
      this.$v.commentForm.comment.$touch();
      if (!this.$v.$invalid) {
        this.$emit('can-continue', {value: true});
      } else {
        this.$emit('can-continue', {value: false});
      }
    },
    commentText() {
      this.$store.commit('setCommentForm', this.commentForm.comment)
    }
  }
}
</script>