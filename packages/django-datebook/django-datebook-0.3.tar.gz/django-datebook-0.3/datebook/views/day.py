# -*- coding: utf-8 -*-
"""
Day entry views
"""
import datetime

from django.conf import settings
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from datebook.models import Datebook, DayEntry
from datebook.mixins import DatebookCalendarMixin, DatebookCalendarAutoCreateMixin
from datebook.forms.day import DayEntryForm
from datebook.utils import week_from_date

class DayEntryBaseFormView(DatebookCalendarMixin):
    """
    DayEntry base form view
    """
    model = DayEntry
    context_object_name = "dayentry"
    template_name = "datebook/datebook_day_form.html"
    form_class = DayEntryForm

    def get_form(self, form_class):
        """
        Add required args to form instance
        """
        return form_class(self.datebook, self.day, **self.get_form_kwargs())
    
    def get(self, request, *args, **kwargs):
        self.datebook = self.get_datebook({'period__year': self.year, 'period__month': self.month})
        
        return super(DayEntryBaseFormView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.datebook = self.get_datebook({'period__year': self.year, 'period__month': self.month})
        
        return super(DayEntryBaseFormView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('datebook-author-month', kwargs={
            'author': self.author,
            'year': self.object.activity_date.year,
            'month': self.object.activity_date.month,
        })


class DayEntryFormCreateView(DayEntryBaseFormView, generic.CreateView):
    """
    DayEntry form create view
    """
    def get_form_kwargs(self):
        """
        Put the initial data for the datetime start and stop
        
        TODO: Time start and stop should comes from the User profile settings (date 
              allways come from the datebook period and the required day).
        """
        kwargs = super(DayEntryFormCreateView, self).get_form_kwargs()
        day_date = self.datebook.period.replace(day=self.day)
        time_start = datetime.time(9, 0)
        time_stop = datetime.time(18, 0)
        kwargs.update({
            'initial': {
                'start' : datetime.datetime.combine(day_date, time_start),
                'stop' : datetime.datetime.combine(day_date, time_stop),
                'pause' : datetime.time(1, 0),
            }
        })
        return kwargs


class DayEntryFormEditView(DayEntryBaseFormView, generic.UpdateView):
    """
    DayEntry form edit view
    """
    def get_object(self):
        """
        Add required args to form instance
        """
        return self.datebook.dayentry_set.get(activity_date__day=self.day)


#class DayEntryAutoCreateBaseFormView(DatebookCalendarAutoCreateMixin, DayEntryBaseFormView):
    #"""
    #DayEntry base form view for DatebookCalendarAutoCreateMixin
    #"""
    
class DayEntryCurrentView(DatebookCalendarAutoCreateMixin, DayEntryFormCreateView):
    def get(self, request, *args, **kwargs):
        today = self.get_current_date()
        self.datebook = self.get_datebook({'period__year': self.year, 'period__month': self.month})
        
        return super(DayEntryCurrentView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        today = self.get_current_date()
        self.datebook = self.get_datebook({'period__year': self.year, 'period__month': self.month})
        
        return super(DayEntryCurrentView, self).post(request, *args, **kwargs)


class DayEntryCurrentView(generic.RedirectView):
    permanent = False
    
    def get_current_date(self):
        """
        Get the current date
        """
        today = datetime.date.today()
        self.year = self.kwargs['year'] = today.year
        self.month = self.kwargs['month'] = today.month
        self.day = self.kwargs['day'] = today.day
        return today
    
    def get_datebook(self):
        """
        Get or Create datebook
        """
        try:
            obj = Datebook.objects.get(author__username=self.kwargs['author'], period__year=self.year, period__month=self.month)
        except Datebook.DoesNotExist:
            self.author = get_object_or_404(User, username=self.kwargs['author'])
            obj = Datebook(author=self.author, period=datetime.date(self.year, self.month, 1))
            obj.save()
        else:
            self.author = obj.author
        return obj
    
    def get_redirect_url(self, author):
        """
        Get Create or Edit dayentry url
        """
        today = self.get_current_date()
        datebook = self.get_datebook()
        
        try:
            obj = DayEntry.objects.get(datebook=datebook, activity_date=datetime.date(self.year, self.month, self.day))
        except DayEntry.DoesNotExist:
            return reverse('datebook-author-day-add', kwargs={
                'author': self.author,
                'year': self.year,
                'month': self.month,
                'day': self.day,
            })
        else:
            return reverse('datebook-author-day-edit', kwargs={
                'author': self.author,
                'year': self.year,
                'month': self.month,
                'day': self.day,
            })

