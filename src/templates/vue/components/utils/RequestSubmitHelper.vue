<template>
  <div class="align-items-center d-flex justify-content-center" style="min-height: 25vh"><i
      class="fa-circle-notch fa-spin fas fs-1 text-primary"></i></div>
</template>

<script>
import requestSubmitHelper from "../../mixins/auth"

export default {
  name  : "RequestSubmitHelper",
  mixins: [requestSubmitHelper],
  mounted() {
    this.requestSubmitHelper()
  },
}
</script>
