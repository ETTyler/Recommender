import requests
from credentials import api_key
from justwatch import JustWatch


def find_streaming_platforms_by_name(show_name):
    justwatch_url = "https://apis.justwatch.com/content/titles/en_GB/popular"
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

    just_watch = JustWatch(country="GB")
    provider_details = just_watch.get_providers()

    if response.status_code == 200:
        data = response.json()

        if data.get("items"):
            platforms = data["items"][0]["offers"]

            services = []
            for platform in platforms:
                if platform["monetization_type"] == "flatrate":
                    services.append(platform["provider_id"])

            platform_names = []
            for service in services:
                for provider in provider_details:
                    if service == provider["id"]:
                        platform_names.append(provider["clear_name"])

            platform_names = list(set(platform_names))

            return platform_names

    return None


def find_highest_rated_shows(start_date, end_date, num_results):
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
            platforms = find_streaming_platforms_by_name(show["title"])
            print(show["title"] + " (" + show["year"] + ") - " + show["imDbRating"])
            print("Available on: " + ", ".join(platforms) + "\n")

    else:
        print("Error occurred while retrieving data from the IMDb API.")

        # Search for the show on JustWatch API


# Example usage
find_highest_rated_shows("2018", "2020", 5)
