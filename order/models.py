from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from product.models import Product
from django.db.models.signals import post_save
from  account.send_email import send_notification


User = get_user_model()

STATUS_CHOICES = (
	('open', 'Открыт'),
	('in_process', 'В обработке'),
	('closed', 'Закрыт')
)


class OrderItem(models.Model):
	order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveSmallIntegerField(default=1)


class Order(models.Model):
	user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
	product = models.ManyToManyField(Product, through=OrderItem)
	total_sum = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES)
	created_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.id} -> {self.user}'

@receiver(post_save, sender=Order)
def order_post_save(sender, instance, *args, **kwargs):
	send_notification(instance.user, instance.id, instance.total_sum)




