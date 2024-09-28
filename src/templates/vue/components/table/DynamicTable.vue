<template>
  <div v-if="showBlur" class="align-items-center d-flex justify-content-center" style="min-height: 25vh"><i
      class="fa-circle-notch fa-spin fas fs-1 text-primary"></i></div>
  <div v-else class="card shadow mb-4">
    <div class="card-header py-3">
      <!--      <slot name="supplier-moderator-actions" :method="saveSelectedReview"></slot>-->
      <div class="row p-0">
        <div class="col-12 d-flex justify-content-between">
          <div class="col-4">
            <h4 class="m-0 font-weight-bold text-primary">{{ this.tableName }}</h4>
          </div>
          <div class="col-4 has-search position-relative">
            <span class="fa fa-search form-control-feedback position-absolute"></span>
            <input placeholder="Search" class="form-control ps-5" @keyup="requestSearch($event)" type="text">
          </div>
        </div>
      </div>

    </div>
    <div class="card-body">
      <div class="table-responsive extra-space">
        <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
          <thead v-if="noDataFound">
          <tr class="text-center">No data found</tr>
          </thead>
          <template v-else>
            <thead>
            <tr>
              <th v-if="selectedReview">
                Selected Review
              </th>
              <th v-for="(item, key) in headers"
                  v-if="item!=='slug' && item!=='id' && item!=='is_deleted' && item!=='review_id' && item!=='reviews'">
                <div class="m-0 p-0 row">
                  <div class="m-0 p-0 col d-flex justify-content-between">
                    <div class="col-8">
                      <label class="text-capitalize mb-0">{{ item.replace("_", " ") }}</label>
                    </div>
                    <div class="col-4">
                      <span @click="sortBy(item, '+', key)"
                            v-if="sort_clicked_items[key] === 0 && item !=='attachments'">
                              <i class="fas fa-sort-amount-up-alt"></i>
                            </span>
                      <span @click="sortBy(item, '+', key)" v-else-if="sort_clicked_items[key] === 1">
                                      <i class="fas fa-sort-amount-up-alt text-warning"></i>
                            </span>
                      <span @click="sortBy(item, '-', key)" v-else-if="sort_clicked_items[key] === 2">
                                       <i class="fas fa-sort-amount-down-alt text-warning"></i>
                            </span>
                    </div>
                  </div>
                </div>
              </th>
              <th v-if="hasActions">
                <div class="ml-4">
                  Actions
                </div>
              </th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(row,index) in results">
              <td v-if="selectedReview">
                <input @click="setReviewId(row.id)" v-model="row.reviews.length > 0 ? true : false" type="checkbox"/>
              </td>
              <td v-for="(item, key) in row"
                  v-if="key!=='slug' && key!=='id' && key!=='is_deleted' && key!=='review_id' && key!=='reviews'"
                  :class="index==0 && key=='title' ? 'w-25' : ''">
                <span v-if="key !== 'attachments'">{{ item }}</span>
                <span v-else>
                  <span v-for="attachment in item">
                    <a v-if="attachment.file" :href="`${attachment.file}`" target="_blank"
                       class="btn btn-primary m-1">Attachment
                      <a v-if="is_attachment_delete"
                         :href="`/request/review_attachment/${attachment.id}/delete`"
                         onclick='return confirm("Are you sure you want to do this?")'
                         class="badge badge-danger times-btn"><i
                          class="fas fa-times"></i></a>
                    </a>
                    <span v-else class="text-danger">Attachments were deleted</span>&nbsp;
                  </span>
                </span>
              </td>
              <td class="colorChange" v-if="hasActions">
                <slot name="actions" :row="row" :review_ids="review_ids" :order_review_ids="orderReviewIds">
                </slot>
              </td>
            </tr>
            </tbody>
          </template>
        </table>
      </div>
    </div>
    <div>
    </div>
    <nav aria-label="Page navigation example" class="pl-3">
      <ul class="pagination">
        <li v-if="this.showPrevButton" class="page-item">
          <button class="page-link" @click="loadPrev">&laquo;
          </button>
        </li>
        <li v-else class="disabled page-item"><span class="page-link">&laquo;</span></li>
        <li v-for="page in totalPage" class="page-item" :class="currentPage===page ? ' active': ''">
          <button v-if="page <= 3" class="page-link"
                  @click="loadPageData(page)">{{ page }}
          </button>
          <button v-else-if="page >= currentPage-1 && page <= currentPage+1" class="page-link"
                  @click="loadPageData(page)">{{ page }}
          </button>
          <span class="disabled page-link" v-else-if="page === 4">...</span>
          <span class="disabled page-link" v-else-if="page === totalPage-4">...</span>
          <button v-else-if="page >totalPage-3" class="page-link"
                  @click="loadPageData(page)">{{ page }}
          </button>
        </li>
        <li v-if="this.showNextButton" class="page-item">
          <button class="page-link" @click="loadNext">&raquo;</button>
        </li>
        <li v-else class="disabled page-item"><span class="page-link">&raquo;</span></li>
      </ul>
    </nav>
  </div>


</template>

