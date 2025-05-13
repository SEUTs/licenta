import requests

def check(username, tag):
    def isGood(content):
        return not content.__contains__("NEXT_HTTP_ERROR_FALLBACK;404\\")

    link = f"https://op.gg/lol/summoners/eune/{username}-{tag}"
    request = requests.get(link)
    content = str(request.content)
    print(link)
    return isGood(content)

if __name__ == "__main__":
    print(check("zimbrul macara", "eune"))
    print(check("fergus123", "eunes"))