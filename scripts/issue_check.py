#pip install PyGithub

import os
from github import Github
from github import Auth
import requests
import json

auth = Auth.Token(os.getenv('GITHUB_TOKEN'))
g = Github(auth=auth)

url = os.getenv('ISSUE_URL')
if url == None:
    print("No issue url, try get input from env")
    url = os.getenv('ISSUE_URL_INPUT')
split = url.split('/')

repoName = split[3]+"/"+split[4]
issueId = int(split[6])

repo = g.get_repo(repoName)
issue = repo.get_issue(number=issueId)

checked = requests.post("https://ic.j2.cx/",issue.body.encode('utf-8')).json()
print(checked)

if checked["type"] == 'bug report':
    result = ""

    if checked["steps"] == 'none':
        result += "- ❌未提供复现步骤信息 does not provide steps for reproduction\r\n"
    if checked["code"] == 'none':
        result += "- ❌未提供复现所需的代码或工程 does not provide codes or project for reproduction\r\n"
    if checked["log"] == 'none':
        result += "- ❌未提供出错时需要的日志文件 does not provide logs when bug happening\r\n"
    if checked["envirnment"] == 'none':
        result += "- ❌未提供你的运行环境与版本 does not provide the envirnment you are using\r\n"

    if result != "":
        issue.create_comment("⚠ 你的Issue可能缺少了一些信息，请自觉补全，以证明issue内容的真实性：\r\n\r\n"+
                            "⚠ Your issue may be missing some information, please complete it to prove the authenticity of the content of the issue:\r\n\r\n"+
                            result)
elif checked["type"] == 'feature request':
    if checked["feature"] == 'incomplete':
        issue.create_comment("⚠ 你的Issue可能缺少了一些信息，请自觉补全，以证明issue内容的真实性：\r\n\r\n"+
                            "⚠ Your issue may be missing some information, please complete it to prove the authenticity of the content of the issue:\r\n\r\n"+
                            "- ❌未提供功能需求的详细描述 does not provide detailed description of the feature request\r\n")

