from django.db import models
from markdown import markdown
from django.template.defaultfilters import slugify


class Term(models.Model):

    """ Term:
    Nominally specifies the time period.

    Usage.
        Spring 2014 -- TRIUMF
        Fall 2014 -- Wolfram Alpha
    """
    name = models.CharField(max_length=250,
                            help_text='e.g. Spring 2014 TRIUMF')
    desc = models.TextField()

    # You cannot save a term without posts under it.
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['start', '-pk']

    def __unicode__(self):
        return self.name


class Entry(models.Model):
    """ Entry:
    Object that contains a post that has a certain type of `style`.
    The Entry takes in a Markdown format file that is compiled to html
    on save.

    Fields:
        title = Duh, its a title. It also generates the slug.
        content_md = Markdown content that compiles to html.
        term = One save, gets assigned the most recent term.
        post_type = defines the type of post.
            'jxnl.co/writing/exmaple-title/2'
        desc = alt/description test.
    """

    title = models.CharField(max_length=100)
    content_md = models.TextField('Content')
    image  = models.ImageField(
        'Image', upload_to='thumbnails/', blank=True, null=True)
    desc = models.CharField('Description', max_length=200)
    tags = models.CharField('Tag', max_length=140)

    POST_TYPE = (
        ('making', 'Project'),
        ('writing', 'Writing'),
        ('designing', 'Design'),
        ('drawing', 'Art'),)

    style = models.CharField('Type of Post', choices=POST_TYPE, max_length=10)

    mod_date = models.DateTimeField('Last Modified', auto_now=True)
    start_date = models.DateField('Starting Date')

    # Hidden/Automatically Generated
    slug = models.SlugField(unique=True)
    content_html = models.TextField(blank=True)
    term = models.ForeignKey("Term", related_name="posts", blank=True, null=True)
    has_math = models.BooleanField(default=False)
    has_code = models.BooleanField(default=False)
    urllink = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['-mod_date', '-pk']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.term = Term.objects.latest("pk")
        self.content_html = markdown(self.content_md,
                                     safe_mode='escape',
                                     extensions=['toc','smarty', 'extra'],
                                    )
        if '<code>' in self.content_html:
            self.has_math = True;
        if '$$' in self.content_html:
            self.has_code = True;
        self.urllink = "/{}/{}/{}/".format(self.style, self.pk, self.slug)
        super(Entry, self).save(*args, **kwargs)
