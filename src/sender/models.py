from django.db import models
from django.utils import timezone

from django.core.validators import MinLengthValidator
# Create your models here.

class Client (models.Model):

    phone_number = models.CharField(
        null=True,
        verbose_name="Телефон",
        max_length=10,
        validators=[MinLengthValidator(10)]
    )

    code = models.CharField(
        max_length=3,
        validators=[MinLengthValidator(3)]

    )

    tag = models.CharField(
        verbose_name="тег",
        max_length=10

    )

    tz = models.CharField(
        default='3',
        null=True,
        max_length=2,
        validators=[MinLengthValidator(1)],
        verbose_name="Часовой пояс")

    def __str__(self):
        return self.phone_number

class Send_out (models.Model):

    start_date_time=models.DateTimeField(
        verbose_name="Время запуска рассылки",
        default=timezone.now
    )

    filter_code = models.CharField(
        max_length=3,
        validators=[MinLengthValidator(3)]

    )
    filter_tag = models.CharField(
        verbose_name="тег",
        max_length=10

    )

    text_msg = models.TextField(
        verbose_name="текст рассылки",
        max_length=5000
    )
    end=models.DateTimeField(
        verbose_name="дата и время завершения рассылки",
    )


    def __str__(self):
        return f"Рассылка #{self.pk}, Дата запуска {self.start_date_time},Завершение: {self.end}"

class MessageInfo (models.Model):
    
    create=models.DateField(
        verbose_name="Дата cоздания",
        auto_now=False,
        auto_now_add=True
    )
    status = models.BooleanField(
        verbose_name="Сообщение доставлено",
        default=False
    )
    mailing_id=models.ForeignKey(
        Send_out,
        on_delete=models.CASCADE,
        related_name='message_mailing'
    )
    client_id=models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="message_client"
    )
    def __str__(self):
        return f"Дата создания {self.create}  Статус доставки: {self.status}"