from django.db import models


class Broker(models.Model):
	name = models.CharField(max_length=200)
	license = models.CharField(max_length=200)

	def __str__(self):
		return self.name


class Property(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField()
	price = models.CharField(max_length=30)
	address = models.CharField(max_length=70)
	broker = models.ForeignKey(Broker, related_name='properties', on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.name


	class Meta:
		verbose_name_plural = 'Properties'