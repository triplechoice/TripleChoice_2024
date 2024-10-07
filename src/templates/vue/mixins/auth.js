import {mapGetters} from 'vuex';

export default {
    data() {
        return {
            authData: {}
        }
    },
    computed: {
        ...mapGetters([
            'form', 'parts', 'commentForm', 'contactForm', 'submitForm', 'getIsLoggedIn', 'getIsRegisterClicked'
        ]),
    },
    methods : {
        formData() {
            return {
                "answer"      : this.parts,
                "comment"     : this.commentForm.comment,
                "contact_info": this.contactForm,
                "quantity"    : this.submitForm.quantity,
                "type"        : this.submitForm.type,
                "zip_code"    : this.submitForm.zip_code,
                "part"        : this.parts.id
            }
        },
        async checkAuth() {
            await axios.get('/api/check-auth/')
                .then(res => {
                    this.authData = res.data
                })
                .catch(e => {
                    this.authData.error = {
                        'message': 'authentication fail'
                    }
                })
        },
        async requestSubmitHelper(file=false) {
            let formData = {form_data: JSON.stringify(this.formData())};
            let data = this.jsonToFormData(formData);

            if (file) {
                data.append("file_comment", this.commentForm.file_comment);
            } else {
                data.append("file_comment", "");
            }

            console.log(formData)
            axios({
                method: "post",
                url: '/api/request/',
                data: data,
                headers: { "Content-Type": "multipart/form-data" },
              })
                .then(res => {
                    console.log(res.data);
                    if (res.data.is_logged_in == "previously_logged_in") {
                        Toast.fire({
                            text: "Request submitted successfully",
                            icon: "success",
                        }).then(value => {
                                window.location.href = '/user/requests/?template=request-detaials'
                            }
                        );
                    } else if (res.data.is_logged_in === "user_already_exists") {
                        Toast.fire({
                            text: "Request submitted successfully",
                            icon: "success",
                        }).then(value => {
                                window.location.href = '/'
                            }
                        );
                    } else if (res.data.is_logged_in === 'wrong_password_given') {
                        Toast.fire({
                            text: "User already exists, But wrong password given",
                            icon: "error",
                        })
                    } else {
                        let text = "order submitted please check your  email for account activation"
                        Toast.fire({
                            text: text,
                            icon: "success",
                        }).then(value => {
                                window.location.href = '/'
                            }
                        );
                    }
                })
                .catch(err => {

                    Toast.fire({
                        text: err.response.data[0],
                        icon: "error",
                    });

                })
        },



        buildFormData(formData, data, parentKey) {
            if (data && typeof data === 'object' && !(data instanceof Date) && !(data instanceof File)) {
                Object.keys(data).forEach(key => {
                    this.buildFormData(formData, data[key], parentKey ? `${parentKey}[${key}]` : key);
                });
            } else {
                const value = data == null ? '' : data;

                formData.append(parentKey, value);
            }
        },

        jsonToFormData(data) {
            const formData = new FormData();

            this.buildFormData(formData, data);

            return formData;
        },

    }
}