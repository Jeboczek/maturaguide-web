from django.shortcuts import redirect, render
from django.core.handlers.wsgi import WSGIRequest
from .forms import MessageForm

# Create your views here.


class ContactView:
    def show_root(request: WSGIRequest):
        if request.method == "POST":
            form = MessageForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("/kontakt/success")
        else:
            form = MessageForm()

        context = {"category": "contact", "form": form}
        return render(request, "contact.html", context)

    def show_success(request : WSGIRequest):
        context = {"category": "contact"}
        return render(request, "success.html", context)