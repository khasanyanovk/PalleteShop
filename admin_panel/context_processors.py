from admin_panel.models import SiteSettings


def site_settings(request):
    """Добавляет настройки сайта в контекст всех шаблонов"""
    return {"site_settings": SiteSettings.get_settings()}