<script>
export default {
  name : "DynamicTable",
  props: {
    url                 : {
      default: "/supplier/api/supplier-requests",
    },
    hasActions          : {
      default: false
    },
    hasParam            : {
      default: false
    },
    hasReview           : {
      default: false
    },
    requestId           : {
      default: null
    },
    tableName           : {
      default: "Request List"
    },
    is_attachment_delete: {
      default: false
    },
    selectedReview      : {
      default: false
    },
    hasOrder            : {
      default: false
    }
  },
  data() {
    return {
      tableData          : {},
      results            : [],
      headers            : [],
      search             : "",
      totalPage          : 0,
      sort_clicked_items : [],
      noDataFound        : false,
      review_ids         : [],
      selected_review_ids: [],
      currentPage        : 1,
      showNextButton     : false,
      showPrevButton     : false,
      order_by_item      : '',
      showBlur           : false,
      orderReviewIds     : []

    }
  },
  mounted() {
    this.getData()
    if (this.hasReview) {
      this.getReviewIds()
    }
    if (this.hasOrder) {
      this.getOrderReviewIds()
    }
  },
  methods: {
    async getData() {
      if (this.search) this.currentPage = 1
      let localUrl = this.url
      localUrl += this.hasParam ? `&page=${this.currentPage}&field=${this.search}&order_by=${this.order_by_item}`
                                : `?page=${this.currentPage}&field=${this.search}&order_by=${this.order_by_item}`
      await axios.get(localUrl).then(res => {
        if (Object.keys(res.data.results).length > 0) {
          this.noDataFound    = false
          this.tableData      = res.data
          this.showNextButton = !!res.data.next;
          this.showPrevButton = !!res.data.previous;
          this.results        = res.data.results
          this.headers        = Object.keys(this.results[0])
          this.getPageNumber()
          for (let i = 0; i < this.headers.length; i++) {
            this.sort_clicked_items.push(0)
          }
        } else {
          this.noDataFound = true
        }
      }).catch(err => {
        console.log("error", err.response)
      })
    },
    async getReviewIds() {
      await axios.get(`/api/get-review-ids/${this.requestId}`).then(
          res => {
            this.review_ids = res.data
          }
      ).catch(err => {
        console.log(err.response)
      })
    },
    async getOrderReviewIds() {
      await axios.get(`/api/get-order-ids/${this.requestId}`).then(
          res => {
            this.orderReviewIds = res.data
          }
      ).catch(err => {
        console.log(err)
      })
    },
    loadNext() {
      this.currentPage += 1
      this.getData()
    },
    loadPrev() {
      this.currentPage -= 1
      this.getData()
    },
    loadPageData(num) {
      this.currentPage = num
      this.getData()
    },
    async requestSearch(e) {
      this.search = e.target.value
      await this.getData()
    },
    async sortBy(item, type, key) {
      this.currentPage = 1
      this.sort_clicked_item = item
      if (type === '-') {
        for (let i = 0; i < this.sort_clicked_items.length; i++) {
          if (i === key) {
            this.sort_clicked_items[i] = 1
          } else {
            this.sort_clicked_items[i] = 0
          }
        }
        item = type + item
      } else {
        for (let i = 0; i < this.sort_clicked_items.length; i++) {
          if (i === key) {
            this.sort_clicked_items[i] = 2
          } else {
            this.sort_clicked_items[i] = 0
          }
        }
      }
      this.order_by_item = item
      await this.getData()
    },
    async getPageNumber() {
      this.totalPage = Math.ceil(this.tableData.count / 10)
    },
    setReviewId(reviewId) {
      this.showBlur = true
      let data      = {
        id        : reviewId,
        request_id: this.requestId
      }
      setTimeout(() => {
        axios.post(`/api/selected-review-id/`, data).then(res => {
          this.getData()
          this.showBlur = false
        }).catch(err => {
          console.log(err.response)
          this.showBlur = false
        })
      }, 200)
      /* if (this.selected_review_ids.includes(reviewId)) {
         this.selected_review_ids = this.selected_review_ids.filter(item => {
               return item !== reviewId
             }
         )
       } else {
         this.selected_review_ids.push(reviewId)
       }
       this.getData()*/
      // console.log(this.selected_review_ids)
    },
    // saveSelectedReview() {
    //   let data = {
    //     review_ids: this.selected_review_ids,
    //     request_id: this.requestId
    //   }
    //   axios.post(`/api/selected-review-id/`, data).then(res => {
    //     this.getData()
    //   }).catch(err => {
    //     console.log(err.response)
    //   })
    // }
  },

}
</script>

<style scoped lang="scss">
.has-search > * {

  top: 11px;
  left: 26px;
  color: #868686;

}

.table-responsive.extra-space {
  //padding-bottom: 190px;
  min-height: 30vh;
}


th {
  vertical-align: middle;
}

td {
  vertical-align: middle;
  padding-left: 25px;
}

.colorChange {
  button {
    background: #3497D3;
    border: none;

    &:hover {
      background: #F2B538;
    }
  }

  .btn-secondary:focus, .btn-secondary.focus {
    color: #fff;
    background-color: #f0a814;
    border-color: #e8a10f;
  }

  .dropdown-item:hover, .dropdown-item:focus {
    color: #fff;
    text-decoration: none;
    background-color: #f0a814;
  }

  .dropdown .dropdown-menu {
    left: -71px !important;
  }
}

.times-btn {
  position: relative;
  top: -15px;
  left: 20px;
  padding: 3px 5px;
  border-radius: 50%;
}

</style>