from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Personal(models.Model):
    enquiry_no = models.IntegerField(unique=True, editable=False)
    enquiry_date = models.DateField(auto_now=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    Gender = models.CharField(max_length=50)
    DOB = models.DateField()
    Contact_no = models.IntegerField()
    Whatsapp_no = models.IntegerField()
    Qualification = models.CharField(max_length=100)

    def __str__(self):
        return self.Name

    def save(self, *args, **kwargs):
        if not self.enquiry_no:
            last_record = Personal.objects.all().order_by('enquiry_no').last()
            if last_record:
                self.enquiry_no = last_record.enquiry_no + 1
            else:
                self.enquiry_no = 1
        super(Personal, self).save(*args, **kwargs)

class College(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    college = models.CharField(max_length=100)

    def __str__(self):
        return self.college

class Course(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.CharField(max_length=100)

    def __str__(self):
        return self.course

class WorkExperiance(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.company

