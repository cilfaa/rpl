def global_search_query(request):
    return {
        "search_query": request.GET.get("q", "").strip()
    }