"""Publish only this repo using the user's existing Git Credential Manager account.

No token is printed, stored in files, embedded in remotes or passed on argv.
"""
import argparse
import os
from pathlib import Path
import subprocess
import requests


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--owner",default="exsinger-hub")
    parser.add_argument("--name",default="sivia-ModelAtlas")
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    environment={**os.environ,"GIT_TERMINAL_PROMPT":"0","GCM_INTERACTIVE":"never"}
    # Requests reads the OS proxy on Windows; libcurl/Git needs it explicitly.
    proxy=requests.utils.get_environ_proxies("https://github.com").get("https")
    if proxy:
        environment.setdefault("https_proxy",proxy)
        environment.setdefault("http_proxy",proxy)
    request=f"protocol=https\nhost=github.com\nusername={args.owner}\n\n"
    credential=subprocess.run(["git","credential","fill"],input=request,text=True,capture_output=True,env=environment,timeout=25)
    values=dict(line.split("=",1) for line in credential.stdout.splitlines() if "=" in line)
    if credential.returncode or not values.get("password"):
        raise SystemExit("No usable GitHub credential available for the requested account")
    session=requests.Session()
    session.headers.update({"Authorization":"Bearer "+values["password"],"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28"})
    user=session.get("https://api.github.com/user",timeout=25)
    if user.status_code!=200 or user.json().get("login","").lower()!=args.owner.lower():
        raise SystemExit("GitHub credential verification failed or returned a different owner")
    print("Authenticated GitHub account:",user.json()["login"])
    target=f"https://api.github.com/repos/{args.owner}/{args.name}"
    response=session.get(target,timeout=25)
    if args.check:
        print("Repository:","exists" if response.status_code==200 else f"HTTP {response.status_code}")
        if response.status_code==200:
            print({key:response.json().get(key) for key in ("html_url","default_branch","size","private","pushed_at")})
            contents=session.get(target+"/contents",timeout=25)
            if contents.status_code==200:
                print("Root entries:",[x["name"] for x in contents.json()])
        return
    if response.status_code==404:
        response=session.post("https://api.github.com/user/repos",json={"name":args.name,"private":True,"description":"Paper to overview with a verified MCM/ICM illustration knowledge base"},timeout=25)
        if response.status_code!=201:
            raise SystemExit(f"Repository creation failed: HTTP {response.status_code}")
    elif response.status_code!=200:
        raise SystemExit(f"Repository lookup failed: HTTP {response.status_code}")
    repo=response.json()
    remotes=subprocess.check_output(["git","remote"],cwd=root,text=True).splitlines()
    if "origin" in remotes:
        remote=subprocess.check_output(["git","remote","get-url","origin"],cwd=root,text=True).strip()
        if remote!=repo["clone_url"]:
            raise SystemExit("Existing origin differs; leaving it unchanged")
    else:
        subprocess.run(["git","remote","add","origin",repo["clone_url"]],cwd=root,check=True)
    subprocess.run(["git","config","credential.https://github.com.username",args.owner],cwd=root,check=True)
    branch=subprocess.check_output(["git","branch","--show-current"],cwd=root,text=True).strip()
    subprocess.run(["git","push","-u","origin",branch],cwd=root,check=True,env=environment,timeout=90)
    head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=root,text=True).strip()
    remote_head=subprocess.check_output(["git","ls-remote","origin",f"refs/heads/{branch}"],cwd=root,text=True,env=environment,timeout=25).split()[0]
    if head!=remote_head:
        raise SystemExit("Remote verification failed")
    print(repo["html_url"],head,"private="+str(repo["private"]))


if __name__=="__main__":
    main()
