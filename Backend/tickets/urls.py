from django.urls import path

from .views import ClassificationView, HomeView, TicketHistoryView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("api/classify/", ClassificationView.as_view(), name="classify-ticket"),
    path("api/history/", TicketHistoryView.as_view(), name="ticket-history"),
]
