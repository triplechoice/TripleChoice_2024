<template>
  <div>
    <div class="field">
      <label class="label fw-bold">Comment</label>
      <div class="control form-group">
        <textarea class="form-control" v-model="commentForm.comment"></textarea>
      </div>

      <div class="form-group">
        <input type="file" class="form-control" @input="addFile($event)">
      </div>
      <p v-if="$v.commentForm.comment.$error" class="help text-danger">This comment is invalid</p>
    </div>
  </div>
</template>

<script>
import {validationMixin} from 'vuelidate'
import {mapGetters} from 'vuex'
import {required} from 'vuelidate/lib/validators'

export default {
  name    : "Comment",
  mixins  : [validationMixin],
  computed: {
    ...mapGetters(['commentForm'])
  },
  data() {
    return {}
  },
  mounted(){
  },
  validations: {
    commentForm: {
      comment: {},
      file_comment:{},
    }
  },
  methods:{
    addFile(e) {
      
      let files = e.target.files || e.dataTransfer.files;
      if (files.length) {
          this.commentForm.file_comment = e.target.files[0];
      }
  },
  },
  

  watch      : {
    $v         : {
      handler: function (val) {
        console.log('aaa')
      }
    }
  }
}
</script>

<style scoped>
.control {
  min-height: 235px;
}
textarea{
  min-height : 204px !important;
}
</style>