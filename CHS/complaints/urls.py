from django.urls import path, include
from . import views

app_name='complaints'

urlpatterns = [
    path('new/', views.CreateComplaint.as_view(), name='create'),
    path('by/<username>/', views.UserComplaints.as_view(), name='for_user'),
    path('by/<username>/<int:pk>/', views.ComplaintDetail.as_view(), name='single'),
    path('delete/<int:pk>', views.DeleteComplaint.as_view(), name='delete'),

]