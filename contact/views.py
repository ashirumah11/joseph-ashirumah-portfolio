import logging
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from .forms import ContactForm
from .models import ContactMessage

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """Extract client IP address handling proxies and forwarders."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def contact_page(request):
    """Standalone contact page view."""
    if request.method == 'POST':
        return process_contact_submission(request, is_standalone_page=True)
    
    form = ContactForm()
    return render(request, 'contact/contact.html', {'form': form})


@require_POST
def submit_contact_message(request):
    """Handles POST submissions from the homepage contact section or AJAX."""
    return process_contact_submission(request, is_standalone_page=False)


def process_contact_submission(request, is_standalone_page=False):
    """Core contact form processor supporting standard form POST and AJAX requests."""
    is_ajax = (
        request.headers.get('x-requested-with') == 'XMLHttpRequest' or
        'application/json' in request.headers.get('Accept', '')
    )

    form = ContactForm(request.POST)

    if form.is_valid():
        contact_msg = form.save(commit=False)
        contact_msg.ip_address = get_client_ip(request)
        contact_msg.save()

        # Send optional email notification to configured contact address
        recipient_email = getattr(settings, 'CONTACT_EMAIL', '') or getattr(settings, 'DEFAULT_FROM_EMAIL', '')
        if recipient_email:
            try:
                subject_line = f"[Portfolio Contact] {contact_msg.subject} from {contact_msg.name}"
                body_content = (
                    f"New message from your portfolio contact form:\n\n"
                    f"Name: {contact_msg.name}\n"
                    f"Email: {contact_msg.email}\n"
                    f"Subject: {contact_msg.subject}\n\n"
                    f"Message:\n{contact_msg.message}\n\n"
                    f"---\nSent via Joseph Ashirumah Portfolio"
                )
                send_mail(
                    subject=subject_line,
                    message=body_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient_email],
                    fail_silently=True,
                )
            except Exception as e:
                logger.warning(f"Could not dispatch contact email notification: {e}")

        success_msg = "Thank you! Your message has been sent successfully. I will get back to you shortly."

        if is_ajax:
            return JsonResponse({
                'success': True,
                'message': success_msg,
            })

        messages.success(request, success_msg)
        if is_standalone_page:
            return redirect('contact:contact_page')
        return redirect('/#contact')

    # Form errors
    if is_ajax:
        return JsonResponse({
            'success': False,
            'errors': form.errors,
            'message': 'Please fix the errors indicated in the form.',
        }, status=400)

    messages.error(request, "There was an error in your submission. Please check the fields below.")
    if is_standalone_page:
        return render(request, 'contact/contact.html', {'form': form})
    
    # Homepage fallback with form errors
    return redirect('/#contact')
