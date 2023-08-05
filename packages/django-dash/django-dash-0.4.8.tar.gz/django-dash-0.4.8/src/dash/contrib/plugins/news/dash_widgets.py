__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('BaseNewsWidget', 'News2x5Widget', 'News4x5Widget')

from django.template.loader import render_to_string

from dash.base import BaseDashboardPluginWidget
from dash.contrib.plugins.news.constants import PAGE_URL_PARAM, NUM_POSTS_URL_PARAM

# ***********************************************************************
# ********************** Base widget for Memo plugin ********************
# ***********************************************************************

class BaseNewsWidget(BaseDashboardPluginWidget):
    """
    Base news widget.
    """
    media_css = [
        'css/dash_plugin_news.css',
    ]

    def render(self, request=None):
        context = {'plugin': self.plugin,}
        return render_to_string('news/render.html', context)

# ***********************************************************************
# ********************** Specific widgets for Memo plugin ***************
# ***********************************************************************

class News2x5Widget(BaseNewsWidget):
    """
    News plugin 2x5 widget.
    """
    plugin_uid = 'news_2x5'
    cols = 2
    rows = 5

    media_js = [
        'js/dash_plugin_2x5_news.js',
    ]


class News4x5Widget(BaseNewsWidget):
    """
    News plugin 4x5 widget.
    """
    plugin_uid = 'news_4x5'
    cols = 4
    rows = 5

    media_js = [
        'js/dash_plugin_4x5_news.js',
    ]

    def render(self, request=None):
        context = {
            'plugin': self.plugin,
            'PAGE_URL_PARAM': PAGE_URL_PARAM,
            'NUM_POSTS_URL_PARAM': NUM_POSTS_URL_PARAM
            }
        return render_to_string('news/render_4x5_main.html', context)
