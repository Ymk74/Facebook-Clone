from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from PIL import Image
from shortuuid.django_fields import ShortUUIDField
import shortuuid

GENDER = (
    ("male", "Male"),
    ("female", "Female")
)

class User(AbstractUser):
    full_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=200)
    gender = models.CharField(max_length=100, choices=GENDER, null=True, blank=True, default='male')    

    otp = models.CharField(max_length=10, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

RELATIONSHIP = (
    ("single","Single"),
    ("married","Married"),
)





# هذا الكود يُستخدم في إعداد مسار (path) لتخزين الملفات المرفوعة بواسطة مستخدمين. يستخدم هذا الكود في نظام إطار العمل (framework) Django لتحديد مكان تخزين الملفات.
#change path save all file
def user_directory_path(instance, filename):
    # 200.jpg
    ext = filename.split('.')[-1]    # split------> .jpg
    filename = "%s.%s" % (instance.user.id, ext)
    return 'user_{0}/{1}'.format(instance.user.id,  filename)



RELATIONSHIP = (
    ("single","Single"),
    ("married","Married"),
)

class Profile(models.Model):
    pid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # cover_images = models.ImageField(upload_to='Images')     change path
    cover_image = models.ImageField(upload_to=user_directory_path, default="cover.jpg", blank=True, null=True)
    image = models.ImageField(upload_to=user_directory_path, default="default.png", blank=True, null=True)
    full_name = models.CharField(max_length=200, null=True ,blank=True)
    phone = models.CharField(max_length=200, null=True ,blank=True)
    # about_me = models.CharField(max_length=1000, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER, null=True, blank=True)
    relationship = models.CharField(max_length=100, choices=RELATIONSHIP, null=True, blank=True)
    bio = models.CharField(max_length=200 ,null=True ,blank=True)
    about_me = models.TextField(null=True ,blank=True)
    country = models.CharField(max_length=200 ,null=True ,blank=True)
    city = models.CharField(max_length=200 ,null=True ,blank=True)
    state = models.CharField(max_length=200 ,null=True ,blank=True)
    address = models.CharField(max_length=200 ,null=True ,blank=True)
    work_at = models.CharField(max_length=200 ,null=True ,blank=True)
    instagram = models.CharField(max_length=200 ,null=True ,blank=True)
    whatsapp = models.CharField(max_length=200 ,null=True ,blank=True)
    verified = models.BooleanField(default=False)
    followers = models.ManyToManyField(User, related_name="Followers",null=True ,blank=True)
    following = models.ManyToManyField(User, related_name="Following",null=True ,blank=True)
    friends = models.ManyToManyField(User, related_name="Friends",null=True ,blank=True)
    blocked = models.ManyToManyField(User, related_name="blocked",null=True ,blank=True)
    date = models.DateTimeField(auto_now_add=True ,null=True ,blank=True)
    slug = models.SlugField(unique=True ,null=True ,blank=True)

    def __str__(self):
        return self.user.username

    # import shortuuid
    def save(self, *args , **kwargs):
        if self.slug == "" or self.slug == None:
            uuid_key = shortuuid.uuid()  
            uniqueid = uuid_key[:2] 
            self.slug = slugify(self.full_name) + '-' + str(uniqueid.lower()) 
        super(Profile, self).save(*args, **kwargs)


# create user profile automatic
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile ,sender=User)
post_save.connect(save_user_profile ,sender=User)