from django.contrib.auth.views import LoginView
from django.contrib import messages
# Create your views here.
class CustomLoginView(LoginView):

    def form_invalid(self, form):
        messages.error(self.request, 'Usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.')
        return super().form_invalid(form)