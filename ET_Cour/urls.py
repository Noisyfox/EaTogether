from django.conf.urls import url, include

from ET_Cour import views

urlpatterns = [
    url(r"^login/$", views.CourierLoginView.as_view(), name='cour_login'),
    url(r"^order/", include([
        url(r"^$", views.CourierOrderListView.as_view(), name='cour_order'),
        url('^(?P<order_id>[0-9]+)/', include([
            url(r"^$", views.CourierOrderDetailView.as_view(), name='cour_detail'),
            url(r"^(?P<personal_order_id>[0-9]+)/", include([
                url(r"^delivered/$", views.CourierPersonalOrderFinishView.as_view(status='F'),
                    name='cour_order_delivered'),
                url(r"^undelivered/$", views.CourierPersonalOrderFinishView.as_view(status='U'),
                    name='cour_order_undelivered'),
            ])),
        ])),
    ])),
]
