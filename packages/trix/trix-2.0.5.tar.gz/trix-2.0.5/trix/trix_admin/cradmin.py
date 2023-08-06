from django.utils.translation import ugettext_lazy as _
from django_cradmin import crinstance, crmenu
from django.core.urlresolvers import reverse

from trix.trix_core.models import Course
# from .views import dashboard
from .views import assignments
from .views import permalinks
from .views import statistics


class Menu(crmenu.Menu):
    def build_menu(self):
        # self.add(label=_('Dashboard'), url=self.appindex_url('dashboard'),
        #     icon="home")
        self.add(
            label=_('Assignments'),
            url=self.appindex_url('assignments'),
            icon="database")
        self.add(
            label=_('Permalinks'),
            url=self.appindex_url('permalinks'),
            icon="link")
        self.add(
            label=_('Statistics'),
            url=self.appindex_url('statistics'),
            icon='bar-chart-o')
        if self.request.user.is_admin:
            self.add(
                label=_('Courses, users, ...'),
                url=reverse('admin:index'),
                icon='cog')
        self.add(
            label=_('Back to website'),
            url=reverse('trix_student_dashboard'),
            icon='arrow-left')



class CrAdminInstance(crinstance.BaseCrAdminInstance):
    id = 'trix_courseadmin'
    menuclass = Menu
    roleclass = Course
    rolefrontpage_appname = 'assignments'

    apps = [
        # ('dashboard', dashboard.App),
        ('assignments', assignments.App),
        ('permalinks', permalinks.App),
        ('statistics', statistics.App),
    ]

    def get_rolequeryset(self):
        queryset = Course.objects.all()
        if not self.request.user.is_admin:
            queryset = queryset.filter(admins=self.request.user)
        queryset = queryset.select_related('course_tag')
        return queryset

    def get_titletext_for_role(self, role):
        """
        Get a short title briefly describing the given ``role``.
        Remember that the role is a Course.
        """
        return role.course_tag.tag
