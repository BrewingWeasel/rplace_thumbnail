import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.force-ssl"]
VIDEO_ID = "Xr3nGd1AqpA"

# with open("API_KEY") as f:
#     API_KEY = f.read()


def _get_some_comments(youtube, page_token = ""):
    return youtube.commentThreads().list(
        part="snippet,replies",
        videoId=VIDEO_ID,
        pageToken = page_token,
    ).execute()


def _get_all_comments(youtube, response):
    comments = []
    for item in response["items"]:
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment)

        if "total_reply_count" not in item:
            continue

        for reply in item["replies"]["comments"]:
            reply = reply["snippet"]["textDisplay"]
            comments.append(reply)


    if "nextPageToken" in response:
        comments.extend(_get_all_comments(youtube, _get_some_comments(youtube, page_token=response["nextPageToken"])))

    return comments


def retrieve_comments() -> list[str]:
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "CLIENT_SECRET.json"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    return _get_all_comments(youtube, _get_some_comments(youtube))
    


if __name__ == "__main__":
    retrieve_comments()
