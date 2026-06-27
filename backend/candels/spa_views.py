from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.views import View


class SpaView(View):
    """Отдаёт index.html React SPA (главная — Home)."""

    def get(self, request, *args, **kwargs):
        index = settings.FRONTEND_DIST / 'index.html'
        if not index.is_file():
            return HttpResponse(
                '<h1>Candels</h1>'
                '<p>Frontend не собран. Выполните:</p>'
                '<pre>cd frontend\nnpm install\nnpm run build</pre>'
                '<p>API: <a href="/api/docs/">/api/docs/</a></p>',
                content_type='text/html; charset=utf-8',
                status=503,
            )
        return FileResponse(index.open('rb'), content_type='text/html; charset=utf-8')
