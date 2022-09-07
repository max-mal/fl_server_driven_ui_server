from googleapiclient.discovery import build

class YoutubeService:
    api_key = "AIzaSyBypitiAnUitwr4jssKwmtYTAtU7LmBQzs"
    client = None

    def get_client(self):
        if self.client is not None:
            return self.client

        api_service_name = "youtube"
        api_version = "v3"
        self.client = build(api_service_name, api_version, developerKey=self.api_key)

        return self.client

    def search(self, text: str):
        request = self.get_client().search().list(
            q=text,
            part='snippet',
            maxResults=25,
        )

        if len(text) == 0:
            request = self.get_client().videos().list(
                part='snippet',
                chart='mostPopular',
                maxResults=25,
            )

        return request.execute()

    def get(self, id: str) -> tuple[dict, dict]:
        request = self.get_client().videos().list(
            part="snippet,contentDetails,statistics",
            id=id,
        )

        video = request.execute()['items'][0]

        # request = self.get_client().commentThreads().list(
        #     part="snippet,replies",
        #     videoId=id,
        # )

        # comments = request.execute()['items']

        return video

