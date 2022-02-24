import argparse
from profile import Profile
from utils.utils import get_cookies

class ProfileWithReplies(Profile):
    base_url = "https://twitter.com/i/api/graphql/{user_tweets_url_token}/UserTweetsAndReplies?variables="
    url_params = {
        "withCommunity": True,
        "userId":"",
        "count":40,
        "includePromotedContent":True,
        "withQuickPromoteEligibilityTweetFields":True,
        "withSuperFollowsUserFields":True,
        "withDownvotePerspective":False,
        "withReactionsMetadata":False,
        "withReactionsPerspective":False,
        "withSuperFollowsTweetFields":True,
        "withVoice":True,
        "withV2Timeline":False,"__fs_dont_mention_me_view_api_enabled":False,"__fs_interactive_text_enabled":False,"__fs_responsive_web_uc_gql_enabled":False}

    def update_cookies(self, username):
        self.cookies, self.headers, self.userid, self.url_profile_token = get_cookies(username, True)
        self.url_params['userId'] = self.userid

parser = argparse.ArgumentParser(description='Script to get tweet from certain user.')
parser.add_argument("-u", "--username")
parser.add_argument("-l", "--limit", default=0, type=int)
args = parser.parse_args()

p = ProfileWithReplies(args.username, args.limit)
p.start_request()