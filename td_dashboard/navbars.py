from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


no_url_namespace = True if settings.APP_NAME == 'td_dashboard' else False

td_dashboard = Navbar(name='td_dashboard')

td_dashboard.append_item(
    NavbarItem(
        name='eligible_subject',
        title='Subject Screening',
        label='Subject Screening',
        fa_icon='fa fa-user-plus',
        url_name=settings.DASHBOARD_URL_NAMES[
            'screening_listboard_url'],
        no_url_namespace=no_url_namespace))

td_dashboard.append_item(
    NavbarItem(
        name='consented_subject',
        title='Maternal Subjects',
        label='maternal subjects',
        fa_icon='far fa-user-circle',
        url_name=settings.DASHBOARD_URL_NAMES[
            'subject_listboard_url'],
        no_url_namespace=no_url_namespace))

td_dashboard.append_item(
    NavbarItem(
        name='infant_subject',
        title='Infant Subjects',
        label='infant subjects',
        fa_icon='far fa-user-circle',
        url_name=settings.DASHBOARD_URL_NAMES[
            'infant_listboard_url'],
        no_url_namespace=no_url_namespace))

site_navbars.register(td_dashboard)
