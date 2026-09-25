from datetime import datetime
from .models import Profile, SiteSettings, SocialLink


def site_context(request):
    """
    Context processor making profile, site_settings, and social links
    globally available across all templates.
    """
    try:
        profile = Profile.load()
    except Exception:
        profile = None

    try:
        site_settings = SiteSettings.load()
    except Exception:
        site_settings = None

    try:
        social_links = SocialLink.objects.filter(is_active=True).order_by('order')
    except Exception:
        social_links = []

    return {
        'profile': profile,
        'site_settings': site_settings,
        'social_links': social_links,
        'current_year': datetime.now().year,
    }
