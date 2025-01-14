# from background_task import background
from django.db import models

# Create your models here.
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
# from django.utils.http import urlquote
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.contrib.auth.models import BaseUserManager
from django.conf import settings as django_settings, settings

import uuid


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class State(models.Model):
    name_of_state = models.CharField(max_length=255, blank=False, null=False)
    name_of_briefly = models.IntegerField(default=0)

    def __str__(self):
        return self.name_of_state


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    name_of_city = models.CharField(max_length=255, blank=False, null=False)
    name_of_briefly = models.IntegerField(default=0)

    def __str__(self):
        return self.name_of_city

    @property
    def get_state_name(self):
        try:
            if self.state:
                return State.objects.get(id=int(self.state.pk)).name_of_state
            else:
                return map(lambda c: c.name_of_state, State.objects.all())
        except Exception as e:
            return "Error:%s" % str(e)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # USER_TYPE = (
    #     (1, "کاربر سایت"),
    #     (2, "مدیر آژانس"),
    #     (3, "مشاور"),
    #
    # )
    username = models.CharField(max_length=254, unique=True, null=True)
    phone_number = models.CharField(max_length=17, unique=True, blank=True, null=True)
    # phone_number = models.CharField(max_length=17, unique=True, blank=True, null=True,
    #                                 validators=[r"09(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}"])
    email = models.EmailField(_('email address'), max_length=254, unique=True, blank=True, null=True)
    IMEI = models.CharField(_('IMEI'), max_length=254, unique=True, blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    # user_type = models.IntegerField(default=1, choices=USER_TYPE)
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now, serialize=True)
    # address1 = models.CharField(max_length=254, blank=True, null=True)
    # state = models.ForeignKey(State, on_delete=models.CASCADE, default=1)
    # city = models.ForeignKey(City, on_delete=models.CASCADE, default=1)
    country_code = models.CharField(max_length=5, blank=True)
    is_verified = models.BooleanField('verified', default=False)  # Add the `is_verified` flag
    verification_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)
    picture_profile = models.FileField(upload_to='profile_pictures',
                                       default=django_settings.MEDIA_URL + 'profile_pictures/user.jpg',
                                       null=True, blank=True,
                                       validators=[
                                           FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])])
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        # fields = ['username', 'first_name', 'last_name', 'phone_number', 'email', 'user_token', 'verify_code',
        #           'ip_address', 'reporter']

    #
    def __unicode__(self):
        return self.date_joined

    def __str__(self):
        return "".join(self.first_name if self.first_name else "")

    def get_absolute_url(self):
        pass
        # return "".join("/users/%s/" % urlquote(self.email))

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return "".join(full_name.strip())

    def get_short_name(self):
        return "".join(self.first_name if self.first_name else "None")

    # def get_data_join(self):
    #     return self.date_joined.__str__()
    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    # @background(schedule=60)
    # def notify_user(self, user_id):
    #     # lookup user by id and send them a message
    #
    #     user = CustomUser.objects.get(pk=user_id)
    #     if user:
    #         if self.email:
    #             user.email_user('Here is a notification', 'You have been notified')

    # def save(self, *args, **kwargs):
    #     self.notify_user(self.pk)
    #     super(CustomUser, self).save(args, kwargs)

#
# class AgentsModel(models.Model):
#     COUNT_EMPLOYEES = (
#         (1, "کمتر از ۳ نفر"),
#         (2, "۳ تا ۵ نفر"),
#         (3, "۵ تا ۱۰ نفر"),
#         (4, "بیشتر از ۱۰ نفر"),
#     )
#     agents_admin = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, verbose_name='صاحب آژانس')
#     name_agents = models.CharField(max_length=250, null=True, blank=True, verbose_name='نام آژانس')
#     city_agents = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='شهر حوزه فعالیت')
#     phone_number_agents = models.CharField(max_length=17, unique=True, blank=True, null=True,
#                                            verbose_name='شماره تماس آژانس')
#     address = models.CharField(max_length=255, null=True, blank=True, verbose_name='آدرس')
#     description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
#     count_employees = models.IntegerField(default=1, choices=COUNT_EMPLOYEES, verbose_name='تعداد کارمندان آژانس')
#     agents_picture_profile = models.FileField(upload_to='profile_pictures/agents',
#                                               default=django_settings.MEDIA_URL + 'profile_pictures/user.jpg',
#                                               null=True, blank=True,
#                                               validators=[
#                                                   FileExtensionValidator(
#                                                       allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],
#                                               verbose_name="آواتار آژانس")
#
#     class Meta:
#         db_table = "agents_model"
#
#
# class ConsultantModel(models.Model):
#     city = models.ForeignKey(City, on_delete=models.CASCADE, default=1, verbose_name='شهر حوزه فعالیت')
#
#     class Meta:
#         db_table = "consultant_model"


class LogAccess(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=False, default=0)
    phone_number = models.CharField(max_length=17, unique=True, blank=True)
    group_key = models.IntegerField(default=0)
    user_token = models.CharField(max_length=254, blank=True, null=True)
    verify_code = models.CharField(max_length=254, blank=True, null=True)
    ip_address = models.CharField(max_length=254, blank=True, null=True)
    time_to_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'log_access'


