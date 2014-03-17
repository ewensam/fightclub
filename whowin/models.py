from django.db import models
from django.template.defaultfilters import slugify
from datetime import datetime


class Fighter(models.Model):
    name = models.CharField(max_length=50)
    SIDE_CHOICES = (
        ('E', 'Evil'),
        ('G', 'Good'),
        ('N', 'Neutral'),
    )
    side = models.CharField(max_length=1, choices=SIDE_CHOICES, default='N')
    description = models.TextField(default='')
    slug = models.SlugField(default=0, max_length=50, unique=True)
    rating = models.DecimalField(default=1600, max_digits=8, decimal_places=2)
    fightswon = models.IntegerField(default=0)
    fightslost = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Fighter, self).save(*args, **kwargs)


class Fight(models.Model):
    member1 = models.ForeignKey(Fighter, related_name='fighter_1')
    member2 = models.ForeignKey(Fighter, related_name='fighter_2')

    winner = models.ForeignKey(Fighter, related_name='winner', null=True, blank=True)
    winner_start_rank = models.IntegerField(null=True, blank=True)
    winner_end_rank = models.IntegerField(null=True, blank=True)
    winner_start_rating = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
    winner_end_rating = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)

    loser = models.ForeignKey(Fighter, related_name='loser', null=True, blank=True)
    loser_start_rank = models.IntegerField(null=True, blank=True)
    loser_endnd_rank = models.IntegerField(null=True, blank=True)
    loser_start_rating = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
    loser_end_rating = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)

    start = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    end = models.DateTimeField(null=True, blank=True, auto_now=True)

    def __unicode__(self):
        return '%s - %s v %s' % (self.start, self.winner, self.loser)

    def rankupdate(self, winner):
        if winner == self.member1:
            loser = self.member2
        else:
            loser = self.member1

        winnerval = 1 / (1 + 10 ** ((loser.rating - winner.rating) / 400))
        loserval = 1 - winnerval

        winner.rating += 20 * (1 - winnerval)
        winner.fightswon += 1
        loser.rating += 20 * (0 - loserval)
        loser.fightslost += 1

        loser.save()
        winner.save()
