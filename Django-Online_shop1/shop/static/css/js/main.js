function showNotification(message, type = "success") {
    const container = document.getElementById("notification-container");

    // إنشاء عنصر الإشعار
    const notification = document.createElement("div");
    notification.className = `notification ${type}`;
    notification.innerText = message;

    // إضافة الإشعار إلى الصفحة
    container.appendChild(notification);

    // إزالة الإشعار بعد 5 ثوانٍ
    setTimeout(() => {
        notification.remove();
    }, 5000);
}