class RegionalInformation(models.Model):
    all_info = """
    [
  {
    "name": "آذربایجان شرقی",
    "Cities": [
      {
        "name": "سهند"
      },
      {
        "name": "سیس"
      },
      {
        "name": "دوزدوزان"
      },
      {
        "name": "تیمورلو"
      },
      {
        "name": "صوفیان"
      },
      {
        "name": "سردرود"
      },
      {
        "name": "هادیشهر"
      },
      {
        "name": "هشترود"
      },
      {
        "name": "زرنق"
      },
      {
        "name": "ترکمانچای"
      },
      {
        "name": "ورزقان"
      },
      {
        "name": "تسوج"
      },
      {
        "name": "زنوز"
      },
      {
        "name": "ایلخچی"
      },
      {
        "name": "شرفخانه"
      },
      {
        "name": "مهربان"
      },
      {
        "name": "مبارک شهر"
      },
      {
        "name": "تیکمه داش"
      },
      {
        "name": "باسمنج"
      },
      {
        "name": "سیه رود"
      },
      {
        "name": "میانه"
      },
      {
        "name": "خمارلو"
      },
      {
        "name": "خواجه"
      },
      {
        "name": "بناب مرند"
      },
      {
        "name": "قره آغاج"
      },
      {
        "name": "وایقان"
      },
      {
        "name": "مراغه"
      },
      {
        "name": "ممقان"
      },
      {
        "name": "خامنه"
      },
      {
        "name": "خسروشاه"
      },
      {
        "name": "لیلان"
      },
      {
        "name": "نظرکهریزی"
      },
      {
        "name": "اهر"
      },
      {
        "name": "بخشایش"
      },
      {
        "name": "آقکند"
      },
      {
        "name": "جوان قلعه"
      },
      {
        "name": "کلیبر"
      },
      {
        "name": "مرند"
      },
      {
        "name": "اسکو"
      },
      {
        "name": "شندآباد"
      },
      {
        "name": "شربیان"
      },
      {
        "name": "گوگان"
      },
      {
        "name": "بستان آباد"
      },
      {
        "name": "تبریز"
      },
      {
        "name": "جلفا"
      },
      {
        "name": "اچاچی"
      },
      {
        "name": "هریس"
      },
      {
        "name": "یامچی"
      },
      {
        "name": "خاروانا"
      },
      {
        "name": "کوزه کنان"
      },
      {
        "name": "خداجو(خراجو)"
      },
      {
        "name": "آذرشهر"
      },
      {
        "name": "شبستر"
      },
      {
        "name": "سراب"
      },
      {
        "name": "ملکان"
      },
      {
        "name": "بناب"
      },
      {
        "name": "هوراند"
      },
      {
        "name": "کلوانق"
      },
      {
        "name": "ترک"
      },
      {
        "name": "عجب شیر"
      },
      {
        "name": "آبش احمد"
      }
    ]
  },
  {
    "name": "آذربایجان غربی",
    "Cities": [
      {
        "name": "نالوس"
      },
      {
        "name": "ایواوغلی"
      },
      {
        "name": "شاهین دژ"
      },
      {
        "name": "گردکشانه"
      },
      {
        "name": "باروق"
      },
      {
        "name": "سیلوانه"
      },
      {
        "name": "بازرگان"
      },
      {
        "name": "نازک علیا"
      },
      {
        "name": "ربط"
      },
      {
        "name": "تکاب"
      },
      {
        "name": "دیزج دیز"
      },
      {
        "name": "سیمینه"
      },
      {
        "name": "نوشین"
      },
      {
        "name": "میاندوآب"
      },
      {
        "name": "مرگنلر"
      },
      {
        "name": "سلماس"
      },
      {
        "name": "آواجیق"
      },
      {
        "name": "قطور"
      },
      {
        "name": "محمودآباد"
      },
      {
        "name": "خوی"
      },
      {
        "name": "نقده"
      },
      {
        "name": "سرو"
      },
      {
        "name": "خلیفان"
      },
      {
        "name": "پلدشت"
      },
      {
        "name": "میرآباد"
      },
      {
        "name": "اشنویه"
      },
      {
        "name": "زرآباد"
      },
      {
        "name": "بوکان"
      },
      {
        "name": "پیرانشهر"
      },
      {
        "name": "چهاربرج"
      },
      {
        "name": "قوشچی"
      },
      {
        "name": "شوط"
      },
      {
        "name": "ماکو"
      },
      {
        "name": "سیه چشمه"
      },
      {
        "name": "سردشت"
      },
      {
        "name": "کشاورز"
      },
      {
        "name": "فیرورق"
      },
      {
        "name": "محمدیار"
      },
      {
        "name": "ارومیه"
      },
      {
        "name": "مهاباد"
      },
      {
        "name": "قره ضیاءالدین"
      }
    ]
  },
  {
    "name": "اردبیل",
    "Cities": [
      {
        "name": "فخراباد"
      },
      {
        "name": "کلور"
      },
      {
        "name": "نیر"
      },
      {
        "name": "اردبیل"
      },
      {
        "name": "اسلام اباد"
      },
      {
        "name": "تازه کندانگوت"
      },
      {
        "name": "مشگین شهر"
      },
      {
        "name": "جعفرآباد"
      },
      {
        "name": "نمین"
      },
      {
        "name": "اصلاندوز"
      },
      {
        "name": "مرادلو"
      },
      {
        "name": "خلخال"
      },
      {
        "name": "کوراییم"
      },
      {
        "name": "هیر"
      },
      {
        "name": "گیوی"
      },
      {
        "name": "گرمی"
      },
      {
        "name": "لاهرود"
      },
      {
        "name": "هشتجین"
      },
      {
        "name": "عنبران"
      },
      {
        "name": "تازه کند"
      },
      {
        "name": "قصابه"
      },
      {
        "name": "رضی"
      },
      {
        "name": "سرعین"
      },
      {
        "name": "بیله سوار"
      },
      {
        "name": "آبی بیگلو"
      }
    ]
  },
  {
    "name": "اصفهان",
    "Cities": [
      {
        "name": "زیار"
      },
      {
        "name": "زرین شهر"
      },
      {
        "name": "گلشن"
      },
      {
        "name": "پیربکران"
      },
      {
        "name": "خالدآباد"
      },
      {
        "name": "سجزی"
      },
      {
        "name": "گوگد"
      },
      {
        "name": "تیران"
      },
      {
        "name": "ونک"
      },
      {
        "name": "دهق"
      },
      {
        "name": "زواره"
      },
      {
        "name": "کاشان"
      },
      {
        "name": "ابوزیدآباد"
      },
      {
        "name": "اصغرآباد"
      },
      {
        "name": "بافران"
      },
      {
        "name": "شهرضا"
      },
      {
        "name": "خور"
      },
      {
        "name": "مجلسی"
      },
      {
        "name": "هرند"
      },
      {
        "name": "فولادشهر"
      },
      {
        "name": "کمشچه"
      },
      {
        "name": "کلیشادوسودرجان"
      },
      {
        "name": "لای بید"
      },
      {
        "name": "قهجاورستان"
      },
      {
        "name": "چرمهین"
      },
      {
        "name": "رزوه"
      },
      {
        "name": "فریدونشهر"
      },
      {
        "name": "طرق رود"
      },
      {
        "name": "نصرآباد"
      },
      {
        "name": "برزک"
      },
      {
        "name": "سفیدشهر"
      },
      {
        "name": "سمیرم"
      },
      {
        "name": "گلدشت"
      },
      {
        "name": "اردستان"
      },
      {
        "name": "جوشقان قالی"
      },
      {
        "name": "بویین ومیاندشت"
      },
      {
        "name": "کرکوند"
      },
      {
        "name": "درچه"
      },
      {
        "name": "انارک"
      },
      {
        "name": "دولت آباد"
      },
      {
        "name": "ایمانشهر"
      },
      {
        "name": "گرگاب"
      },
      {
        "name": "حسن اباد"
      },
      {
        "name": "سده لنجان"
      },
      {
        "name": "حبیب آباد"
      },
      {
        "name": "بهاران شهر"
      },
      {
        "name": "میمه"
      },
      {
        "name": "تودشک"
      },
      {
        "name": "گلشهر"
      },
      {
        "name": "رضوانشهر"
      },
      {
        "name": "داران"
      },
      {
        "name": "علویجه"
      },
      {
        "name": "نیک آباد"
      },
      {
        "name": "مشکات"
      },
      {
        "name": "آران وبیدگل"
      },
      {
        "name": "خوانسار"
      },
      {
        "name": "نجف آباد"
      },
      {
        "name": "منظریه"
      },
      {
        "name": "فرخی"
      },
      {
        "name": "دیزیچه"
      },
      {
        "name": "اژیه"
      },
      {
        "name": "زاینده رود"
      },
      {
        "name": "خورزوق"
      },
      {
        "name": "قهدریجان"
      },
      {
        "name": "شاهین شهر"
      },
      {
        "name": "بهارستان"
      },
      {
        "name": "چمگردان"
      },
      {
        "name": "دهاقان"
      },
      {
        "name": "برف انبار"
      },
      {
        "name": "بادرود"
      },
      {
        "name": "کوهپایه"
      },
      {
        "name": "گلپایگان"
      },
      {
        "name": "عسگران"
      },
      {
        "name": "حنا"
      },
      {
        "name": "کهریزسنگ"
      },
      {
        "name": "مهاباد"
      },
      {
        "name": "کامو و چوگان"
      },
      {
        "name": "افوس"
      },
      {
        "name": "زیباشهر"
      },
      {
        "name": "کوشک"
      },
      {
        "name": "نایین"
      },
      {
        "name": "سین"
      },
      {
        "name": "زازران"
      },
      {
        "name": "مبارکه"
      },
      {
        "name": "ورزنه"
      },
      {
        "name": "ورنامخواست"
      },
      {
        "name": "شاپورآباد"
      },
      {
        "name": "فلاورجان"
      },
      {
        "name": "وزوان"
      },
      {
        "name": "اصفهان"
      },
      {
        "name": "باغ بهادران"
      },
      {
        "name": "چادگان"
      },
      {
        "name": "دامنه"
      },
      {
        "name": "نطنز"
      },
      {
        "name": "محمدآباد"
      },
      {
        "name": "نیاسر"
      },
      {
        "name": "نوش آباد"
      },
      {
        "name": "کمه"
      },
      {
        "name": "جوزدان"
      },
      {
        "name": "قمصر"
      },
      {
        "name": "جندق"
      },
      {
        "name": "طالخونچه"
      },
      {
        "name": "خمینی شهر"
      },
      {
        "name": "باغشاد"
      },
      {
        "name": "دستگرد"
      },
      {
        "name": "ابریشم"
      }
    ]
  },
  {
    "name": "البرز",
    "Cities": [
      {
        "name": "آسارا"
      },
      {
        "name": "کرج"
      },
      {
        "name": "طالقان"
      },
      {
        "name": "شهرجدیدهشتگرد"
      },
      {
        "name": "محمدشهر"
      },
      {
        "name": "مشکین دشت"
      },
      {
        "name": "نظرآباد"
      },
      {
        "name": "هشتگرد"
      },
      {
        "name": "ماهدشت"
      },
      {
        "name": "اشتهارد"
      },
      {
        "name": "کوهسار"
      },
      {
        "name": "گرمدره"
      },
      {
        "name": "تنکمان"
      },
      {
        "name": "گلسار"
      },
      {
        "name": "کمال شهر"
      },
      {
        "name": "فردیس"
      }
    ]
  },
  {
    "name": "ایلام",
    "Cities": [
      {
        "name": "شباب"
      },
      {
        "name": "موسیان"
      },
      {
        "name": "بدره"
      },
      {
        "name": "ایلام"
      },
      {
        "name": "ایوان"
      },
      {
        "name": "مهران"
      },
      {
        "name": "آسمان آباد"
      },
      {
        "name": "پهله"
      },
      {
        "name": "مهر"
      },
      {
        "name": "سراب باغ"
      },
      {
        "name": "بلاوه"
      },
      {
        "name": "میمه"
      },
      {
        "name": "دره شهر"
      },
      {
        "name": "ارکواز"
      },
      {
        "name": "مورموری"
      },
      {
        "name": "توحید"
      },
      {
        "name": "دهلران"
      },
      {
        "name": "لومار"
      },
      {
        "name": "چوار"
      },
      {
        "name": "زرنه"
      },
      {
        "name": "صالح آباد"
      },
      {
        "name": "سرابله"
      },
      {
        "name": "ماژین"
      },
      {
        "name": "دلگشا"
      }
    ]
  },
  {
    "name": "بوشهر",
    "Cities": [
      {
        "name": "برازجان"
      },
      {
        "name": "بندرریگ"
      },
      {
        "name": "اهرم"
      },
      {
        "name": "دوراهک"
      },
      {
        "name": "خورموج"
      },
      {
        "name": "نخل تقی"
      },
      {
        "name": "کلمه"
      },
      {
        "name": "بندردیلم"
      },
      {
        "name": "وحدتیه"
      },
      {
        "name": "بنک"
      },
      {
        "name": "چغادک"
      },
      {
        "name": "بندردیر"
      },
      {
        "name": "کاکی"
      },
      {
        "name": "جم"
      },
      {
        "name": "دالکی"
      },
      {
        "name": "بندرگناوه"
      },
      {
        "name": "آباد"
      },
      {
        "name": "آبدان"
      },
      {
        "name": "خارک"
      },
      {
        "name": "شنبه"
      },
      {
        "name": "بوشکان"
      },
      {
        "name": "انارستان"
      },
      {
        "name": "شبانکاره"
      },
      {
        "name": "سیراف"
      },
      {
        "name": "دلوار"
      },
      {
        "name": "بردستان"
      },
      {
        "name": "بادوله"
      },
      {
        "name": "عسلویه"
      },
      {
        "name": "تنگ ارم"
      },
      {
        "name": "امام حسن"
      },
      {
        "name": "سعد آباد"
      },
      {
        "name": "بندرکنگان"
      },
      {
        "name": "بوشهر"
      },
      {
        "name": "بردخون"
      },
      {
        "name": "آب پخش"
      }
    ]
  },
  {
    "name": "تهران",
    "Cities": [
      {
        "name": "پیشوا"
      },
      {
        "name": "جوادآباد"
      },
      {
        "name": "ارجمند"
      },
      {
        "name": "ری"
      },
      {
        "name": "نصیرشهر"
      },
      {
        "name": "رودهن"
      },
      {
        "name": "اندیشه"
      },
      {
        "name": "نسیم شهر"
      },
      {
        "name": "صباشهر"
      },
      {
        "name": "ملارد"
      },
      {
        "name": "شمشک"
      },
      {
        "name": "پاکدشت"
      },
      {
        "name": "باقرشهر"
      },
      {
        "name": "احمد آباد مستوفی"
      },
      {
        "name": "کیلان"
      },
      {
        "name": "قرچک"
      },
      {
        "name": "فردوسیه"
      },
      {
        "name": "گلستان"
      },
      {
        "name": "ورامین"
      },
      {
        "name": "فیروزکوه"
      },
      {
        "name": "فشم"
      },
      {
        "name": "پرند"
      },
      {
        "name": "آبعلی"
      },
      {
        "name": "چهاردانگه"
      },
      {
        "name": "تهران"
      },
      {
        "name": "بومهن"
      },
      {
        "name": "وحیدیه"
      },
      {
        "name": "صفادشت"
      },
      {
        "name": "لواسان"
      },
      {
        "name": "فرون اباد"
      },
      {
        "name": "کهریزک"
      },
      {
        "name": "رباطکریم"
      },
      {
        "name": "آبسرد"
      },
      {
        "name": "باغستان"
      },
      {
        "name": "صالحیه"
      },
      {
        "name": "شهریار"
      },
      {
        "name": "قدس"
      },
      {
        "name": "تجریش"
      },
      {
        "name": "شریف آباد"
      },
      {
        "name": "حسن آباد"
      },
      {
        "name": "اسلامشهر"
      },
      {
        "name": "دماوند"
      },
      {
        "name": "پردیس"
      }
    ]
  },
  {
    "name": "چهارمحال و بختیاری",
    "Cities": [
      {
        "name": "گوجان"
      },
      {
        "name": "گهرو"
      },
      {
        "name": "سورشجان"
      },
      {
        "name": "سرخون"
      },
      {
        "name": "شهرکرد"
      },
      {
        "name": "منج"
      },
      {
        "name": "بروجن"
      },
      {
        "name": "پردنجان"
      },
      {
        "name": "سامان"
      },
      {
        "name": "فرخ شهر"
      },
      {
        "name": "صمصامی"
      },
      {
        "name": "طاقانک"
      },
      {
        "name": "کاج"
      },
      {
        "name": "نقنه"
      },
      {
        "name": "لردگان"
      },
      {
        "name": "باباحیدر"
      },
      {
        "name": "دستنا"
      },
      {
        "name": "سودجان"
      },
      {
        "name": "بازفت"
      },
      {
        "name": "هفشجان"
      },
      {
        "name": "سردشت"
      },
      {
        "name": "فرادبنه"
      },
      {
        "name": "چلیچه"
      },
      {
        "name": "بن"
      },
      {
        "name": "فارسان"
      },
      {
        "name": "شلمزار"
      },
      {
        "name": "نافچ"
      },
      {
        "name": "دشتک"
      },
      {
        "name": "بلداجی"
      },
      {
        "name": "آلونی"
      },
      {
        "name": "گندمان"
      },
      {
        "name": "جونقان"
      },
      {
        "name": "ناغان"
      },
      {
        "name": "هارونی"
      },
      {
        "name": "چلگرد"
      },
      {
        "name": "کیان"
      },
      {
        "name": "اردل"
      },
      {
        "name": "سفیددشت"
      },
      {
        "name": "مال خلیفه"
      }
    ]
  },
  {
    "name": "خراسان جنوبی",
    "Cities": [
      {
        "name": "شوسف"
      },
      {
        "name": "قاین"
      },
      {
        "name": "عشق آباد"
      },
      {
        "name": "طبس مسینا"
      },
      {
        "name": "ارسک"
      },
      {
        "name": "آیسک"
      },
      {
        "name": "نیمبلوک"
      },
      {
        "name": "دیهوک"
      },
      {
        "name": "سربیشه"
      },
      {
        "name": "محمدشهر"
      },
      {
        "name": "بیرجند"
      },
      {
        "name": "فردوس"
      },
      {
        "name": "نهبندان"
      },
      {
        "name": "اسفدن"
      },
      {
        "name": "گزیک"
      },
      {
        "name": "حاجی آباد"
      },
      {
        "name": "سه قلعه"
      },
      {
        "name": "آرین شهر"
      },
      {
        "name": "مود"
      },
      {
        "name": "خوسف"
      },
      {
        "name": "قهستان"
      },
      {
        "name": "بشرویه"
      },
      {
        "name": "سرایان"
      },
      {
        "name": "خضری دشت بیاض"
      },
      {
        "name": "طبس"
      },
      {
        "name": "اسدیه"
      },
      {
        "name": "زهان"
      }
    ]
  },
  {
    "name": "خراسان رضوی",
    "Cities": [
      {
        "name": "نیل شهر"
      },
      {
        "name": "جنگل"
      },
      {
        "name": "درود"
      },
      {
        "name": "رباط سنگ"
      },
      {
        "name": "سلطان آباد"
      },
      {
        "name": "فریمان"
      },
      {
        "name": "گناباد"
      },
      {
        "name": "کاریز"
      },
      {
        "name": "همت آباد"
      },
      {
        "name": "سلامی"
      },
      {
        "name": "باجگیران"
      },
      {
        "name": "بجستان"
      },
      {
        "name": "چناران"
      },
      {
        "name": "درگز"
      },
      {
        "name": "کلات"
      },
      {
        "name": "چکنه"
      },
      {
        "name": "نصرآباد"
      },
      {
        "name": "بردسکن"
      },
      {
        "name": "مشهد"
      },
      {
        "name": "کدکن"
      },
      {
        "name": "نقاب"
      },
      {
        "name": "قلندرآباد"
      },
      {
        "name": "کاشمر"
      },
      {
        "name": "شاندیز"
      },
      {
        "name": "نشتیفان"
      },
      {
        "name": "ششتمد"
      },
      {
        "name": "شادمهر"
      },
      {
        "name": "عشق آباد"
      },
      {
        "name": "چاپشلو"
      },
      {
        "name": "رشتخوار"
      },
      {
        "name": "قدمگاه"
      },
      {
        "name": "صالح آباد"
      },
      {
        "name": "داورزن"
      },
      {
        "name": "فرهادگرد"
      },
      {
        "name": "کاخک"
      },
      {
        "name": "مشهدریزه"
      },
      {
        "name": "جغتای"
      },
      {
        "name": "مزدآوند"
      },
      {
        "name": "قوچان"
      },
      {
        "name": "یونسی"
      },
      {
        "name": "سنگان"
      },
      {
        "name": "نوخندان"
      },
      {
        "name": "کندر"
      },
      {
        "name": "نیشابور"
      },
      {
        "name": "احمدابادصولت"
      },
      {
        "name": "شهراباد"
      },
      {
        "name": "رضویه"
      },
      {
        "name": "تربت حیدریه"
      },
      {
        "name": "باخرز"
      },
      {
        "name": "سفیدسنگ"
      },
      {
        "name": "بیدخت"
      },
      {
        "name": "تایباد"
      },
      {
        "name": "فیروزه"
      },
      {
        "name": "قاسم آباد"
      },
      {
        "name": "سبزوار"
      },
      {
        "name": "فیض آباد"
      },
      {
        "name": "گلمکان"
      },
      {
        "name": "لطف آباد"
      },
      {
        "name": "شهرزو"
      },
      {
        "name": "خرو"
      },
      {
        "name": "تربت جام"
      },
      {
        "name": "انابد"
      },
      {
        "name": "ملک آباد"
      },
      {
        "name": "بایک"
      },
      {
        "name": "دولت آباد"
      },
      {
        "name": "سرخس"
      },
      {
        "name": "ریوش"
      },
      {
        "name": "طرقبه"
      },
      {
        "name": "خواف"
      },
      {
        "name": "روداب"
      },
      {
        "name": "خلیل آباد"
      }
    ]
  },
  {
    "name": "خراسان شمالی",
    "Cities": [
      {
        "name": "راز"
      },
      {
        "name": "پیش قلعه"
      },
      {
        "name": "قوشخانه"
      },
      {
        "name": "شوقان"
      },
      {
        "name": "اسفراین"
      },
      {
        "name": "گرمه"
      },
      {
        "name": "قاضی"
      },
      {
        "name": "شیروان"
      },
      {
        "name": "حصارگرمخان"
      },
      {
        "name": "آشخانه"
      },
      {
        "name": "تیتکانلو"
      },
      {
        "name": "جاجرم"
      },
      {
        "name": "بجنورد"
      },
      {
        "name": "درق"
      },
      {
        "name": "آوا"
      },
      {
        "name": "زیارت"
      },
      {
        "name": "سنخواست"
      },
      {
        "name": "صفی آباد"
      },
      {
        "name": "ایور"
      },
      {
        "name": "فاروج"
      },
      {
        "name": "لوجلی"
      }
    ]
  },
  {
    "name": "خوزستان",
    "Cities": [
      {
        "name": "بیدروبه"
      },
      {
        "name": "شاوور"
      },
      {
        "name": "حمزه"
      },
      {
        "name": "گتوند"
      },
      {
        "name": "شرافت"
      },
      {
        "name": "منصوریه"
      },
      {
        "name": "زهره"
      },
      {
        "name": "رامهرمز"
      },
      {
        "name": "بندرامام خمینی"
      },
      {
        "name": "کوت عبداله"
      },
      {
        "name": "میداود"
      },
      {
        "name": "چغامیش"
      },
      {
        "name": "ملاثانی"
      },
      {
        "name": "چم گلک"
      },
      {
        "name": "حر"
      },
      {
        "name": "شمس آباد"
      },
      {
        "name": "آبژدان"
      },
      {
        "name": "چویبده"
      },
      {
        "name": "مسجدسلیمان"
      },
      {
        "name": "مقاومت"
      },
      {
        "name": "ترکالکی"
      },
      {
        "name": "دارخوین"
      },
      {
        "name": "سردشت"
      },
      {
        "name": "لالی"
      },
      {
        "name": "کوت سیدنعیم"
      },
      {
        "name": "حمیدیه"
      },
      {
        "name": "دهدز"
      },
      {
        "name": "قلعه تل"
      },
      {
        "name": "میانرود"
      },
      {
        "name": "رفیع"
      },
      {
        "name": "اندیمشک"
      },
      {
        "name": "الوان"
      },
      {
        "name": "سالند"
      },
      {
        "name": "صالح شهر"
      },
      {
        "name": "اروندکنار"
      },
      {
        "name": "سرداران"
      },
      {
        "name": "تشان"
      },
      {
        "name": "رامشیر"
      },
      {
        "name": "شادگان"
      },
      {
        "name": "بندرماهشهر"
      },
      {
        "name": "جایزان"
      },
      {
        "name": "بستان"
      },
      {
        "name": "ویس"
      },
      {
        "name": "اهواز"
      },
      {
        "name": "فتح المبین"
      },
      {
        "name": "شهر امام"
      },
      {
        "name": "قلعه خواجه"
      },
      {
        "name": "حسینیه"
      },
      {
        "name": "گلگیر"
      },
      {
        "name": "مینوشهر"
      },
      {
        "name": "سماله"
      },
      {
        "name": "شوشتر"
      },
      {
        "name": "بهبهان"
      },
      {
        "name": "هندیجان"
      },
      {
        "name": "ابوحمیظه"
      },
      {
        "name": "آغاجاری"
      },
      {
        "name": "ایذه"
      },
      {
        "name": "صیدون"
      },
      {
        "name": "سیاه منصور"
      },
      {
        "name": "هویزه"
      },
      {
        "name": "آزادی"
      },
      {
        "name": "شوش"
      },
      {
        "name": "دزفول"
      },
      {
        "name": "جنت مکان"
      },
      {
        "name": "آبادان"
      },
      {
        "name": "گوریه"
      },
      {
        "name": "خرمشهر"
      },
      {
        "name": "مشراگه"
      },
      {
        "name": "خنافره"
      },
      {
        "name": "چمران"
      },
      {
        "name": "امیدیه"
      },
      {
        "name": "سوسنگرد"
      },
      {
        "name": "شیبان"
      },
      {
        "name": "الهایی"
      },
      {
        "name": "باغ ملک"
      },
      {
        "name": "صفی آباد"
      }
    ]
  },
  {
    "name": "زنجان",
    "Cities": [
      {
        "name": "زرین رود"
      },
      {
        "name": "آب بر"
      },
      {
        "name": "ارمغانخانه"
      },
      {
        "name": "کرسف"
      },
      {
        "name": "هیدج"
      },
      {
        "name": "سلطانیه"
      },
      {
        "name": "خرمدره"
      },
      {
        "name": "نیک پی"
      },
      {
        "name": "قیدار"
      },
      {
        "name": "ابهر"
      },
      {
        "name": "دندی"
      },
      {
        "name": "حلب"
      },
      {
        "name": "نوربهار"
      },
      {
        "name": "گرماب"
      },
      {
        "name": "چورزق"
      },
      {
        "name": "زنجان"
      },
      {
        "name": "سهرورد"
      },
      {
        "name": "صایین قلعه"
      },
      {
        "name": "ماه نشان"
      },
      {
        "name": "زرین آباد"
      }
    ]
  },
  {
    "name": "سمنان",
    "Cities": [
      {
        "name": "مجن"
      },
      {
        "name": "دامغان"
      },
      {
        "name": "سرخه"
      },
      {
        "name": "مهدی شهر"
      },
      {
        "name": "شاهرود"
      },
      {
        "name": "سمنان"
      },
      {
        "name": "کهن آباد"
      },
      {
        "name": "گرمسار"
      },
      {
        "name": "کلاته خیج"
      },
      {
        "name": "دیباج"
      },
      {
        "name": "درجزین"
      },
      {
        "name": "رودیان"
      },
      {
        "name": "بسطام"
      },
      {
        "name": "امیریه"
      },
      {
        "name": "میامی"
      },
      {
        "name": "شهمیرزاد"
      },
      {
        "name": "بیارجمند"
      },
      {
        "name": "کلاته"
      },
      {
        "name": "آرادان"
      }
    ]
  },
  {
    "name": "سیستان و بلوچستان",
    "Cities": [
      {
        "name": "شهرک علی اکبر"
      },
      {
        "name": "بنجار"
      },
      {
        "name": "گلمورتی"
      },
      {
        "name": "نگور"
      },
      {
        "name": "راسک"
      },
      {
        "name": "بنت"
      },
      {
        "name": "قصرقند"
      },
      {
        "name": "جالق"
      },
      {
        "name": "هیدوچ"
      },
      {
        "name": "نوک آباد"
      },
      {
        "name": "زهک"
      },
      {
        "name": "بمپور"
      },
      {
        "name": "پیشین"
      },
      {
        "name": "گشت"
      },
      {
        "name": "محمدآباد"
      },
      {
        "name": "زاهدان"
      },
      {
        "name": "زابلی"
      },
      {
        "name": "چاه بهار"
      },
      {
        "name": "زرآباد"
      },
      {
        "name": "بزمان"
      },
      {
        "name": "اسپکه"
      },
      {
        "name": "فنوج"
      },
      {
        "name": "سراوان"
      },
      {
        "name": "ادیمی"
      },
      {
        "name": "زابل"
      },
      {
        "name": "دوست محمد"
      },
      {
        "name": "ایرانشهر"
      },
      {
        "name": "سرباز"
      },
      {
        "name": "سیرکان"
      },
      {
        "name": "میرجاوه"
      },
      {
        "name": "نصرت آباد"
      },
      {
        "name": "سوران"
      },
      {
        "name": "خاش"
      },
      {
        "name": "کنارک"
      },
      {
        "name": "محمدان"
      },
      {
        "name": "نیک شهر"
      }
    ]
  },
  {
    "name": "فارس",
    "Cities": [
      {
        "name": "کارزین (فتح آباد)"
      },
      {
        "name": "فدامی"
      },
      {
        "name": "خومه زار"
      },
      {
        "name": "سلطان شهر"
      },
      {
        "name": "فیروزآباد"
      },
      {
        "name": "دبیران"
      },
      {
        "name": "باب انار"
      },
      {
        "name": "رامجرد"
      },
      {
        "name": "سروستان"
      },
      {
        "name": "قره بلاغ"
      },
      {
        "name": "ارسنجان"
      },
      {
        "name": "دژکرد"
      },
      {
        "name": "بیرم"
      },
      {
        "name": "دهرم"
      },
      {
        "name": "شیراز"
      },
      {
        "name": "ایزدخواست"
      },
      {
        "name": "علامرودشت"
      },
      {
        "name": "اوز"
      },
      {
        "name": "وراوی"
      },
      {
        "name": "بیضا"
      },
      {
        "name": "نی ریز"
      },
      {
        "name": "کنارتخته"
      },
      {
        "name": "امام شهر"
      },
      {
        "name": "جهرم"
      },
      {
        "name": "بابامنیر"
      },
      {
        "name": "گراش"
      },
      {
        "name": "فسا"
      },
      {
        "name": "شهرپیر"
      },
      {
        "name": "حسن اباد"
      },
      {
        "name": "کامفیروز"
      },
      {
        "name": "خنج"
      },
      {
        "name": "خانه زنیان"
      },
      {
        "name": "استهبان"
      },
      {
        "name": "بوانات"
      },
      {
        "name": "لطیفی"
      },
      {
        "name": "فراشبند"
      },
      {
        "name": "زرقان"
      },
      {
        "name": "صغاد"
      },
      {
        "name": "اشکنان"
      },
      {
        "name": "قایمیه"
      },
      {
        "name": "گله دار"
      },
      {
        "name": "دوبرجی"
      },
      {
        "name": "آباده طشک"
      },
      {
        "name": "خرامه"
      },
      {
        "name": "میمند"
      },
      {
        "name": "افزر"
      },
      {
        "name": "دوزه"
      },
      {
        "name": "سیدان"
      },
      {
        "name": "کوپن"
      },
      {
        "name": "زاهدشهر"
      },
      {
        "name": "قادراباد"
      },
      {
        "name": "سده"
      },
      {
        "name": "بنارویه"
      },
      {
        "name": "سعادت شهر"
      },
      {
        "name": "شهرصدرا"
      },
      {
        "name": "سورمق"
      },
      {
        "name": "حسامی"
      },
      {
        "name": "جویم"
      },
      {
        "name": "خوزی"
      },
      {
        "name": "اردکان"
      },
      {
        "name": "قطرویه"
      },
      {
        "name": "نودان"
      },
      {
        "name": "مبارک آباددیز"
      },
      {
        "name": "داراب"
      },
      {
        "name": "نورآباد"
      },
      {
        "name": "کوار"
      },
      {
        "name": "نوبندگان"
      },
      {
        "name": "حاجی آباد"
      },
      {
        "name": "خاوران"
      },
      {
        "name": "مرودشت"
      },
      {
        "name": "کوهنجان"
      },
      {
        "name": "ششده"
      },
      {
        "name": "مزایجان"
      },
      {
        "name": "ایج"
      },
      {
        "name": "خور"
      },
      {
        "name": "نوجین"
      },
      {
        "name": "لپویی"
      },
      {
        "name": "بهمن"
      },
      {
        "name": "اهل"
      },
      {
        "name": "خشت"
      },
      {
        "name": "مهر"
      },
      {
        "name": "جنت شهر"
      },
      {
        "name": "مشکان"
      },
      {
        "name": "بالاده"
      },
      {
        "name": "قیر"
      },
      {
        "name": "قطب آباد"
      },
      {
        "name": "خانیمن"
      },
      {
        "name": "مصیری"
      },
      {
        "name": "میانشهر"
      },
      {
        "name": "صفاشهر"
      },
      {
        "name": "اقلید"
      },
      {
        "name": "عمادده"
      },
      {
        "name": "مادرسلیمان"
      },
      {
        "name": "داریان"
      },
      {
        "name": "رونیز"
      },
      {
        "name": "کره ای"
      },
      {
        "name": "لار"
      },
      {
        "name": "اسیر"
      },
      {
        "name": "هماشهر"
      },
      {
        "name": "آباده"
      },
      {
        "name": "لامرد"
      }
    ]
  },
  {
    "name": "قزوین",
    "Cities": [
      {
        "name": "بیدستان"
      },
      {
        "name": "کوهین"
      },
      {
        "name": "رازمیان"
      },
      {
        "name": "خرمدشت"
      },
      {
        "name": "آبگرم"
      },
      {
        "name": "شال"
      },
      {
        "name": "شریفیه"
      },
      {
        "name": "اقبالیه"
      },
      {
        "name": "نرجه"
      },
      {
        "name": "ارداق"
      },
      {
        "name": "الوند"
      },
      {
        "name": "خاکعلی"
      },
      {
        "name": "سیردان"
      },
      {
        "name": "ضیاڈآباد"
      },
      {
        "name": "بویین زهرا"
      },
      {
        "name": "محمدیه"
      },
      {
        "name": "محمودآبادنمونه"
      },
      {
        "name": "معلم کلایه"
      },
      {
        "name": "اسفرورین"
      },
      {
        "name": "آوج"
      },
      {
        "name": "دانسفهان"
      },
      {
        "name": "آبیک"
      },
      {
        "name": "قزوین"
      },
      {
        "name": "تاکستان"
      }
    ]
  },
  {
    "name": "قم",
    "Cities": [
      {
        "name": "قم"
      },
      {
        "name": "سلفچگان"
      },
      {
        "name": "جعفریه"
      },
      {
        "name": "قنوات"
      },
      {
        "name": "دستجرد"
      }
    ]
  },
  {
    "name": "کردستان",
    "Cities": [
      {
        "name": "توپ آغاج"
      },
      {
        "name": "سروآباد"
      },
      {
        "name": "بویین سفلی"
      },
      {
        "name": "زرینه"
      },
      {
        "name": "دلبران"
      },
      {
        "name": "سنندج"
      },
      {
        "name": "یاسوکند"
      },
      {
        "name": "موچش"
      },
      {
        "name": "بانه"
      },
      {
        "name": "مریوان"
      },
      {
        "name": "سریش آباد"
      },
      {
        "name": "صاحب"
      },
      {
        "name": "دهگلان"
      },
      {
        "name": "بابارشانی"
      },
      {
        "name": "دیواندره"
      },
      {
        "name": "برده رشه"
      },
      {
        "name": "شویشه"
      },
      {
        "name": "بیجار"
      },
      {
        "name": "اورامان تخت"
      },
      {
        "name": "کانی سور"
      },
      {
        "name": "کانی دینار"
      },
      {
        "name": "دزج"
      },
      {
        "name": "سقز"
      },
      {
        "name": "بلبان آباد"
      },
      {
        "name": "پیرتاج"
      },
      {
        "name": "کامیاران"
      },
      {
        "name": "آرمرده"
      },
      {
        "name": "چناره"
      }
    ]
  },
  {
    "name": "کرمان",
    "Cities": [
      {
        "name": "بلوک"
      },
      {
        "name": "پاریز"
      },
      {
        "name": "گنبکی"
      },
      {
        "name": "زنگی آباد"
      },
      {
        "name": "بم"
      },
      {
        "name": "خانوک"
      },
      {
        "name": "کیانشهر"
      },
      {
        "name": "جوپار"
      },
      {
        "name": "عنبرآباد"
      },
      {
        "name": "جوزم"
      },
      {
        "name": "نظام شهر"
      },
      {
        "name": "لاله زار"
      },
      {
        "name": "کشکوییه"
      },
      {
        "name": "زیدآباد"
      },
      {
        "name": "هنزا"
      },
      {
        "name": "چترود"
      },
      {
        "name": "جبالبارز"
      },
      {
        "name": "سیرجان"
      },
      {
        "name": "رودبار"
      },
      {
        "name": "کرمان"
      },
      {
        "name": "بافت"
      },
      {
        "name": "صفاییه"
      },
      {
        "name": "منوجان"
      },
      {
        "name": "اندوهجرد"
      },
      {
        "name": "هجدک"
      },
      {
        "name": "خورسند"
      },
      {
        "name": "امین شهر"
      },
      {
        "name": "بردسیر"
      },
      {
        "name": "رفسنجان"
      },
      {
        "name": "هماشهر"
      },
      {
        "name": "محمدآباد"
      },
      {
        "name": "اختیارآباد"
      },
      {
        "name": "بروات"
      },
      {
        "name": "ریحان"
      },
      {
        "name": "کوهبنان"
      },
      {
        "name": "ماهان"
      },
      {
        "name": "دوساری"
      },
      {
        "name": "دهج"
      },
      {
        "name": "فاریاب"
      },
      {
        "name": "گلزار"
      },
      {
        "name": "بهرمان"
      },
      {
        "name": "بلورد"
      },
      {
        "name": "فهرج"
      },
      {
        "name": "کاظم آباد"
      },
      {
        "name": "جیرفت"
      },
      {
        "name": "نجف شهر"
      },
      {
        "name": "قلعه گنج"
      },
      {
        "name": "باغین"
      },
      {
        "name": "بزنجان"
      },
      {
        "name": "زرند"
      },
      {
        "name": "نودژ"
      },
      {
        "name": "گلباف"
      },
      {
        "name": "راور"
      },
      {
        "name": "خاتون اباد"
      },
      {
        "name": "نرماشیر"
      },
      {
        "name": "دشتکار"
      },
      {
        "name": "مس سرچشمه"
      },
      {
        "name": "خواجو شهر"
      },
      {
        "name": "رابر"
      },
      {
        "name": "راین"
      },
      {
        "name": "درب بهشت"
      },
      {
        "name": "یزدان شهر"
      },
      {
        "name": "زهکلوت"
      },
      {
        "name": "محی آباد"
      },
      {
        "name": "مردهک"
      },
      {
        "name": "شهداد"
      },
      {
        "name": "ارزوییه"
      },
      {
        "name": "نگار"
      },
      {
        "name": "شهربابک"
      },
      {
        "name": "انار"
      }
    ]
  },
  {
    "name": "کرمانشاه",
    "Cities": [
      {
        "name": "شاهو"
      },
      {
        "name": "بانوره"
      },
      {
        "name": "تازه آباد"
      },
      {
        "name": "هلشی"
      },
      {
        "name": "جوانرود"
      },
      {
        "name": "قصرشیرین"
      },
      {
        "name": "نوسود"
      },
      {
        "name": "کرند"
      },
      {
        "name": "کوزران"
      },
      {
        "name": "بیستون"
      },
      {
        "name": "حمیل"
      },
      {
        "name": "گیلانغرب"
      },
      {
        "name": "سطر"
      },
      {
        "name": "روانسر"
      },
      {
        "name": "پاوه"
      },
      {
        "name": "ازگله"
      },
      {
        "name": "کرمانشاه"
      },
      {
        "name": "میان راهان"
      },
      {
        "name": "کنگاور"
      },
      {
        "name": "سرپل ذهاب"
      },
      {
        "name": "ریجاب"
      },
      {
        "name": "باینگان"
      },
      {
        "name": "هرسین"
      },
      {
        "name": "اسلام آبادغرب"
      },
      {
        "name": "سرمست"
      },
      {
        "name": "سومار"
      },
      {
        "name": "نودشه"
      },
      {
        "name": "گهواره"
      },
      {
        "name": "رباط"
      },
      {
        "name": "صحنه"
      },
      {
        "name": "گودین"
      }
    ]
  },
  {
    "name": "کهگیلویه وبویراحمد",
    "Cities": [
      {
        "name": "لنده"
      },
      {
        "name": "سی سخت"
      },
      {
        "name": "دهدشت"
      },
      {
        "name": "یاسوج"
      },
      {
        "name": "سرفاریاب"
      },
      {
        "name": "دوگنبدان"
      },
      {
        "name": "چیتاب"
      },
      {
        "name": "لیکک"
      },
      {
        "name": "دیشموک"
      },
      {
        "name": "مادوان"
      },
      {
        "name": "باشت"
      },
      {
        "name": "پاتاوه"
      },
      {
        "name": "قلعه رییسی"
      },
      {
        "name": "مارگون"
      },
      {
        "name": "چرام"
      },
      {
        "name": "سوق"
      }
    ]
  },
  {
    "name": "گلستان",
    "Cities": [
      {
        "name": "مزرعه"
      },
      {
        "name": "رامیان"
      },
      {
        "name": "فراغی"
      },
      {
        "name": "گنبدکاووس"
      },
      {
        "name": "کردکوی"
      },
      {
        "name": "مراوه"
      },
      {
        "name": "بندرترکمن"
      },
      {
        "name": "نگین شهر"
      },
      {
        "name": "آق قلا"
      },
      {
        "name": "سرخنکلاته"
      },
      {
        "name": "گالیکش"
      },
      {
        "name": "سنگدوین"
      },
      {
        "name": "دلند"
      },
      {
        "name": "بندرگز"
      },
      {
        "name": "نوده خاندوز"
      },
      {
        "name": "مینودشت"
      },
      {
        "name": "گرگان"
      },
      {
        "name": "گمیش تپه"
      },
      {
        "name": "علی اباد"
      },
      {
        "name": "خان ببین"
      },
      {
        "name": "کلاله"
      },
      {
        "name": "اینچه برون"
      },
      {
        "name": "فاضل آباد"
      },
      {
        "name": "تاتارعلیا"
      },
      {
        "name": "نوکنده"
      },
      {
        "name": "آزادشهر"
      },
      {
        "name": "انبارآلوم"
      },
      {
        "name": "جلین"
      }
    ]
  },
  {
    "name": "گیلان",
    "Cities": [
      {
        "name": "شلمان"
      },
      {
        "name": "خشکبیجار"
      },
      {
        "name": "ماکلوان"
      },
      {
        "name": "سنگر"
      },
      {
        "name": "مرجقل"
      },
      {
        "name": "لیسار"
      },
      {
        "name": "رضوانشهر"
      },
      {
        "name": "رحیم آباد"
      },
      {
        "name": "لوندویل"
      },
      {
        "name": "احمدسرگوراب"
      },
      {
        "name": "لوشان"
      },
      {
        "name": "اطاقور"
      },
      {
        "name": "لشت نشاء"
      },
      {
        "name": "فومن"
      },
      {
        "name": "چوبر"
      },
      {
        "name": "بازار جمعه"
      },
      {
        "name": "کلاچای"
      },
      {
        "name": "بندرانزلی"
      },
      {
        "name": "املش"
      },
      {
        "name": "رستم آباد"
      },
      {
        "name": "لاهیجان"
      },
      {
        "name": "توتکابن"
      },
      {
        "name": "لنگرود"
      },
      {
        "name": "کوچصفهان"
      },
      {
        "name": "صومعه سرا"
      },
      {
        "name": "اسالم"
      },
      {
        "name": "دیلمان"
      },
      {
        "name": "رودسر"
      },
      {
        "name": "کیاشهر"
      },
      {
        "name": "شفت"
      },
      {
        "name": "رودبار"
      },
      {
        "name": "کومله"
      },
      {
        "name": "رشت"
      },
      {
        "name": "ماسوله"
      },
      {
        "name": "خمام"
      },
      {
        "name": "ماسال"
      },
      {
        "name": "واجارگاه"
      },
      {
        "name": "هشتپر (تالش)"
      },
      {
        "name": "پره سر"
      },
      {
        "name": "بره سر"
      },
      {
        "name": "آستارا"
      },
      {
        "name": "رودبنه"
      },
      {
        "name": "جیرنده"
      },
      {
        "name": "چاف و چمخاله"
      },
      {
        "name": "لولمان"
      },
      {
        "name": "گوراب زرمیخ"
      },
      {
        "name": "حویق"
      },
      {
        "name": "سیاهکل"
      },
      {
        "name": "چابکسر"
      },
      {
        "name": "آستانه اشرفیه"
      },
      {
        "name": "رانکوه"
      }
    ]
  },
  {
    "name": "لرستان",
    "Cities": [
      {
        "name": "بیران شهر"
      },
      {
        "name": "ویسیان"
      },
      {
        "name": "شول آباد"
      },
      {
        "name": "پلدختر"
      },
      {
        "name": "کوهدشت"
      },
      {
        "name": "هفت چشمه"
      },
      {
        "name": "بروجرد"
      },
      {
        "name": "الشتر"
      },
      {
        "name": "مومن آباد"
      },
      {
        "name": "دورود"
      },
      {
        "name": "زاغه"
      },
      {
        "name": "چقابل"
      },
      {
        "name": "الیگودرز"
      },
      {
        "name": "معمولان"
      },
      {
        "name": "کوهنانی"
      },
      {
        "name": "نورآباد"
      },
      {
        "name": "سپیددشت"
      },
      {
        "name": "سراب دوره"
      },
      {
        "name": "ازنا"
      },
      {
        "name": "گراب"
      },
      {
        "name": "خرم آباد"
      },
      {
        "name": "اشترینان"
      },
      {
        "name": "فیروزآباد"
      },
      {
        "name": "درب گنبد"
      }
    ]
  },
  {
    "name": "مازندران",
    "Cities": [
      {
        "name": "گلوگاه"
      },
      {
        "name": "پل سفید"
      },
      {
        "name": "دابودشت"
      },
      {
        "name": "چالوس"
      },
      {
        "name": "کیاسر"
      },
      {
        "name": "بهنمیر"
      },
      {
        "name": "تنکابن"
      },
      {
        "name": "کلاردشت"
      },
      {
        "name": "ایزدشهر"
      },
      {
        "name": "گتاب"
      },
      {
        "name": "سلمان شهر"
      },
      {
        "name": "ارطه"
      },
      {
        "name": "امیرکلا"
      },
      {
        "name": "کوهی خیل"
      },
      {
        "name": "پایین هولار"
      },
      {
        "name": "گزنک"
      },
      {
        "name": "محمودآباد"
      },
      {
        "name": "رامسر"
      },
      {
        "name": "نوشهر"
      },
      {
        "name": "خلیل شهر"
      },
      {
        "name": "کیاکلا"
      },
      {
        "name": "نور"
      },
      {
        "name": "مرزیکلا"
      },
      {
        "name": "فریدونکنار"
      },
      {
        "name": "زیرآب"
      },
      {
        "name": "امامزاده عبدالله"
      },
      {
        "name": "هچیرود"
      },
      {
        "name": "فریم"
      },
      {
        "name": "هادی شهر"
      },
      {
        "name": "نشتارود"
      },
      {
        "name": "پول"
      },
      {
        "name": "بهشهر"
      },
      {
        "name": "کلارآباد"
      },
      {
        "name": "بلده"
      },
      {
        "name": "بابل"
      },
      {
        "name": "جویبار"
      },
      {
        "name": "آلاشت"
      },
      {
        "name": "آمل"
      },
      {
        "name": "نکا"
      },
      {
        "name": "کتالم وسادات شهر"
      },
      {
        "name": "بابلسر"
      },
      {
        "name": "شیرود"
      },
      {
        "name": "شیرگاه"
      },
      {
        "name": "رویان"
      },
      {
        "name": "زرگرمحله"
      },
      {
        "name": "عباس اباد"
      },
      {
        "name": "قایم شهر"
      },
      {
        "name": "خوش رودپی"
      },
      {
        "name": "مرزن آباد"
      },
      {
        "name": "ساری"
      },
      {
        "name": "رینه"
      },
      {
        "name": "سرخرود"
      },
      {
        "name": "خرم آباد"
      },
      {
        "name": "کجور"
      },
      {
        "name": "رستمکلا"
      },
      {
        "name": "سورک"
      },
      {
        "name": "چمستان"
      }
    ]
  },
  {
    "name": "مرکزی",
    "Cities": [
      {
        "name": "خنجین"
      },
      {
        "name": "نراق"
      },
      {
        "name": "کمیجان"
      },
      {
        "name": "آشتیان"
      },
      {
        "name": "رازقان"
      },
      {
        "name": "مهاجران"
      },
      {
        "name": "غرق آباد"
      },
      {
        "name": "خنداب"
      },
      {
        "name": "قورچی باشی"
      },
      {
        "name": "خشکرود"
      },
      {
        "name": "ساروق"
      },
      {
        "name": "محلات"
      },
      {
        "name": "شازند"
      },
      {
        "name": "ساوه"
      },
      {
        "name": "میلاجرد"
      },
      {
        "name": "تفرش"
      },
      {
        "name": "زاویه"
      },
      {
        "name": "اراک"
      },
      {
        "name": "توره"
      },
      {
        "name": "نوبران"
      },
      {
        "name": "فرمهین"
      },
      {
        "name": "دلیجان"
      },
      {
        "name": "پرندک"
      },
      {
        "name": "کارچان"
      },
      {
        "name": "نیمور"
      },
      {
        "name": "هندودر"
      },
      {
        "name": "آوه"
      },
      {
        "name": "جاورسیان"
      },
      {
        "name": "خمین"
      },
      {
        "name": "مامونیه"
      },
      {
        "name": "داودآباد"
      },
      {
        "name": "شهباز"
      }
    ]
  },
  {
    "name": "هرمزگان",
    "Cities": [
      {
        "name": "تیرور"
      },
      {
        "name": "گروک"
      },
      {
        "name": "قشم"
      },
      {
        "name": "کوشکنار"
      },
      {
        "name": "کیش"
      },
      {
        "name": "سرگز"
      },
      {
        "name": "بندرعباس"
      },
      {
        "name": "زیارتعلی"
      },
      {
        "name": "سندرک"
      },
      {
        "name": "کوهستک"
      },
      {
        "name": "لمزان"
      },
      {
        "name": "رویدر"
      },
      {
        "name": "قلعه قاضی"
      },
      {
        "name": "فارغان"
      },
      {
        "name": "ابوموسی"
      },
      {
        "name": "هشتبندی"
      },
      {
        "name": "سردشت"
      },
      {
        "name": "درگهان"
      },
      {
        "name": "پارسیان"
      },
      {
        "name": "کنگ"
      },
      {
        "name": "جناح"
      },
      {
        "name": "تازیان پایین"
      },
      {
        "name": "دهبارز"
      },
      {
        "name": "میناب"
      },
      {
        "name": "سیریک"
      },
      {
        "name": "سوزا"
      },
      {
        "name": "خمیر"
      },
      {
        "name": "چارک"
      },
      {
        "name": "حاجی اباد"
      },
      {
        "name": "فین"
      },
      {
        "name": "بندرجاسک"
      },
      {
        "name": "گوهران"
      },
      {
        "name": "هرمز"
      },
      {
        "name": "دشتی"
      },
      {
        "name": "بندرلنگه"
      },
      {
        "name": "بستک"
      },
      {
        "name": "تخت"
      }
    ]
  },
  {
    "name": "همدان",
    "Cities": [
      {
        "name": "دمق"
      },
      {
        "name": "سرکان"
      },
      {
        "name": "آجین"
      },
      {
        "name": "جورقان"
      },
      {
        "name": "برزول"
      },
      {
        "name": "فامنین"
      },
      {
        "name": "سامن"
      },
      {
        "name": "بهار"
      },
      {
        "name": "فرسفج"
      },
      {
        "name": "شیرین سو"
      },
      {
        "name": "مریانج"
      },
      {
        "name": "فیروزان"
      },
      {
        "name": "قروه درجزین"
      },
      {
        "name": "ازندریان"
      },
      {
        "name": "لالجین"
      },
      {
        "name": "گل تپه"
      },
      {
        "name": "گیان"
      },
      {
        "name": "ملایر"
      },
      {
        "name": "صالح آباد"
      },
      {
        "name": "تویسرکان"
      },
      {
        "name": "اسدآباد"
      },
      {
        "name": "همدان"
      },
      {
        "name": "نهاوند"
      },
      {
        "name": "رزن"
      },
      {
        "name": "جوکار"
      },
      {
        "name": "مهاجران"
      },
      {
        "name": "کبودرآهنگ"
      },
      {
        "name": "قهاوند"
      }
    ]
  },
  {
    "name": "یزد",
    "Cities": [
      {
        "name": "مهردشت"
      },
      {
        "name": "حمیدیا"
      },
      {
        "name": "تفت"
      },
      {
        "name": "اشکذر"
      },
      {
        "name": "ندوشن"
      },
      {
        "name": "یزد"
      },
      {
        "name": "عقدا"
      },
      {
        "name": "بهاباد"
      },
      {
        "name": "ابرکوه"
      },
      {
        "name": "زارچ"
      },
      {
        "name": "نیر"
      },
      {
        "name": "اردکان"
      },
      {
        "name": "هرات"
      },
      {
        "name": "بفروییه"
      },
      {
        "name": "شاهدیه"
      },
      {
        "name": "بافق"
      },
      {
        "name": "خضرآباد"
      },
      {
        "name": "میبد"
      },
      {
        "name": "مهریز"
      },
      {
        "name": "احمدآباد"
      }
    ]
  }
]
    """
    databaseRegionalInformation = models.TextField(max_length=5000, blank=False)

