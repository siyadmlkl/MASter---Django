from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register/', views.register),
    path('login/', views.logIn),
    path('logout', views.logOut),
    path('create/', views.createWorkOrder),
    path('show/', views.showWorkOrders),
    path('create/selectlocation', views.selectLocation),
    path('create/selectasset', views.selectAssets),
    path('show/filter_wo_area', views.selectArea),
    path('show/filter_wo_location', views.filterByLocation),
    path('show/filter_wo_createdby', views.filterByCreatedby),
    path('show/filter_wo_status', views.filterByStatus),
    path('show/display_wo', views.displayWo),
    path('show/add_wo_event', views.addEvent)

]
