from django.views.generic import ListView, DetailView
from whowin.forms import FighterSelectForm
from whowin.models import Fight, Fighter
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class FightView(FormView):

    template_name = 'whowin/match.html'
    success_url = 'success'
    fight = None

    def get_form(self, form_class):
        self.fight = get_object_or_404(Fight, id=self.kwargs['id'])
        choices = [(self.fight.member1.id, self.fight.member1.name),
                   (self.fight.member2.id, self.fight.member2.name)]
        kwargs = super(FightView, self).get_form_kwargs()
        kwargs.update({"choices": choices})
        form = FighterSelectForm(**kwargs)
        return form

    def form_valid(self, form):
        winner = Fighter.objects.get(id=form.cleaned_data['fighter_choices'])
        self.fight.rankupdate(winner)
        return super(FightView, self).form_valid(form)
	

class RankResultsView(ListView):
    queryset = Fighter.objects.order_by('-rating')[:10]
    context_object_name = 'fighter_list'
    template_name = 'whowin/results.html'


class FighterDetailView(DetailView):
    model = Fighter
    template_name = 'whowin/fighterdetail.html'


class FighterListView(ListView):
    template_name = 'whowin/fighterlist.html'
    context_object_name = 'all_fighters'
    queryset = Fighter.objects.order_by('name')

def home_view(request):
    next = Fight.objects.order_by('?')[0]
    return HttpResponseRedirect(reverse('fight', kwargs={'id': next.pk}))