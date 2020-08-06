#! /usr/bin/python3
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

# tested with pygithub 1.52 from PyPi
from github import Github
# in Fedora, this is python3-keyring
# personal access token stored with CLI: `keyring set login pygithub`
import keyring

# variables to edit
org_name = 'yourorg'
prefix = 'yourprojectprefix'
# branch protection will be removed from old branch, but
# the branch itself won't be deleted
old_default_branch = 'master'
# new branch should exist already; if not, clone and do this first:
# `git remote update origin && git push origin origin/master:refs/heads/main`
new_default_branch = 'main'

# authenticate and grab the org
token = keyring.get_password('login', 'pygithub')
org = Github(token).get_organization(org_name)

for repo in org.get_repos(type='public'):
    if repo.name.startswith(prefix):
        print(f'Updating "{org_name}/{repo.name}"...')
        print(f'    -> Changing default branch to "{new_default_branch}"...')
        repo.edit(default_branch = new_default_branch)
        # this branch protection only stops force pushes and deletions, nothing else
        print(f'    -> Setting branch protection on "{new_default_branch}"...')
        repo.get_branch(new_default_branch).edit_protection()
        # this may or may not remove the branch protection, depending on whether
        # branch protection rule is using a pattern or an exact name; if it has an
        # exact name that matches the old default branch, all protections will be
        # removed, not just the deletion and force push restrictions
        branch = repo.get_branch(old_default_branch)
        if branch.protected:
            print(f'    -> Removing branch protection from "{old_default_branch}"...')
            repo.get_branch(old_default_branch).remove_protection()
        else:
            print(f'    -> (Skipped) Branch protection not set on "{old_default_branch}"')
        print('    Done.')

