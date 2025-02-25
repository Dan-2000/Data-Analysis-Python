base_url = "https://itunes.apple.com/search"
r = request.get(base_url, params = {"term": "bring me the horizon", "country": "uk"})
r.status_code