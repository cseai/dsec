import types
from django.urls import get_resolver

def get_urls(url_patterns=None):
    if not url_patterns:
        url_patterns = get_resolver().url_patterns
    url_dict_list = {}
    url_list_dict = []
    for up in url_patterns:
        try:
            if up.pattern and up.app_name and up.namespace:
                url_list = []
                if isinstance(up.urlconf_name, list) and up.urlconf_name:
                    for an_url in up.urlconf_name:
                        url_list.append({
                            'url': f"{up.pattern}{an_url.pattern}",
                            'url_reverse': f"{up.app_name}:{an_url.name}"
                        })
                elif isinstance(up.urlconf_name, types.ModuleType) and up.urlconf_name:
                    for an_url in up.urlconf_name.urlpatterns:
                        url_list.append({
                            'url': f"{up.pattern}{an_url.pattern}",
                            'url_reverse': f"{up.app_name}:{an_url.name}"
                        })
                else:
                    # print(f'url_pattern [NOT ADDED]:{up}')
                    pass
                if len(url_list) > 0:
                    url_dict_list[up.app_name] = url_list
                    url_list_dict.append(url_list)
        except:
            # print(f'url_pattern [EXCEPTION ERROR]:{up}')
            pass
    
    # print(f"url_dict_list:\n {url_dict_list}")

    # return url_dict_list
    return url_list_dict, url_dict_list