from backend.server import load_data


def handler(request):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json", "Cache-Control": "s-maxage=3600, stale-while-revalidate=86400"},
        "body": load_data(),
    }
