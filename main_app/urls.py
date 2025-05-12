from django.urls import path
from .views import (
    Home,
    CreateUserView,
    LoginView,
    VerifyUserView,
    ServiceList,
    ServiceDetail,
    DiscountRuleListCreate,
    AppointmentListCreate,
    AppointmentDetail,
)

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("signup/", CreateUserView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("verify/", VerifyUserView.as_view(), name="verify"),
    path("services/", ServiceList.as_view(), name="service-list"),
    path("services/<int:id>/", ServiceDetail.as_view(), name="service-detail"),
    path("discount-rules/", DiscountRuleListCreate.as_view(), name="discount-rule"),
    path("appointments/", AppointmentListCreate.as_view(), name="appointment-list"),
    path("appointments/<int:id>/", AppointmentDetail.as_view(), name="appointment-detail"),
]
