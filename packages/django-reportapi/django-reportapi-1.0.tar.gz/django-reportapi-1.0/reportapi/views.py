# -*- coding: utf-8 -*-
#
#  reportapi/views.py
#  
#  Copyright 2014 Grigoriy Kramarenko <root@rosix.ru>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from __future__ import unicode_literals, print_function
from django.utils.encoding import smart_text
from django.contrib.auth import authenticate, login
from django.core.mail import mail_admins
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, RequestContext
from django.views.debug import ExceptionReporter
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
#~ from django.utils import translation
from django.utils.translation import get_language, ugettext_lazy as _

from datetime import timedelta
import os, sys, datetime, hashlib, traceback, threading

from quickapi.http import JSONResponse, tojson
from quickapi.views import api as quickapi_index, get_methods
from quickapi.decorators import login_required, api_required

from reportapi.sites import site
from reportapi.conf import (settings, REPORTAPI_DEBUG,
    REPORTAPI_FILES_UNIDECODE, REPORTAPI_ENABLE_THREADS,
    REPORTAPI_LANGUAGES)
from reportapi.models import Register, Document

DOCS_PER_PAGE = 25

class PermissionError(Exception):
    message = _('Access denied')

class ExceptionReporterExt(ExceptionReporter):
    """
    Расширение класса отчёта об ошибках
    """
    def get_traceback_data(self):
        ctx = super(ExceptionReporterExt, self).get_traceback_data()
        ctx['os_environ'] = os.environ
        return ctx

    def get_traceback_html(self):
        "Return HTML version of debug 500 HTTP error page."
        t = Template(TECHNICAL_500_TEMPLATE, name='Technical 500 template')
        c = Context(self.get_traceback_data())
        return t.render(c)

########################################################################
# Views for URLs
########################################################################

