from django.db import models
from django.template.defaultfilters import slugify
from markdown import markdown
from django.core.validators import validate_email, RegexValidator

check_phone = '^(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?$'

class Resume(models.Model):
    """
    Sample Usage:
        Design Resume, Physics Resume, Data
    """
    title = models.CharField(
        'Name',
        max_length=100,
        help_text='Usually just your name',)
    subtitle = models.CharField(
        'subtitle',
        max_length=100,
        help_text='e.g. Math 2b 1234567')
    purpose = models.CharField(
        max_length=250,
        help_text='Mission Statement')
    skills = models.TextField(
        help_text='Your skills summary, markdown is allowed')

    #Person
    address_1 = models.CharField(max_length=250)
    address_2 = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=250,
                            validators=[validate_email])
    phone_number = models.CharField(max_length=15,
                                    validators=[RegexValidator(
                                        regex=check_phone,
                                        message='Please Input correct phone number')])

    #hidden fields
    skills_html = models.TextField(blank=True, null=True)
    last_modified = models.DateField(auto_now=True)
    slug = models.SlugField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.skills_html = markdown(self.skills)
        self.slug = slugify(self.title)
        super(Resume, self).save(*args, **kwargs)

class Topic(models.Model):
    """
    Sample Usage:
        Extra-Curricular, Work Experience, Volunteer, Projects
    """
    resume = models.ForeignKey('Resume', related_name='topics',)
    title = models.CharField(max_length=100)
    desc = models.TextField(
        'Description',
        help_text='Markdown Support, First block of content',
        blank=True,
        null=True,)
    order = models.IntegerField(unique=True)
    desc_html = models.TextField(
        blank=True,
        null=True,)

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.desc_html = markdown(self.desc)
        super(Topic, self).save(*args, **kwargs)

class Experience(models.Model):
    topic = models.ForeignKey('Topic', related_name='listing')
    name = models.CharField(max_length=150)
    organization = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    desc = models.TextField('Description',
                            help_text='Limited markdown is supported')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True,)
    desc_html = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['topic', '-start_date']

    def __unicode__(self):
        return "{}\t({})".format(self.topic.title, self.name)

    def save(self, *args, **kwargs):
        self.desc_html = markdown(self.desc)
        super(Experience, self).save(*args, **kwargs)
