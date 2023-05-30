new Vue({
    el: '#app',
    data: {
        tasks: [],
        formData: {
            task: '',
            detail: '',
            deadline: ''
        },
        isShowTips: false,
        isShowMore: false,
        keyWord: "",
    },
    methods: {
        getAllTask: function () {
            fetch('http://127.0.0.1:5001/')
                .then(response => response.json())
                .then(data => { this.tasks = data })
        },
        addTask: function () {
            this.isShowTips = false
            if (this.formData.task) {
                fetch('http://127.0.0.1:5001/add_task', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(this.formData)
                })
                    .then(response => response.json())
                    .then(data => {
                        this.getAllTask()
                        this.formData.task = ""
                        this.formData.detail = ""
                        this.formData.deadline = ""
                    })
            } else {
                this.isShowTips = true
            }
        },
        delTask: function (task_id) {
            fetch('http://127.0.0.1:5001/delete_task/' + task_id, {
                method: 'DELETE'
            })
                .then(response => response.json())
                .then(data => {
                    this.getAllTask()
                })
        },
        completeTask: function (task_id) {
            fetch('http://127.0.0.1:5001/complete_task/' + task_id, {
                method: 'POST'
            })
                .then(response => response.json())
                .then(data => {
                    this.getAllTask()
                })
        },
        reDoTask: function (task_id) {
            fetch('http://127.0.0.1:5001/incomplete_task/' + task_id, {
                method: 'POST'
            })
                .then(response => response.json())
                .then(data => {
                    this.getAllTask()
                })
        },
        showMore: function () {
            this.isShowMore = !this.isShowMore
            this.isShowTips = false
        }
    },
    mounted() {
        this.getAllTask()
    },
    computed: {
        filterTasks() {
            return this.tasks.filter((task) => {
                return task.task.indexOf(this.keyWord) !== -1
            })
        }

    }
})