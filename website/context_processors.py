


def website_context(request):
    show_cookie_consent = True
    
    if 'cookie-consent' in request.COOKIES:
        show_cookie_consent = False

    context = {
        'show_cookie_consent': show_cookie_consent,
    }
    return context

