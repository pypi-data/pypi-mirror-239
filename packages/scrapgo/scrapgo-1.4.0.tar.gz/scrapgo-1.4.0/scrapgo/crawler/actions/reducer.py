from scrapgo.lib import select_kwargs, filter_params, find_function, curl2requests, assingles
from .base import UrlRenderAction, UrlPatternAction, FileAction, CurlAction
from .exceptions import *



class ReduceMixin:

    def get_action(self, name):
        for action in self.urlorders:
            if action.name == name:
                return action    

    def dispatch_response(self, action, **kwargs):
        if isinstance(action, CurlAction):
            command = kwargs.get('url')
            request_kwargs = curl2requests(command)
            for key in ['headers', 'cookies', 'proxies']:
                curlval = request_kwargs.get(key)
                cmnval = kwargs.get(key)
                if curlval is not None or cmnval is not None:
                    curlval = curlval or {}
                    curlval.update(cmnval or {})
                    request_kwargs[key] = curlval

            return self.fetch(refresh=action.refresh, delay=action.delay, **request_kwargs)

        method = action.method or ('post' if kwargs.get('data') else 'get')
        return self.fetch(
            method=method, refresh=action.refresh, delay=action.delay,
            ignore_status_codes=action.ignore_status_codes,
            allowable_status_codes=action.allowable_status_codes,
            **kwargs
        )

    @assingles
    def dispatch_renderer(self, action, response, responsemap, prev_results, prev_action):
        kwargs = {
            'parent_response': response,
            'responsemap': responsemap,
            'prev': prev_results,
        }
        if prev_action:
            kwargs[prev_action.name] = prev_results

        if isinstance(action, UrlRenderAction):
            if urlrenderer := action.urlrenderer:
                kwargs['url'] = action.url
                return self.dispatch('urlrenderer', urlrenderer, **kwargs)                
            return action.url

        elif isinstance(action, UrlPatternAction):
            if urlpattern_renderer := action.urlpattern_renderer:
                kwargs['pattern'] = action.urlpattern
                urlpattern = self.dispatch('urlpattern_renderer', urlpattern_renderer, **kwargs)
                if urlpattern is None:
                    raise UrlRendererError(f"{urlpattern_renderer} must return regex pattern of url, not {urlpattern}")
            else:
                urlpattern = action.urlpattern
            linkpattern_kwargs = {
                **action.as_kwargs(),
                'urlpattern': urlpattern
            }
            return self.parse_linkpattern(response.content, **linkpattern_kwargs)
    
        elif isinstance(action, CurlAction):
            if command_renderer:= action.command_renderer:
                kwargs['command'] = action.command
                return self.dispatch('curlrenderer', command_renderer, **kwargs)
            return action.command
        elif isinstance(action, FileAction):
            if path_renderer := action.path_renderer:
                kwargs['path'] = action.path
                return self.dispatch('path_renderer', path_renderer, **kwargs)
            return action.path
        else:
            raise CannotFindAction(f'{action} is not memeber of renderer action')

    @assingles
    def dispatch_payloader(self, action, responsemap, prev_results, prev_action):
        if not hasattr(action, 'payloader') or not action.payloader:
            return {}
        else:
            kwargs = {
                'responsemap': responsemap,
                'prev': prev_results,
            }
            if prev_action:
                kwargs[prev_action.name] = prev_results
            return self.dispatch('payloader', action.payloader, **kwargs)
            
    def dispatch_fields(self, action, url):
        if not hasattr(action, 'fields'):
            return url
        url = filter_params(url, action.fields)
        return url

    def dispatch_headers(self, action):
        headers = self.get_headers()
        if hasattr(action, 'headers'):
            headers.update(action.headers or {})
        return headers
    
    def dispatch_cookies(self, action):
        cookies = self.get_cookies()
        if hasattr(action, 'cookies'):
            cookies.update(action.cookies or {})
        return cookies

    def dispatch_extractor(self, action, meta, response, prev_results, results_cache, prev_action):
        extractset = {}
        if module := action.extractor:
            pat = r'^extract_(?P<ext>\w+)$'
            for g, func in find_function(module, pat):
                kwargs = {
                    'response': response,
                    'meta': meta,
                    'soup': meta.soup,
                    'prev': prev_results,
                    'results_set': results_cache
                }

                if prev_action:
                    kwargs[prev_action.name] = prev_results

                extracted = select_kwargs(func, **kwargs)
                extractset[g('ext')] = self.validate_extracted(extracted, func, meta)
        return extractset

    def dispatch_parser(self, action, response, extracted, meta, prev_results, results_cache, prev_action):
        kwargs = {
            'response': response,
            'parsed': extracted,
            'meta': meta,
            'prev': prev_results,
            'results_set': results_cache,
        }
        if prev_action:
            kwargs[prev_action.name] = prev_results

        results = self.dispatch('parser', action.parser, **kwargs)
        return results

    def dispatch_urlfilter(self, action, url, responsemap, prev_results, prev_action):
        if not hasattr(action, 'urlfilter'):
            return True

        kwargs = {
            'url': url,
            'responsemap': responsemap,
            'prev': prev_results,
        }
        if prev_action:
            kwargs[prev_action.name] = prev_results

        return self.dispatch('urlfilter', action.urlfilter, **kwargs)
    
    def dispatch_referer(self, action, response):
        headers = self.get_headers()
        if not hasattr(action, 'referer'):
            return headers
        
        if action.referer and response:
            try:
                referer = response.crawler.responsemap[action.referer]
            except KeyError:
                raise CannotFindAction(f"An action named {action.referer} could not be found at urlorders.")
            else:
                headers['Referer'] = referer.url
        return headers

    def dispatch_compose(self, results_set):
        if hasattr(self, 'compose'):
            for action in self.urlorders:
                results_set.setdefault(action.name, [])
            composed = self.dispatch(
                'compose', self.compose,
                **results_set
            )
            return composed

    def dispatch_onfailure(self, action, exception, response, responsemap, prev_results, prev_action, **requests_kwargs):
        kwargs = {
            'response': response,
            'exception': exception,
            'responsemap': responsemap,
            'prev': prev_results,
        }
        if prev_action:
            kwargs[prev_action.name] = prev_results
        kwargs.update(requests_kwargs)
        self.dispatch('onfailure', action.onfailure, **kwargs)

    def dispatch_ignore_status_codes(self, action, response):
        if hasattr(action, 'ignore_status_codes'):
            ignore_codes =  action.ignore_status_codes or []
            return response.status_code in ignore_codes
        return False
    
    ## trash
    def dispatch_allowable_status_codes(self, action, response):
        if hasattr(action, 'allowable_status_codes'):
            alloable_codes = action.allowable_status_codes or []
            return response.status_code in alloable_codes
        return False

    def dispatch(self, type, func, *args, **kwargs):
        if callable(func):
            f = func
        elif isinstance(func, str):
            if hasattr(self, func):
                f = getattr(self, func)
            else:
                raise NotImplementedError(f"The method {func} is not implemented!")
        else:
            f = {
                'urlfilter': self.default_urlfilter,
                'parser': self.default_parser,
                'urlrenderer': self.default_urlrenderer,
                'urlpattern_renderer': self.default_pattern_renderer,
                'breaker': self.default_breaker,
                'onfailure': self.onfailure,
                'payloader': self.default_payloader,
                'curlrenderer': self.default_curlrenderer,
                'path_renderer': self.default_path_renderer,
            }[type]

        return select_kwargs(f, *args, **kwargs)
    

    def default_urlfilter(self, url, **kwargs):
        return True

    def onfailure(self, exception, **kwargs):
        raise
    
    def default_breaker(self, response, **kwargs):
        return False

    def default_parser(self, response, **kwargs):
        return
    
    def default_urlrenderer(self, url, response, **kwargs):
        yield url
    
    def default_curlrenderer(self, curl, resposne, **kwargs):
        return curl
    
    def default_path_renderer(self, path, response, **kwargs):        
        return path
        
    def default_pattern_renderer(self, pattern, resposne, **kwargs):
        return pattern
    
    def default_breaker(self, response, **kwargs):
        return False
    
    def default_payloader(self):
        yield