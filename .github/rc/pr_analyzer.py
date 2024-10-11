
def read_json(_filename:str) -> dict:
    import json
    with open(_filename, 'r') as file:
        data = json.load(file)
    return data

class GitMgr:
    """Manage git actions operation."""

    def __init__(self, _repo: str, _current_branch: str, _token: str) -> None:
        """Initialize git manager objec."""
        self.repo_ = _repo
        self.cbranch_ = _current_branch
        self.token_ = _token

    def get(self,_pull_request_id:int) -> None:
        l_api_method = (
            f"https://api.github.com/repos/{self.repo_}/pulls/{_pull_request_id}"
        )
        
        l_h_op_1 = "Accept: application/vnd.github+json"
        l_h_op_2 = f"Authorization: Bearer {self.token_}"
        l_h_op_3 = "X-GitHub-Api-Version: 2022-11-28"
        
        l_output = "response.json"
        
        l_curl_cmd = (
            f"curl -o {l_output} -L "
            + f'-H "{l_h_op_1}" -H "{l_h_op_2}" -H "{l_h_op_3}"'
            + " "
            + l_api_method
        )

        __import__("os").system(l_curl_cmd)
        return read_json(l_output)

class PRHdr:
    """manages pull requests."""
    def __init__(self,_pr:dict) -> None:
        self.pr=_pr

    def is_root(self) -> bool:
        if self.pr['user']['login'] == self.pr['head']['repo']['owner']['login']:
            return True
        return False

    def is_review_requested(self) -> bool:
        return True if len(self.pr['requested_reviewers']) == 1 else False


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        sys.exit()

    l_pr_id = int(sys.argv[1])
    l_repo = sys.argv[2]
    l_branch = sys.argv[3]
    l_token = sys.argv[4]
    
    l_gitmgr = GitMgr(l_repo,l_branch,l_token)
    l_data = l_gitmgr.get(l_pr_id)
    root = PRHdr(l_data).is_root()
    review_requested = PRHdr(l_data).is_review_requested()

    if '-r' in sys.argv:
        root = PRHdr(l_data).is_root()
        if not root:
            raise Exception("actor is not root")

    if '-rr' in sys.argv:
        review_requested = PRHdr(l_data).is_review_requested()
        if not review_requested:
            raise Exception("actor needs to ask review request")
