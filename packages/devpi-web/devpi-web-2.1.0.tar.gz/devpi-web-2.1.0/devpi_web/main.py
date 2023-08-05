from __future__ import unicode_literals
from chameleon.config import AUTO_RELOAD
from devpi_common.metadata import get_latest_version
from devpi_web.description import render_description
from devpi_web.doczip import unpack_docs
from devpi_web.indexing import iter_projects, preprocess_project
from devpi_web.whoosh_index import Index
from devpi_server.log import threadlog
from pkg_resources import resource_filename
from pyramid.renderers import get_renderer
from pyramid_chameleon.renderer import ChameleonRendererLookup
import os
import sys


def theme_static_url(request, path):
    return request.static_url(
        os.path.join(request.registry['theme_path'], 'static', path))


def macros(request):
    # returns macros which may partially be overwritten in a theme
    result = {}
    paths = [
        resource_filename('devpi_web', 'templates/macros.pt'),
        "templates/macros.pt"]
    for path in paths:
        renderer = get_renderer(path)
        macros = renderer.implementation().macros
        for name in macros.names:
            if name in result:
                result['original-%s' % name] = result[name]
            result[name] = macros[name]
    return result


def navigation_info(request):
    context = request.context
    path = [dict(
        url=request.route_url("root"),
        title="devpi")]
    result = dict(path=path)
    if context.matchdict and 'user' in context.matchdict:
        user = context.username
    else:
        return result
    if 'index' in context.matchdict:
        index = context.index
        path.append(dict(
            url=request.route_url(
                "/{user}/{index}", user=user, index=index),
            title="%s/%s" % (user, index)))
    else:
        return result
    if 'name' in context.matchdict:
        name = context.name
        path.append(dict(
            url=request.route_url(
                "/{user}/{index}/{name}", user=user, index=index, name=name),
            title=name))
    else:
        return result
    if 'version' in context.matchdict:
        version = context.version
        if version == 'latest':
            stage = context.model.getstage(user, index)
            version = stage.get_latest_version(name)
        path.append(dict(
            url=request.route_url(
                "/{user}/{index}/{name}/{version}",
                user=user, index=index, name=name, version=version),
            title=version))
    else:
        return result
    return result


def query_docs_html(request):
    search_index = request.registry['search_index']
    return search_index.get_query_parser_html_help()


class ThemeChameleonRendererLookup(ChameleonRendererLookup):
    auto_reload = AUTO_RELOAD

    def __call__(self, info):
        # if the template exists in the theme, we will use it instead of the
        # original template
        theme_path = getattr(self, 'theme_path', None)
        if theme_path:
            theme_file = os.path.join(theme_path, info.name)
            if os.path.exists(theme_file):
                info.name = theme_file
        return ChameleonRendererLookup.__call__(self, info)


def includeme(config):
    from pyramid_chameleon.interfaces import IChameleonLookup
    from pyramid_chameleon.zpt import ZPTTemplateRenderer
    config.include('pyramid_chameleon')
    # we overwrite the template lookup to allow theming
    lookup = ThemeChameleonRendererLookup(ZPTTemplateRenderer, config.registry)
    config.registry.registerUtility(lookup, IChameleonLookup, name='.pt')
    config.add_static_view('static', 'static')
    theme_path = config.registry['theme_path']
    if theme_path:
        # if a theme is used, we set the path on the lookup instance
        lookup.theme_path = theme_path
        # if a 'static' directory exists in the theme, we add it and a helper
        # method 'theme_static_url' on the request
        static_path = os.path.join(theme_path, 'static')
        if os.path.exists(static_path):
            config.add_static_view('theme-static', static_path)
            config.add_request_method(theme_static_url)
    config.add_route('root', '/', accept='text/html')
    config.add_route('search', '/+search', accept='text/html')
    config.add_route('search_help', '/+searchhelp', accept='text/html')
    config.add_route(
        "docroot",
        "/{user}/{index}/{name}/{version}/+doc/{relpath:.*}")
    config.add_route(
        "docviewroot",
        "/{user}/{index}/{name}/{version}/+d/{relpath:.*}")
    config.add_route(
        "toxresults",
        "/{user}/{index}/{name}/{version}/+toxresults/{basename}")
    config.add_route(
        "toxresult",
        "/{user}/{index}/{name}/{version}/+toxresults/{basename}/{toxresult}")
    config.add_request_method(macros, reify=True)
    config.add_request_method(navigation_info, reify=True)
    config.add_request_method(query_docs_html, reify=True)
    config.scan()


