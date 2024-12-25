# notification.py
from.utils.cart import Cart

class Notification:
    def __init__(self):
        self.messages = []  # قائمة لتخزين الرسائل (الإشعارات)

    def update(self, subject):
        """التحديث عند حدوث تغيير في الـ Cart"""
        if isinstance(subject, Cart):
            if subject.notifications:
                for notification in subject.notifications:
                    self.messages.append(notification)
