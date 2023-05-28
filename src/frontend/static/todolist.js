new Vue({
    el: '#app',
    data: {
        tasks: [],
        formData: {
            task: '',
            detail: '',
            deadline: ''
        }
    },
    methods: {
        getalltask: function () {
            fetch('http://127.0.0.1:5001/')
                .then(response => response.json())
                .then(data => this.tasks = data)
        },
        addTask: function () {
            fetch('http://127.0.0.1:5001/add_task', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    this.getalltask()
                })
        },
        delTask: function (task_id) {
            fetch('http://127.0.0.1:5001/delete_task/' + task_id, {
                method: 'DELETE'
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    this.getalltask()
                })
        }
    },
    mounted() {
        this.getalltask()
    }
})