from django.db import models

class Institution(models.Model):
    name                   = models.CharField(max_length=200)
    description            = models.CharField(max_length=500)
    main_site_url          = models.URLField(max_length=255)
    domain                 = models.CharField(max_length=126)
    professor_email_domain = models.CharField(max_length=126)
    student_email_domain   = models.CharField(max_length=126)
    is_for_profit          = models.BooleanField(default=True)
    is_private             = models.BooleanField(default=False)
    institution_type       = models.CharField(max_length=38)
    # instituation_type should store the string representation
    # of one of the institutions.InstitutionType enums as a string
    # (e.g., (str(InstitutionType.University)) ).