new Vue({
    el: '#app',
    data: {
        tasks: []
    },
    mounted() {
        fetch('http://127.0.0.1:5001/')
            .then(response => response.json())
            .then(data => this.tasks = data)
    }
})