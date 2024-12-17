from django.db import models

from customers.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5,blank=True, null=True)
    """
    серийный номер присваивается при производстве НА ЭКЗЕМПЛЯР и не может быть известен во время заказа.
    Поле оставляю, так как при выпуске робота по этому номеру робот может быть забронирован
    на определенный заказ
    """
    # по нижестоящим полям вполне возможно идентифицировать заказ
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
