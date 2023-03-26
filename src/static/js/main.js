$(document).ready(function() {
$('.task-button-complete, .task-button-delete').click(function() {
var taskid = $(this).data('taskid');
var url = $(this).hasClass('task-button-complete') ? '/complete_task' : '/delete_task';
$.ajax({
url: url,
type: 'POST',
data: {taskid: taskid},
success: function(response) {
// 处理后台返回的数据
window.location.reload();
},
error: function(jqXHR, textStatus, errorThrown) {
// 处理错误
}
});
});
});