<template>
  <div>
    <form @submit.prevent="checkExistance()" id="part">
      <div class="card">
        <div class="card-header">
          Add Part
        </div>
        <div class="card-body">

          <div class="row">
            <div class="col-md-4">
              <h3>Part Summery</h3>
              <div class="mb-3">
                <label :class="errors.title ? 'text-danger' : ''" class="form-label">Title</label>
                <div class="">
                  <input v-model="title" type="text" class="form-control" :class="errors.title ? 'border-danger' : ''">
                  <span class="help-block text-danger" v-if="errors.title">{{ this.errors.title[0] }}</span>
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <div class="">
                  <textarea v-model="description" cols="30" rows="5" class="form-control"></textarea>
                </div>
              </div>
            </div>

          </div>
          <!--          <hr>-->
          <div class="row">
            <!--            <div class="card-header mb-5">-->
            <!--              Part Specifications-->
            <!--            </div>-->
            <h3>Part Specifications</h3>
            <div class="col-md-4 mb-4" v-for="(classification, index) in classifications" :key="index">
              <div class="card">
                <div class="card-header">
                  <button v-if="classifications.length > 1" @click="removeClassification(index)" type="button"
                          class="btn btn-danger float-end py-0" style="margin-right: -10px; margin-top: -10px">
                    -
                  </button>
                  <div class="mb-3">
                    <label class="form-label"
                           :class="errors.classifications && errors.classifications[index] && errors.classifications[index].value ? 'text-danger': ''">Classification</label>
                    <div class="">
                      <select v-model="classification.value" class="form-select py-0"
                              :class="errors.classifications && errors.classifications[index] && errors.classifications[index].value ? 'border border-danger':''"
                              @change="getAttribute($event, index)">
                        <!--                        <option selected>Open this select menu</option>-->

                        <option v-if="msg" :value="classification.value"> {{ classification.title }}</option>
                        <option v-else value="">Open this select menu</option>

                        <option :value="classificationList.id" v-for="classificationList in classificationLists">
                          {{ classificationList.title }}
                        </option>
                      </select>
                      <div
                          v-if="errors.classifications && errors.classifications[index] && errors.classifications[index].value">
                        <span class="help-block text-danger"> {{ errors.classifications[index].value[0] }}</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="card-body">
                  <div class="mb-3" v-for="(input, at_index) in classification.attribute" :key="at_index">
                    <label class="form-label"
                           :class="errors.classifications && errors.classifications[index] && errors.classifications[index].attribute[at_index] ? 'text-danger':'' ">Attribute</label>
                    <div class="input-group">
                      <select class="form-select py-0 mr-2"
                              :class="errors.classifications && errors.classifications[index] && errors.classifications[index].attribute[at_index] ? 'border border-danger':'' "
                              :id="`attribute${at_index}`"
                              v-model="input.value" @change="selectAttribute($event, index, at_index)">
                        <!--                        <option v-if="msg" :value="">{{ item.title }}</option>-->
                        <option value="">Open this select menu</option>

                        <option :value="item.id" v-for="item in classification.items">{{ item.title }}</option>
                      </select>

                      <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="" :id="`isOptional${index}${at_index}`"
                               v-model="input.isOptional">
                        <label class="form-check-label" :for="`isOptional${index}${at_index}`">
                          is optional
                        </label>
                        <button v-if="classification.attribute.length > 1" type="button"
                                @click="removeAttribute(index, at_index)"
                                class="btn btn-danger py-0 ml-2">-
                        </button>
                      </div>
                    </div>
                    <div
                        v-if="errors.classifications && errors.classifications[index] && errors.classifications[index].attribute[at_index]">
                      <span class="help-block text-danger">{{
                          errors.classifications[index].attribute[at_index].value[0]
                        }}</span>
                    </div>
                  </div>
                  <button type="button" @click="addAttribute(index)" class="btn btn-success btn-sm">
                    + Add more attribute
                  </button>
                </div>
                <div class="card-footer">
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" :id="`isOptional${index}`"
                           v-model="classification.isOptional">
                    <label class="form-check-label" :for="`isOptional${index}`">
                      is optional
                    </label>
                  </div>
                </div>
              </div>


            </div>
            <div class="col-md-4">
              <button type="button" class="btn btn-success" @click="addClassification">+</button>
            </div>
          </div>

        </div>
        <div class="card-footer">
          <button @click="updatePart()" class="btn btn-primary float-start" type="button" v-if="msg">Update</button>
          <button v-else class="btn btn-success float-start" type="submit">Save</button>
          <button @click="reset()" class="btn btn-danger float-end" type="button">Reset</button>
        </div>
      </div>
    </form>

    <!--    TODO:show current part-->
    <div v-if="showModal">
      <transition name="modal">
        <div class="modal-mask">
          <div class="modal-wrapper">
            <div class="modal-dialog modal-xl modal-dialog-scrollable" role="document">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title">Modal title</h5>
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true" @click="showModal = false">&times;</span>
                  </button>
                </div>
                <div class="modal-body">
                  <div class="card mb-3 ">
                    <div class="card-header bg-primary text-white py-1">
                      Current part
                    </div>
                    <div class="card-body p-0">
                      <table class="table table-bordered table-striped table-hover mb-0">

                        <tbody>
                        <tr>
                          <td>{{ title }}</td>
                          <td>
                            <ul>
                              <li style="list-style: none" v-if="classifications"
                                  v-for="classification in classifications">

                                <ul class="p-0">
                                  <li class="list-group-item bg-primary text-white">
                                    {{ classification.title }}
                                  </li>
                                  <li class="list-group-item">
                                    <label class="badge bg-success ml-1" v-if="classification.attribute"
                                           v-for="attribute in classification.attribute">
                                      {{ attribute.title }}
                                    </label>
                                  </li>
                                </ul>
                              </li>
                            </ul>
                          </td>
                        </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                  <div class="card ">
                    <div class="card-header bg-primary text-white py-1">
                      Similar Parts
                    </div>
                    <div class="card-body p-0">
                      <table class="table table-bordered table-striped  mb-0">

                        <tbody>
                        <tr v-if="similarPart" v-for="part in similarPart">
                          <td>{{ part.title }}</td>
                          <td>
                            <ul>
                              <li style="list-style: none" v-if="part.partclassification_set"
                                  v-for="partclassification_set in part.partclassification_set">

                                <ul class="p-0">
                                  <li class="list-group-item bg-primary text-white">
                                    {{ partclassification_set.classification.title }}
                                  </li>
                                  <li class="list-group-item">
                                    <label class="badge bg-success ml-1"
                                           v-for="partclassificationattribute_set in partclassification_set.partclassificationattribute_set">
                                      {{ partclassificationattribute_set.attribute.title }}
                                    </label>
                                  </li>
                                </ul>
                              </li>
                            </ul>
                          </td>
                        </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" @click="showModal = false">Close</button>
                  <button type="button" class="btn btn-primary" @click="savePart()">Save changes</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Part',
  props: {
    msg: String
  },
  data() {
    return {
      title: '',
      description: '',
      counter: 0,
      classifications: [{
        isOptional: false,
        title: '',
        value: '',
        items: [],
        attribute: [{
          title: '',
          value: '',
          isOptional: false
        }]
      }],
      classificationLists: [],
      errors: {},
      showModal: false,
      similarPart: []
    }

  },
  mounted() {
    if (this.msg) {
      let part_id = this.getPartId(this.msg)
      this.getPart(part_id)
    }
    this.getClassification()
  },
  methods: {
    getPart(part_id) {
      axios.get(`/api/part-details/${part_id}`)
          .then(res => {
            this.title = res.data.title
            this.description = res.data.description
            this.classifications = []
            res.data.partclassification_set.forEach(obj => {
              let abc = false
              if (obj.is_optional === "True") abc = true
              this.classifications.push({
                isOptional: abc,
                title: obj.classification.title,
                value: obj.classification.id,
                items: [],
                attribute: [],
              });
            })
            let classification_id = 0
            res.data.partclassification_set.forEach(obj => {
              obj.partclassificationattribute_set.forEach(item => {
                let dbc = false
                if (item.is_optional === "True") dbc = true
                this.classifications[classification_id].attribute.push({
                  title: item.attribute.title,
                  isOptional: dbc,
                  value: item.attribute.id
                })
                this.classifications[classification_id].items.push({
                  title: item.attribute.title,
                  id: item.attribute.id
                })
              })
              classification_id += 1
            })
          })
          .catch()

    },
    getPartId(url) {
      let items = url.split('/')
      return items[4]
    },

    addAttribute(classification_id) {
      this.classifications[classification_id].attribute.push({
        title: '',
        value: "",
        isOptional: false
      });
    },
    removeAttribute(index, at_index) {
      this.classifications[index].attribute.splice(at_index, 1)
    },
    addClassification() {
      this.classifications.push({
        isOptional: false,
        title: '',
        value: '',
        items: [],
        attribute: [{
          title: '',
          value: '',
          isOptional: false
        }],
      });
    },
    removeClassification(index) {
      this.classifications.splice(index, 1)
    },
    getClassification() {
      axios.get('/api/classification')
          .then(res => {
            this.classificationLists = res.data
          })
    },
    getAttribute(event, classification_id) {
      this.classifications[classification_id].title = this.classificationLists[event.target.options.selectedIndex - 1].title
      let id = event.target.value;
      axios.get('/api/attribute/' + id)
          .then(res => {
            this.classifications[classification_id].items = res.data
          })
    },
    selectAttribute(event, classification_id, at_index) {
      this.classifications[classification_id].attribute[at_index].title = this.classifications[classification_id].items[event.target.options.selectedIndex - 1].title
    },
    checkExistance() {
      if (!this.title) {
        Toast.fire({
          'icon': 'error',
          'title': 'title field id required'
        })
        return
      }
      axios.get(`/api/part?title=${this.title}&&exact=true&&pagination=false`)
          .then(res => {
            if (res.data.length > 0) {
              this.similarPart = res.data
              this.showModal = true
            } else {
              if (this.msg) {
                this.updatePart(this.getPartId(this.msg))
              } else {
                this.savePart()
              }
            }
          })
          .catch(e => {

          })

    },
    updatePart() {
      let part_id = this.getPartId(this.msg)
      let data = {}
      data['title'] = this.title
      data['description'] = this.description
      data['classifications'] = this.classifications
      axios.put(`/api/part-update/${part_id}/`, data)
          .then(res => {
            Toast.fire({
              icon: "success",
              title: "data updated successfully"
            })
          })
          .catch(err => {
            console.log(err.message)
          })
    },
    savePart() {
      let data = {}
      data['title'] = this.title
      data['description'] = this.description
      data['classifications'] = this.classifications
      axios.post('/api/part/', data)
          .then(res => {
            this.reset()
            this.errors = {}
            this.showModal = false
            Toast.fire({
              icon: "success",
              title: "data store successfully"
            })
          })
          .catch((errors) => {
            this.errors = errors.response.data
            this.showModal = false
          })
    },

    reset() {
      this.title = ''
      this.description = ''
      this.counter = 0
      this.classifications = [{
        isOptional: false,
        value: '',
        items: [],
        attribute: [{
          title: '',
          value: '',
          isOptional: false
        }]
      }]
    }

  }

}
</script>

<style>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, .5);
  display: table;
  transition: opacity .3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}
</style>