@login_required
def index(request):
    ctx = _default_context(request)
    return render_to_response('reportapi/index.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def report_list(request, section):
    ctx = _default_context(request)
    if not section in site.sections:
        return render_to_response('reportapi/404.html', ctx,
                            context_instance=RequestContext(request,))
    ctx['section'] = site.sections[section]

    docs = Document.objects.permitted(request).all()
    docs = docs.filter(register__section=section)
    ctx['docs'] = docs[:DOCS_PER_PAGE]

    ctx['reports'] = site.sections[section].get_reports(request)

    return render_to_response('reportapi/report_list.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def documents(request, section=None, name=None):
    """
    Returns inner html with founded documents
    """
    ctx = _default_context(request)

    docs = Document.objects.permitted(request).all()

    if section:
        ctx['section'] = site.sections.get(section, None)
        if not ctx['section'] or not ctx['section'].has_permission(request):
            return render_to_response('reportapi/404.html', ctx,
                            context_instance=RequestContext(request,))
        docs = docs.filter(register__section=section)

    if section and name:
        report, register = site.get_report_and_register(request, section, name)
        if not report or not register:
            return render_to_response('reportapi/404.html', ctx,
                            context_instance=RequestContext(request,))
        ctx['report'] = report
        docs = docs.filter(register__name=name)

    ctx['docs'] = docs[:DOCS_PER_PAGE]

    return render_to_response('reportapi/index.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def report(request, section, name):
    ctx = _default_context(request)
    report, register = site.get_report_and_register(request, section, name)
    if not report or not register:
        return render_to_response('reportapi/404.html', ctx,
                            context_instance=RequestContext(request,))

    ctx['report_as_json'] = tojson(report.get_scheme(request) or dict())
    ctx['report']  = report
    ctx['section'] = site.sections[section]

    return render_to_response('reportapi/report.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def get_document(request, pk, download=False):
    ctx = _default_context(request)
    try:
        doc = Document.objects.permitted(request).get(pk=pk)
    except Exception as e:
        ctx['remove_nav'] = True
        return render_to_response('reportapi/404.html', ctx,
                            context_instance=RequestContext(request,))
    if doc.error:
        return HttpResponse(doc.error, mimetype='text/html')

    if doc.report_file and os.path.exists(doc.report_file.path):
        url = doc.url
        if download:
            return HttpResponseRedirect(url)
        # compatible with old versions
        elif url.endswith('.html'):
            return HttpResponseRedirect(url)

        ctx['DOCUMENT'] = doc

        lang = get_language()
        if lang in REPORTAPI_LANGUAGES:
            lang = '.' + lang
        else:
            lang = ''

        return HttpResponseRedirect('%slib/ViewerJS/index%s.html#%s' %
            (settings.STATIC_URL, lang, url))

    ctx['remove_nav'] = True

    return render_to_response('reportapi/404.html', ctx,
                            context_instance=RequestContext(request,))

########################################################################
# Additional functions
########################################################################

def _default_context(request):
    ctx = {}
    ctx['sections'] = site.get_sections(request)
    docs = Document.objects.permitted(request).all()
    ctx['docs'] = docs[:DOCS_PER_PAGE]
    return ctx

def create_document(request, report, document, filters):
    """ Создание отчёта """
    try:
        report.render(request, document, filters)
    except Exception as e:
        msg = traceback.format_exc()
        print(msg)
        if REPORTAPI_DEBUG:
            exc_info = sys.exc_info()
            reporter = ExceptionReporterExt(request, *exc_info)
            document.error = reporter.get_traceback_html()
        else:
            document.error = '%s:\n%s' % (smart_text(_('Error in template')), msg)

    document.end = timezone.now()
    document.save()

    if not document.error:
        if document.autoconvert():
            document.end = timezone.now()
            document.save()

        delta = document.end - document.start
        ms = int(delta.total_seconds() *1000)
        register = document.register
        if register.timeout < ms:
            register.timeout = ms
            register.save()
        

    return document

def result(request, document, old=False):
    user = request.user
    result = {
        'report_id': document.register_id,
        'id': document.id,
        'start': document.start,
        'end': document.end,
        'user': document.user.get_full_name() or document.user.username,
        'error': document.error or None,
        'timeout': document.register.timeout,
        'has_remove': False,
    }
    if old:
        result['old'] = True
    if document.end:
        result['url'] = document.get_absolute_url()
        if user.is_superuser or document.user == user:
            result['has_remove'] = True
    return JSONResponse(data=result)

########################################################################
# API
########################################################################

@api_required
@login_required
def API_get_scheme(request, **kwargs):
    """ *Возвращает схему ReportAPI для пользователя.*

        ####ЗАПРОС. Без параметров.

        ####ОТВЕТ. Формат ключа "data":
        Схема
    """
    data = site.get_scheme(request)
    return JSONResponse(data=data)

@api_required
@login_required
def API_document_create(request, section, name, filters=None, force=False, fake=False, **kwargs):
    """ *Запускает процесс создания отчёта и/или возвращает информацию
        об уже запущенном процессе.*

        ####ЗАПРОС. Параметры:

        1. "section" - идентификационное название раздела;
        2. "name"    - идентификационное название отчёта;
        3. "filters" - фильтры для обработки результата (необязательно);
        4. "force"   - принудительное создание отчёта (необязательно).

        ####ОТВЕТ. Формат ключа "data":
        Информация о процессе

        ```
        #!javascript
        {
            "id": 1,
            "start": "2014-01-01T10:00:00+0000",
            "user": "Гадя Петрович Хренова",
            "end": null, // либо дата создания
            "url": "",
            "old": null, // true, когда взят уже существующий старый отчёт
            "error": null, // или описание ошибки
            "timeout": 1000, // расчётное время ожидания результата в милисекундах 
        }
        ```

    """
    user = request.user
    session = request.session

    report, register = site.get_report_and_register(request, section, name)
    if not report or not register:
        raise PermissionError()

    code = report.get_code(request, filters)
    expired = timezone.now() - timedelta(seconds=report.expiration_time)

    all_documents = register.document_set.filter(code=code, error='')
    proc_documents = all_documents.filter(end__isnull=True)
    last_documents = all_documents.filter(end__gt=expired)

    if proc_documents:
        # Создающийся отчёт
        return result(request, proc_documents[0])
    elif last_documents and (not force or not report.create_force):
        # Готовый отчёт
        if fake:
            return result(request, last_documents[0])
        return result(request, last_documents[0], old=True)
    else:
        if not report.validate_filters(filters):
            return JSONResponse(status=400, message=_('One or more filters filled in not correctly'))
        # Новый отчёт
        document = Document(user=user, code=code, register=register)
        document.description = report.get_description_from_filters(filters)
        document.details = report.get_details(request, document, filters)
        document.save()

        func_kwargs = {
            'request': request,
            'filters': filters,
            'document': document,
            'report': report,
        }

        if report.enable_threads and REPORTAPI_ENABLE_THREADS:
            # Создание нового потока в режиме демона
            t = threading.Thread(target=create_document, kwargs=func_kwargs)
            t.setDaemon(True)
            t.start()
            return result(request, document)
        else:
            # Последовательное создание отчёта
            r = create_document(**func_kwargs)
            return result(request, document)

@api_required
@login_required
def API_document_info(request, id, section, name, filters=None, **kwargs):
    """ *Возвращает информацию об определённом запущенном или
        завершённом отчёте по заданному идентификационному номеру,
        либо по другим идентификационным данным.*

        ####ЗАПРОС. Параметры:

        1. "id" - идентификатор отчёта;
        2. "section" - идентификационное название раздела;
        3. "name"    - идентификационное название отчёта;
        4. "filters" - фильтры для обработки результата (необязательно);

        ####ОТВЕТ. Формат ключа "data":
        Информация о процессе формирования отчёта

        ```
        #!javascript
        {
            "id": 1,
            "start": "2014-01-01T10:00:00+0000",
            "user": "Гадя Петрович Хренова",
            "end": null, // либо дата создания
            "url": "",
            "error": null, // или описание ошибки
        }
        ```

    """
    if not id:
        return API_document_create(request, section, name, filters, fake=True)
    user = request.user
    all_documents = Document.objects.permitted(request)
    try:
        document = all_documents.get(id=id)
    except:
        return JSONResponse(status=404)
    else:
        return result(request, document)

@api_required
@login_required
def API_document_delete(request, id, **kwargs):
    """ *Удаляет документ по заданному идентификационному номеру.*

        ####ЗАПРОС. Параметры:

        1. "id" - идентификатор отчёта;

        ####ОТВЕТ. Формат ключа "data":

        ```
        #!javascript
        true // если удаление произведено
        ```

    """
    user = request.user
    all_documents = Document.objects.del_permitted(request)
    try:
        document = all_documents.get(id=id)
    except:
        return JSONResponse(status=404)
    else:
        document.delete()
        return JSONResponse(data=True)

@api_required
@login_required
def API_object_search(request, section, name, filter_name, query=None, page=1, **kwargs):
    """ *Производит поиск для заполнения объектного фильтра экземпляром
        связанной модели.*

        ####ЗАПРОС. Параметры:

        1. "section" - идентификационное название раздела;
        2. "name"    - идентификационное название отчёта;
        3. "filter_name" - имя фильтра для связанной модели;
        4. "query" - поисковый запрос (необязательно);
        5. "page" - номер страницы (необязательно);

        ####ОТВЕТ. Формат ключа "data":
        Сериализованный объект страницы паджинатора

        ```
        #!javascript
        {
            "object_list": [
                {"pk": 1, "__unicode__": "First object"},
                {"pk": 2, "__unicode__": "Second object"}
            ],
            "number": 2,
            "count": 99,
            "per_page": 10
            "num_pages": 10,
            "page_range": [1,2,3,'...',9,10],
            "start_index": 1,
            "end_index": 10,
            "has_previous": true,
            "has_next": true,
            "has_other_pages": true,
            "previous_page_number": 1,
            "next_page_number": 3,
        }
        ```
        Это стандартный вывод, который может быть переопределён
        отдельно для каждого отчёта.

    """
    user = request.user
    report = site.get_report(request, section, name)
    if not report:
        return JSONResponse(status=404)
    _filter = report.get_filter(filter_name)
    if not hasattr(_filter, 'search'):
        return JSONResponse(status=400)
    data = _filter.search(query, page)
    return JSONResponse(data=data)


_methods = [
    ('reportapi.get_scheme', API_get_scheme),
    ('reportapi.document_create', API_document_create),
    ('reportapi.document_info', API_document_info),
    ('reportapi.document_delete', API_document_delete),
    ('reportapi.object_search', API_object_search),
]

# store prepared methods
METHODS = get_methods(_methods)

@csrf_exempt
def api(request):
    return quickapi_index(request, methods=METHODS)

#
# Templates are embedded in the file so that we know the error handler will
# always work even if the template loader is broken.
#

TECHNICAL_500_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8">
  <meta name="robots" content="NONE,NOARCHIVE">
  <title>{% if exception_type %}{{ exception_type }}{% else %}Report{% endif %}{% if request %} at {{ request.path_info|escape }}{% endif %}</title>
  <style type="text/css">
    html * { padding:0; margin:0; }
    body * { padding:10px 20px; }
    body * * { padding:0; }
    body { font:small sans-serif; }
    body>div { border-bottom:1px solid #ddd; }
    h1 { font-weight:normal; }
    h2 { margin-bottom:.8em; }
    h2 span { font-size:80%; color:#666; font-weight:normal; }
    h3 { margin:1em 0 .5em 0; }
    h4 { margin:0 0 .5em 0; font-weight: normal; }
    code, pre { font-size: 100%; white-space: pre-wrap; }
    table { border:1px solid #ccc; border-collapse: collapse; width:100%; background:white; }
    tbody td, tbody th { vertical-align:top; padding:2px 3px; }
    thead th { padding:1px 6px 1px 3px; background:#fefefe; text-align:left; font-weight:normal; font-size:11px; border:1px solid #ddd; }
    tbody th { width:12em; text-align:right; color:#666; padding-right:.5em; }
    table.vars { margin:5px 0 2px 40px; }
    table.vars td, table.req td { font-family:monospace; }
    table td.code { width:100%; }
    table td.code pre { overflow:hidden; }
    table.source th { color:#666; }
    table.source td { font-family:monospace; white-space:pre; border-bottom:1px solid #eee; }
    ul.traceback { list-style-type:none; color: #222; }
    ul.traceback li.frame { padding-bottom:1em; color:#666; }
    ul.traceback li.user { background-color:#e0e0e0; color:#000 }
    div.context { padding:10px 0; overflow:hidden; }
    div.context ol { padding-left:30px; margin:0 10px; list-style-position: inside; }
    div.context ol li { font-family:monospace; white-space:pre; color:#777; cursor:pointer; }
    div.context ol li pre { display:inline; }
    div.context ol.context-line li { color:#505050; background-color:#dfdfdf; }
    div.context ol.context-line li span { position:absolute; right:32px; }
    .user div.context ol.context-line li { background-color:#bbb; color:#000; }
    .user div.context ol li { color:#666; }
    div.commands { margin-left: 40px; }
    div.commands a { color:#555; text-decoration:none; }
    .user div.commands a { color: black; }
    #summary { background: #ffc; }
    #summary h2 { font-weight: normal; color: #666; }
    #explanation { background:#eee; }
    #template, #template-not-exist { background:#f6f6f6; }
    #template-not-exist ul { margin: 0 0 0 20px; }
    #unicode-hint { background:#eee; }
    #traceback { background:#eee; }
    #requestinfo { background:#f6f6f6; padding-left:120px; }
    #summary table { border:none; background:transparent; }
    #requestinfo h2, #requestinfo h3 { position:relative; margin-left:-100px; }
    #requestinfo h3 { margin-bottom:-1em; }
    .error { background: #ffc; }
    .specific { color:#cc3300; font-weight:bold; }
    h2 span.commands { font-size:.7em;}
    span.commands a:link {color:#5E5694;}
    pre.exception_value { font-family: sans-serif; color: #666; font-size: 1.5em; margin: 10px 0 10px 0; }
  </style>
  {% if not is_email %}
  <script type="text/javascript">
  //<!--
    function getElementsByClassName(oElm, strTagName, strClassName){
        // Written by Jonathan Snook, http://www.snook.ca/jon; Add-ons by Robert Nyman, http://www.robertnyman.com
        var arrElements = (strTagName == "*" && document.all)? document.all :
        oElm.getElementsByTagName(strTagName);
        var arrReturnElements = new Array();
        strClassName = strClassName.replace(/\-/g, "\\-");
        var oRegExp = new RegExp("(^|\\s)" + strClassName + "(\\s|$)");
        var oElement;
        for(var i=0; i<arrElements.length; i++){
            oElement = arrElements[i];
            if(oRegExp.test(oElement.className)){
                arrReturnElements.push(oElement);
            }
        }
        return (arrReturnElements)
    }
    function hideAll(elems) {
      for (var e = 0; e < elems.length; e++) {
        elems[e].style.display = 'none';
      }
    }
    window.onload = function() {
      hideAll(getElementsByClassName(document, 'table', 'vars'));
      hideAll(getElementsByClassName(document, 'ol', 'pre-context'));
      hideAll(getElementsByClassName(document, 'ol', 'post-context'));
      hideAll(getElementsByClassName(document, 'div', 'pastebin'));
    }
    function toggle() {
      for (var i = 0; i < arguments.length; i++) {
        var e = document.getElementById(arguments[i]);
        if (e) {
          e.style.display = e.style.display == 'none' ? 'block' : 'none';
        }
      }
      return false;
    }
    function varToggle(link, id) {
      toggle('v' + id);
      var s = link.getElementsByTagName('span')[0];
      var uarr = String.fromCharCode(0x25b6);
      var darr = String.fromCharCode(0x25bc);
      s.innerHTML = s.innerHTML == uarr ? darr : uarr;
      return false;
    }
    function switchPastebinFriendly(link) {
      s1 = "Switch to copy-and-paste view";
      s2 = "Switch back to interactive view";
      link.innerHTML = link.innerHTML == s1 ? s2 : s1;
      toggle('browserTraceback', 'pastebinTraceback');
      return false;
    }
    //-->
  </script>
  {% endif %}
</head>
<body>
<div id="summary">
  <h1>{% if exception_type %}{{ exception_type }}{% else %}Report{% endif %}{% if request %} at {{ request.path_info|escape }}{% endif %}</h1>
  <pre class="exception_value">{% if exception_value %}{{ exception_value|force_escape }}{% else %}No exception supplied{% endif %}</pre>
  <table class="meta">
{% if request %}
    <tr>
      <th>Request Method:</th>
      <td>{{ request.META.REQUEST_METHOD }}</td>
    </tr>
    <tr>
      <th>Request URL:</th>
      <td>{{ request.build_absolute_uri|escape }}</td>
    </tr>
{% endif %}
    <tr>
      <th>Django Version:</th>
      <td>{{ django_version_info }}</td>
    </tr>
{% if exception_type %}
    <tr>
      <th>Exception Type:</th>
      <td>{{ exception_type }}</td>
    </tr>
{% endif %}
{% if exception_type and exception_value %}
    <tr>
      <th>Exception Value:</th>
      <td><pre>{{ exception_value|force_escape }}</pre></td>
    </tr>
{% endif %}
{% if lastframe %}
    <tr>
      <th>Exception Location:</th>
      <td>{{ lastframe.filename|escape }} in {{ lastframe.function|escape }}, line {{ lastframe.lineno }}</td>
    </tr>
{% endif %}
    <tr>
      <th>Python Executable:</th>
      <td>{{ sys_executable|escape }}</td>
    </tr>
    <tr>
      <th>Python Version:</th>
      <td>{{ sys_version_info }}</td>
    </tr>
    <tr>
      <th>Python Path:</th>
      <td><pre>{{ sys_path|pprint }}</pre></td>
    </tr>
    <tr>
      <th>OS Environ:</th>
      <td><pre>{{ os_environ|pprint }}</pre></td>
    </tr>
    <tr>
      <th>Server time:</th>
      <td>{{server_time|date:"r"}}</td>
    </tr>
  </table>
</div>
{% if unicode_hint %}
<div id="unicode-hint">
    <h2>Unicode error hint</h2>
    <p>The string that could not be encoded/decoded was: <strong>{{ unicode_hint|force_escape }}</strong></p>
</div>
{% endif %}
{% if template_does_not_exist %}
<div id="template-not-exist">
    <h2>Template-loader postmortem</h2>
    {% if loader_debug_info %}
        <p>Django tried loading these templates, in this order:</p>
        <ul>
        {% for loader in loader_debug_info %}
            <li>Using loader <code>{{ loader.loader }}</code>:
                <ul>{% for t in loader.templates %}<li><code>{{ t.name }}</code> (File {% if t.exists %}exists{% else %}does not exist{% endif %})</li>{% endfor %}</ul>
            </li>
        {% endfor %}
        </ul>
    {% else %}
        <p>Django couldn't find any templates because your <code>TEMPLATE_LOADERS</code> setting is empty!</p>
    {% endif %}
</div>
{% endif %}
{% if template_info %}
<div id="template">
   <h2>Error during template rendering</h2>
   <p>In template <code>{{ template_info.name }}</code>, error at line <strong>{{ template_info.line }}</strong></p>
   <h3>{{ template_info.message }}</h3>
   <table class="source{% if template_info.top %} cut-top{% endif %}{% ifnotequal template_info.bottom template_info.total %} cut-bottom{% endifnotequal %}">
   {% for source_line in template_info.source_lines %}
   {% ifequal source_line.0 template_info.line %}
       <tr class="error"><th>{{ source_line.0 }}</th>
       <td>{{ template_info.before }}<span class="specific">{{ template_info.during }}</span>{{ template_info.after }}</td></tr>
   {% else %}
      <tr><th>{{ source_line.0 }}</th>
      <td>{{ source_line.1 }}</td></tr>
   {% endifequal %}
   {% endfor %}
   </table>
</div>
{% endif %}
{% if frames %}
<div id="traceback">
  <h2>Traceback <span class="commands">{% if not is_email %}<a href="#" onclick="return switchPastebinFriendly(this);">Switch to copy-and-paste view</a></span>{% endif %}</h2>
  {% autoescape off %}
  <div id="browserTraceback">
    <ul class="traceback">
      {% for frame in frames %}
        <li class="frame {{ frame.type }}">
          <code>{{ frame.filename|escape }}</code> in <code>{{ frame.function|escape }}</code>

          {% if frame.context_line %}
            <div class="context" id="c{{ frame.id }}">
              {% if frame.pre_context and not is_email %}
                <ol start="{{ frame.pre_context_lineno }}" class="pre-context" id="pre{{ frame.id }}">{% for line in frame.pre_context %}<li onclick="toggle('pre{{ frame.id }}', 'post{{ frame.id }}')"><pre>{{ line|escape }}</pre></li>{% endfor %}</ol>
              {% endif %}
              <ol start="{{ frame.lineno }}" class="context-line"><li onclick="toggle('pre{{ frame.id }}', 'post{{ frame.id }}')"><pre>{{ frame.context_line|escape }}</pre>{% if not is_email %} <span>...</span>{% endif %}</li></ol>
              {% if frame.post_context and not is_email  %}
                <ol start='{{ frame.lineno|add:"1" }}' class="post-context" id="post{{ frame.id }}">{% for line in frame.post_context %}<li onclick="toggle('pre{{ frame.id }}', 'post{{ frame.id }}')"><pre>{{ line|escape }}</pre></li>{% endfor %}</ol>
              {% endif %}
            </div>
          {% endif %}

          {% if frame.vars %}
            <div class="commands">
                {% if is_email %}
                    <h2>Local Vars</h2>
                {% else %}
                    <a href="#" onclick="return varToggle(this, '{{ frame.id }}')"><span>&#x25b6;</span> Local vars</a>
                {% endif %}
            </div>
            <table class="vars" id="v{{ frame.id }}">
              <thead>
                <tr>
                  <th>Variable</th>
                  <th>Value</th>
                </tr>
              </thead>
              <tbody>
                {% for var in frame.vars|dictsort:"0" %}
                  <tr>
                    <td>{{ var.0|force_escape }}</td>
                    <td class="code"><pre>{{ var.1 }}</pre></td>
                  </tr>
                {% endfor %}
              </tbody>
            </table>
          {% endif %}
        </li>
      {% endfor %}
    </ul>
  </div>
  {% endautoescape %}
  <form action="http://dpaste.com/" name="pasteform" id="pasteform" method="post">
{% if not is_email %}
  <div id="pastebinTraceback" class="pastebin">
    <input type="hidden" name="language" value="PythonConsole">
    <input type="hidden" name="title" value="{{ exception_type|escape }}{% if request %} at {{ request.path_info|escape }}{% endif %}">
    <input type="hidden" name="source" value="Django Dpaste Agent">
    <input type="hidden" name="poster" value="Django">
    <textarea name="content" id="traceback_area" cols="140" rows="25">
Environment:

{% if request %}
Request Method: {{ request.META.REQUEST_METHOD }}
Request URL: {{ request.build_absolute_uri|escape }}
{% endif %}
Django Version: {{ django_version_info }}
Python Version: {{ sys_version_info }}
Installed Applications:
{{ settings.INSTALLED_APPS|pprint }}
Installed Middleware:
{{ settings.MIDDLEWARE_CLASSES|pprint }}

{% if template_does_not_exist %}Template Loader Error:
{% if loader_debug_info %}Django tried loading these templates, in this order:
{% for loader in loader_debug_info %}Using loader {{ loader.loader }}:
{% for t in loader.templates %}{{ t.name }} (File {% if t.exists %}exists{% else %}does not exist{% endif %})
{% endfor %}{% endfor %}
{% else %}Django couldn't find any templates because your TEMPLATE_LOADERS setting is empty!
{% endif %}
{% endif %}{% if template_info %}
Template error:
In template {{ template_info.name }}, error at line {{ template_info.line }}
   {{ template_info.message }}{% for source_line in template_info.source_lines %}{% ifequal source_line.0 template_info.line %}
   {{ source_line.0 }} : {{ template_info.before }} {{ template_info.during }} {{ template_info.after }}
{% else %}
   {{ source_line.0 }} : {{ source_line.1 }}
{% endifequal %}{% endfor %}{% endif %}
Traceback:
{% for frame in frames %}File "{{ frame.filename|escape }}" in {{ frame.function|escape }}
{% if frame.context_line %}  {{ frame.lineno }}. {{ frame.context_line|escape }}{% endif %}
{% endfor %}
Exception Type: {{ exception_type|escape }}{% if request %} at {{ request.path_info|escape }}{% endif %}
Exception Value: {{ exception_value|force_escape }}
</textarea>
  <br><br>
  <input type="submit" value="Share this traceback on a public Web site">
  </div>
</form>
</div>
{% endif %}
{% endif %}

<div id="requestinfo">
  <h2>Request information</h2>

{% if request %}
  <h3 id="get-info">GET</h3>
  {% if request.GET %}
    <table class="req">
      <thead>
        <tr>
          <th>Variable</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        {% for var in request.GET.items %}
          <tr>
            <td>{{ var.0 }}</td>
            <td class="code"><pre>{{ var.1|pprint }}</pre></td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
  {% else %}
    <p>No GET data</p>
  {% endif %}

  <h3 id="post-info">POST</h3>
  {% if filtered_POST %}
    <table class="req">
      <thead>
        <tr>
          <th>Variable</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        {% for var in filtered_POST.items %}
          <tr>
            <td>{{ var.0 }}</td>
            <td class="code"><pre>{{ var.1|pprint }}</pre></td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
  {% else %}
    <p>No POST data</p>
  {% endif %}
  <h3 id="files-info">FILES</h3>
  {% if request.FILES %}
    <table class="req">
        <thead>
            <tr>
                <th>Variable</th>
                <th>Value</th>
            </tr>
        </thead>
        <tbody>
            {% for var in request.FILES.items %}
                <tr>
                    <td>{{ var.0 }}</td>
                    <td class="code"><pre>{{ var.1|pprint }}</pre></td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
  {% else %}
    <p>No FILES data</p>
  {% endif %}


  <h3 id="cookie-info">COOKIES</h3>
  {% if request.COOKIES %}
    <table class="req">
      <thead>
        <tr>
          <th>Variable</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        {% for var in request.COOKIES.items %}
          <tr>
            <td>{{ var.0 }}</td>
            <td class="code"><pre>{{ var.1|pprint }}</pre></td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
  {% else %}
    <p>No cookie data</p>
  {% endif %}

  <h3 id="meta-info">META</h3>
  <table class="req">
    <thead>
      <tr>
        <th>Variable</th>
        <th>Value</th>
      </tr>
    </thead>
    <tbody>
      {% for var in request.META.items|dictsort:"0" %}
        <tr>
          <td>{{ var.0 }}</td>
          <td class="code"><pre>{{ var.1|pprint }}</pre></td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
{% else %}
  <p>Request data not supplied</p>
{% endif %}

  <h3 id="settings-info">Settings</h3>
  <h4>Using settings module <code>{{ settings.SETTINGS_MODULE }}</code></h4>
  <table class="req">
    <thead>
      <tr>
        <th>Setting</th>
        <th>Value</th>
      </tr>
    </thead>
    <tbody>
      {% for var in settings.items|dictsort:"0" %}
        <tr>
          <td>{{ var.0 }}</td>
          <td class="code"><pre>{{ var.1|pprint }}</pre></td>
        </tr>
      {% endfor %}
    </tbody>
  </table>

</div>
{% if not is_email %}
  <div id="explanation">
    <p>
      You're seeing this error because you have <code>DEBUG = True</code> in your
      Django settings file. Change that to <code>False</code>, and Django will
      display a standard 500 page.
    </p>
  </div>
{% endif %}
</body>
</html>
"""