# class UserInfo(models.Model):
#     pass
#
#
# class MyHairdressers(models.Model):
#     user = models.ForeignKey(CustomUser, models.PROTECT)
#     office_name = models.CharField(max_length=255, blank=False, null=False)
#     office_phone_number = models.CharField(max_length=17, unique=True, blank=True, null=True)
#     date_joined = models.DateTimeField(_('date joined'), default=timezone.now, serialize=True)
#     email = models.EmailField(_('email address'), max_length=254, unique=True, blank=True, null=True)
#     geolocation = models.ForeignKey(GeoLocation, on_delete=models.CASCADE)
#     city = models.ForeignKey(City, on_delete=models.CASCADE)
#     state = models.ForeignKey(State, on_delete=models.CASCADE)
#     is_active = models.BooleanField(_('active'), default=False,
#                                     help_text=_('Designates whether this user should be treated as '
#                                                 'active. Unselect this instead of deleting accounts.'))
#     picture_profile = models.FileField(upload_to='profile_pictures',
#                                        default=django_settings.MEDIA_URL + 'profile_pictures/user.jpg',
#                                        null=True, blank=True,
#                                        validators=[
#                                            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])])
#
#     class Meta:
#         db_table = 'my_hairdressers'
#
#     @property
#     def get_user_name(self):
#         try:
#             if self.user:
#                 return CustomUser.objects.get(id=int(self.user.pk)).first_name
#             else:
#                 return map(lambda c: c.name, CustomUser.objects.all())
#         except Exception as e:
#             return "Error:%s" % str(e)
#
#     @property
#     def get_state_name(self):
#         try:
#             if self.state:
#                 return State.objects.get(id=int(self.state.pk)).name_of_state
#             else:
#                 return map(lambda c: c.name_of_state, State.objects.all())
#         except Exception as e:
#             return "Error:%s" % str(e)
#
#     @property
#     def get_city_name(self):
#         try:
#             if self.city:
#                 return City.objects.get(id=int(self.city.pk)).name_of_city
#             else:
#                 return map(lambda c: c.name_of_city, City.objects.all())
#         except Exception as e:
#             return "Error:%s" % str(e)
#
#
# class Customer(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
#     my_hairdressers = models.ForeignKey(MyHairdressers, on_delete=models.PROTECT)
#
#     class Meta:
#         db_table = 'customer'
#
#     @property
#     def get_user_name(self):
#         try:
#             if self.user:
#                 return CustomUser.objects.get(id=int(self.user.pk)).first_name
#             else:
#                 return map(lambda c: c.name, CustomUser.objects.all())
#         except Exception as e:
#             return "Error:%s" % str(e)
#
#     @property
#     def get_my_hairdressers_name(self):
#         try:
#             if self.my_hairdressers:
#                 return MyHairdressers.objects.get(id=int(self.my_hairdressers.pk)).office_name
#             else:
#                 return map(lambda c: c.office_name, MyHairdressers.objects.all())
#         except Exception as e:
#             return "Error:%s" % str(e)
