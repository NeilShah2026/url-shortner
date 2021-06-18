
def url_check(url):
    if url.startswith('www.'):
        new_url = url.replace("www.", "https://")
        return new_url
    elif url.startswith('https://'):
        return url