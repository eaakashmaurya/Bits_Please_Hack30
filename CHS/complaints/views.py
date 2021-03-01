from django.shortcuts import render
from django.urls import reverse_lazy

from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

#from . import forms
from . import models

# Create your views here.

from django.contrib.auth import get_user_model
User = get_user_model()


class UserComplaints(generic.ListView):
    model = models.Complaint
    template_name = "complaints/user_complaint_list.html"

    def get_queryset(self):
        try:
            self.complaint_user = User.objects.prefetch_related("complaints").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.complaint_user.complaints.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["complaint_user"] = self.complaint_user
        return context


class ComplaintDetail(generic.DetailView):
    model = models.Complaint

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreateComplaint(LoginRequiredMixin, generic.CreateView):
    # form_class = forms.PostForm
    fields = ('complaint_face_picture','category','message')
    model = models.Complaint

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeleteComplaint(LoginRequiredMixin, generic.DeleteView):
    model = models.Complaint
    success_url = reverse_lazy("complaint:for_user")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Complaint Deleted")
        return super().delete(*args, **kwargs)