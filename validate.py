def validate_request(request_data):
    # validate and verify videourl and mediatype keys
    if 'videourl' not in request_data:
        return False, 'Missing "videourl" key in the request data'
    if 'mediatype' not in request_data:
        return False, 'Missing "mediatype" key in the request data'

    return True, ''

def validate_request_download(request_data):
    # validate and verify videourl and mediatype keys
    if 'videourl' not in request_data:
        return False, 'Missing "videourl" key in the request data'
    if 'itag' not in request_data:
        return False, 'Missing "itag" key in the request data'

    return True, ''