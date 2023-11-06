import asyncio
import shlex
import socket
import dotenv
from typing import Tuple

#import heroku3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

from config import BRANCH, GIT_TOKEN, HEROKU_API_KEY, HEROKU_APP_NAME, REPO_URL
from pixy import LOGGER

HAPP = None

XCB = [
    "/",
    "@",
    ".",
    "com",
    ":",
    "git",
    "heroku",
    "push",
    str(HEROKU_API_KEY),
    "https",
    str(HEROKU_APP_NAME),
    "HEAD",
    "main",
]


def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    return asyncio.get_event_loop().run_until_complete(install_requirements())


def git():
    REPO_LINK = REPO_URL
    if GIT_TOKEN:
        GIT_USERNAME = REPO_LINK.split("com/")[1].split("/")[0]
        TEMP_REPO = REPO_LINK.split("https://")[1]
        UPSTREAM_REPO = f"https://{GIT_USERNAME}:{GIT_TOKEN}@{TEMP_REPO}"
    else:
        UPSTREAM_REPO = REPO_URL
    try:
        repo = Repo()
        LOGGER("pixy").info(f"Git Client Found")
    except GitCommandError:
        LOGGER("pixy").info(f"Invalid Git Command")
    except InvalidGitRepositoryError:
        repo = Repo.init()
        if "origin" in repo.remotes:
            origin = repo.remote("origin")
        else:
            origin = repo.create_remote("origin", UPSTREAM_REPO)
        origin.fetch()
        repo.create_head(
            BRANCH,
            origin.refs[BRANCH],
        )
        repo.heads[BRANCH].set_tracking_branch(origin.refs[BRANCH])
        repo.heads[BRANCH].checkout(True)
        try:
            repo.create_remote("origin", REPO_URL)
        except BaseException:
            pass
        nrs = repo.remote("origin")
        nrs.fetch(BRANCH)
        try:
            nrs.pull(BRANCH)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        install_req("pip3 install --no-cache-dir -U -r requirements.txt")
        LOGGER("pixy").info("Fetched Latest Updates")


def is_heroku():
    return "heroku" in socket.getfqdn()


def heroku():
    global HAPP
    if is_heroku:
        if HEROKU_API_KEY and HEROKU_APP_NAME:
            try:
                Heroku = heroku3.from_key(HEROKU_API_KEY)
                HAPP = Heroku.app(HEROKU_APP_NAME)
                LOGGER("pixy").info(f"Heroku App Configured")
            except BaseException as e:
                LOGGER("Heroku").error(e)
                LOGGER("Heroku").info(
                    f"Make sure your HEROKU_API_KEY and HEROKU_APP_NAME are configured correctly in the heroku config vars."
                )
                
async def in_heroku():
    return "heroku" in socket.getfqdn()


async def create_botlog(client):
    if HAPP is None:
        return
    LOGGER("pixy").info(
        "Making the botlog group for you, please wait for a minute..."
    )
    desc = "Group Log for Pixsuvy-Bot.\n\nPLEASE DO NOT LEAVE THIS GROUP.\n\nPowered By ~ @pixsuvy"
    try:
        gruplog = await client.create_supergroup("Logs Pixsuvy-Bot", desc)
        if await in_heroku():
            heroku_var = HAPP.config()
            heroku_var["BOTLOG_CHATID"] = gruplog.id
        else:
            path = dotenv.find_dotenv("config.env")
            dotenv.set_key(path, "BOTLOG_CHATID", gruplog.id)
    except Exception:
        LOGGER("pixy").warning(
            "Your BOTLOG_CHATID var has not been filled in. Create a telegram group and enter the bot @MissRose_bot then type /id Enter the group ID in var BOTLOG_CHATID"
        )

