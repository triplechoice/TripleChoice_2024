import Vue   from 'vue'
import './scss/app.scss'
import Swal  from 'sweetalert2'
import store from "./store";
import 'bootstrap';

const Toast  = Swal.mixin({
    toast            : true,
    position         : 'top-end',
    showConfirmButton: false,
    timer            : 3000,
    timerProgressBar : true,
    didOpen          : (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
});
window.Toast = Toast

Vue.config.productionTip                            = false
const csrftoken                                     = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
window.axios                                        = require('axios')
window.axios.defaults.headers.common['X-CSRFToken'] = csrftoken;

import DynamicTable from "./components/table/DynamicTable";

Vue.component('part', require('./components/product/CreatePart').default)
Vue.component('home-page', require('./components/frontend/homepage/Index').default)
Vue.component('main-slider', require('./components/frontend/homepage/mainSlider').default)
Vue.component('customer-part', require('./components/frontend/part/Index').default)
Vue.component('supplier', require('./components/product/Supplier').default)
Vue.component('selected-request-review', require('./components/request_review/Create').default)
// TODO:form wizard
Vue.component('form-wizard', require('./components/wizard/Index').default)
Vue.component('request-order', require('./components/request_order/Create').default)
Vue.component('checkout', require('./components/request_order/CheckOut').default)
Vue.component('order-update', require('./components/request_order/OrderUpdate').default)
Vue.component('dynamic-table', DynamicTable)
Vue.component('request-submit-helper', require('./components/utils/RequestSubmitHelper').default)

new Vue({
    el        : "#app",
    delimiters: ["[[", "]]"],
    store,
})
