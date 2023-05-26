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
            offers = data["items"][0].get("offers", [])
            platforms = [
                platform["provider_id"]
                for platform in offers
                if platform["monetization_type"] == "flatrate"
            ]

            platform_names = []
            for platform in platforms:
                for provider in provider_details:
                    if platform == provider["id"]:
                        platform_names.append(provider["clear_name"])

            platform_names = list(set(platform_names))

            return platform_names

    return None


def find_highest_rated(start_date, end_date, num_results, option):
    imdb_url = f"https://imdb-api.com/en/API/MostPopular{option}/{api_key}"
    imdb_response = requests.get(imdb_url)

    if imdb_response.status_code == 200:
        imdb_data = imdb_response.json()
        results = imdb_data["items"]

        # Filter shows within the specified date range
        filtered_results = [
            result for result in results if start_date <= result["year"] <= end_date
        ]

        for result in filtered_results:
            if result["imDbRating"] == "":
                result["imDbRating"] = "0.0"

        # Sort shows based on ratings
        sorted_results = sorted(
            filtered_results, key=lambda x: float(x["imDbRating"]), reverse=True
        )

        for result in sorted_results[:num_results]:
            platforms = find_streaming_platforms_by_name(result["title"])
            print(result["fullTitle"] + " - " + result["imDbRating"])
            print("Available on: " + ", ".join(platforms) + "\n")

    else:
        print("Error occurred while retrieving data from the IMDb API.")

        # Search for the show on JustWatch API


# Example usage
find_highest_rated("2018", "2022", 8, "Movies")
