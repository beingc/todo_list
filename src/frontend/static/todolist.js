new Vue({
    el: '#app',
    data: {
        tasks: [],
        formData: {
            task:'',
            detail:'',
            deadline:''
        }
    },
    methods: {
        getalltask: function () {
            fetch('http://127.0.0.1:5001/')
                .then(response => response.json())
                .then(data => this.tasks = data)
        },
        addtask: function () {
            const data = { name: this.name, email: this.email }
            fetch('http://127.0.0.1:5001/add_task', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
                .then(response => response.json())
                .then(data => console.log(data))
                .catch(error => console.error(error))
        }
    },
    mounted() {
        this.getalltask()
    }
})