def get_indexer(config):
    indices_dir = config.serverdir.join('.indices')
    indices_dir.ensure_dir()
    return Index(indices_dir.strpath)


def devpiserver_pyramid_configure(config, pyramid_config):
    # make the theme path absolute if it exists and make it available via the
    # pyramid registry
    theme_path = config.args.theme
    if theme_path:
        theme_path = os.path.abspath(theme_path)
        if not os.path.exists(theme_path):
            threadlog.error(
                "The theme path '%s' does not exist." % theme_path)
            sys.exit(1)
        if not os.path.isdir(theme_path):
            threadlog.error(
                "The theme path '%s' is not a directory." % theme_path)
            sys.exit(1)
    pyramid_config.registry['theme_path'] = theme_path
    # by using include, the package name doesn't need to be set explicitly
    # for registrations of static views etc
    pyramid_config.include('devpi_web.main')
    pyramid_config.registry['search_index'] = get_indexer(config)

    # monkeypatch mimetypes.guess_type on because pyramid-1.5.1/webob
    # choke on mimtypes.guess_type on windows with python2.7
    if sys.platform == "win32" and sys.version_info[:2] == (2, 7):
        import mimetypes
        old = mimetypes.guess_type

        def guess_type_str(url, strict=True):
            res = old(url, strict)
            return str(res[0]), res[1]

        mimetypes.guess_type = guess_type_str
        threadlog.debug("monkeypatched mimetypes.guess_type to return bytes")


def devpiserver_add_parser_options(parser):
    web = None
    for action in parser._actions:
        if '--host' in action.option_strings:
            web = action.container
    web.addoption(
        "--theme", action="store",
        help="folder with template and resource overwrites for the web interface")
    indexing = parser.addgroup("indexing")
    indexing.addoption(
        "--index-projects", action="store_true",
        help="index all existing projects")


def devpiserver_pypi_initial(stage, name2serials):
    xom = stage.xom
    ix = get_indexer(xom.config)
    ix.delete_index()
    indexer = get_indexer(xom.config)
    # directly use name2serials?
    indexer.update_projects(iter_projects(xom), clear=True)
    threadlog.info("finished initial indexing op")


def devpiserver_run_commands(xom):
    ix = get_indexer(xom.config)
    if xom.config.args.index_projects:
        ix.delete_index()
        indexer = get_indexer(xom.config)
        indexer.update_projects(iter_projects(xom), clear=True)
        # only exit when indexing explicitly
        return 0
    # allow devpi-server to run
    return None


def delete_project(stage, name):
    if stage is None:
        return
    ix = get_indexer(stage.xom.config)
    ix.delete_projects([preprocess_project(stage, name)])


def index_project(stage, name):
    if stage is None:
        return
    ix = get_indexer(stage.xom.config)
    ix.update_projects([preprocess_project(stage, name)])


def devpiserver_on_upload(stage, projectname, version, link):
    if not link.entry.file_exists():
        # on replication or import we might be at a lower than
        # current revision and the file might have been deleted already
        threadlog.debug("igoring lost upload: %s", link)
    elif link.rel == "doczip":
        unpack_docs(stage, projectname, version, link.entry)
        index_project(stage, projectname)


def devpiserver_on_changed_versiondata(stage, projectname, version, metadata):
    if stage is None:
        # TODO we don't have enough info to delete the project
        return
    if not metadata:
        if stage.get_projectname(projectname) is None:
            delete_project(stage, projectname)
            return
        versions = stage.list_versions(projectname)
        if versions:
            version = get_latest_version(versions)
            if version:
                threadlog.debug("A version of %s was deleted, using latest version %s for indexing" % (
                    projectname, version))
                metadata = stage.get_versiondata(projectname, version)
    if metadata:
        render_description(stage, metadata)
        index_project(stage, metadata['name'])
