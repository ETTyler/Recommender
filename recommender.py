import requests


def find_streaming_platforms_by_name(show_name):
    justwatch_url = "https://apis.justwatch.com/content/titles/en_US/popular"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    null = None
    payload = {
        "age_certifications": null,
        "content_types": null,
        "presentation_types": null,
        "providers": null,
        "genres": null,
        "languages": null,
        "release_year_from": null,
        "release_year_until": null,
        "monetization_types": null,
        "min_price": null,
        "max_price": null,
        "nationwide_cinema_releases_only": null,
        "scoring_filter_types": null,
        "cinema_release": null,
        "query": show_name,
        "page": null,
        "page_size": null,
        "timeline_type": null,
        "person_id": null,
    }

    response = requests.post(justwatch_url, json=payload, headers=headers)
    print(response.json())

    if response.status_code == 200:
        data = response.json()
        print(data)

        if data.get("items"):
            platforms = data["items"][0]["offers"]

            platform_names = [platform["provider_id"] for platform in platforms]
            return platform_names

    return None


def find_highest_rated_shows(start_date, end_date, num_results):
    api_key = "k_si04o5n5"
    print("Finding the highest rated shows...")
    imdb_url = f"https://imdb-api.com/en/API/MostPopularTVs/{api_key}"
    imdb_response = requests.get(imdb_url)

    if imdb_response.status_code == 200:
        imdb_data = imdb_response.json()
        shows = imdb_data["items"]

        # Filter shows within the specified date range
        filtered_shows = [
            show for show in shows if start_date <= show["year"] <= end_date
        ]

        # Sort shows based on ratings
        sorted_shows = sorted(
            filtered_shows, key=lambda x: float(x["imDbRating"]), reverse=True
        )

        for show in sorted_shows[:num_results]:
            print(show["title"] + " (" + show["year"] + ") - " + show["imDbRating"])

    else:
        print("Error occurred while retrieving data from the IMDb API.")

        # Search for the show on JustWatch API


# Example usage
# find_highest_rated_shows("2018", "2020", 5)

print(find_streaming_platforms_by_name("Succession"))
