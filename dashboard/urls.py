from django.conf.urls import url

from dashboard.views import DashboardView, PictureDetailView, PictureAddView, PictureDeleteView

urlpatterns = [
    url(r'^picture/add', PictureAddView.as_view(), name='picture_add'),
    url(r'^picture/delete/(?P<slug>[-\w]+)', PictureDeleteView.as_view(), name='picture_delete'),
    url(r'^picture/(?P<slug>[-\w]+)', PictureDetailView.as_view(), name='picture_info'),
    url(r'^', DashboardView.as_view(), name='dashboard'),
]