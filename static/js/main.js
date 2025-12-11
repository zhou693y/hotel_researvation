// 通用JavaScript函数

// 格式化日期
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN');
}

// 格式化金额
function formatMoney(amount) {
    return '¥' + parseFloat(amount).toFixed(2);
}

// 显示提示消息
function showMessage(message, type = 'info') {
    alert(message);
}

// 确认对话框
function confirmAction(message) {
    return confirm(message);
}

// 点击模态框外部关闭
window.onclick = function (event) {
    const modals = document.getElementsByClassName('modal');
    for (let modal of modals) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    }
}
