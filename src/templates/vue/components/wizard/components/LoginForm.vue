<template>
  <div class="row">
    <div class="col-12 col-sm-6 col-md-8 offset-2 ps-0">
      <!--    <h3>Login Form </h3>-->

      <form class="border shadow-sm p-3" @submit.prevent="submit">
        <div class="form-group mb-3">
          <label class="label">Email<span class="text-danger">*</span></label>
          <input type="email" class="form-control" v-model="form.email" required>
        </div>
        <div class="form-group mb-3">
          <label class="label">Password<span class="text-danger">*</span></label>
          <input type="password" class="form-control" v-model="form.password" required>
        </div>
        <div class="form-group mb-3">
          <p>If you don't account <span class="text-primary" @click="$parent.toogle_register" style="cursor:pointer">Create an account</span> here</p>
        </div>

      </form>

    </div>
  </div>
</template>

<script>
export default {
  name: "LoginForm",

  data() {
    return {
      form: {
        email: "",
        password: "",
      },
      showError: false
    };
  },

  methods: {
    async submit() {
      let formdata = {
        "email": this.form.email,
        "password": this.form.password
      }
      await axios.post('/api/api_login/', formdata).then(res => {
        this.$emit("login_submitted", res.data.is_logged_in)

      })

    }
  }


}
</script>

<style scoped>

</style>