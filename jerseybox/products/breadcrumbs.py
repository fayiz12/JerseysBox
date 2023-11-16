

def get_breadcrumbs(url):
    """Generates a list of breadcrumbs for the given URL."""

    breadcrumbs = []

    # Split the URL path into its individual parts
    parts = url.split('/')

    # Initialize the URL for building the breadcrumbs
    current_url = ''

    for part in parts:
        if part != '':
            current_url += '/' + part
            breadcrumbs.append({
                'label': part,
                'url': current_url
            })

    return breadcrumbs
