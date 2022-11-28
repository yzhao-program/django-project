from django.urls import path
from . import views

urlpatterns = [

    path('notebooks', views.notebooks_view),
    path('add', views.add_view),
    path('update/<int:notebook_id>', views.update_view),
    path('delete', views.delete_view)

]
