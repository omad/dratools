import typer
from github import Github

ORGS = ['GeoscienceAustralia'] #, 'opendatacube']

def main(name: str):
    typer.echo(f"Hello {name}")
    g = Github("access_token")

    for repo in g.get_user().get_repos():
        print(repo.name)
        print(dir(repo))

    for org_name in ORGS:
        org = g.get_organization(org_name)

        members = org.get_members()
        for member in members:
            keys = member.get_keys()




if __name__ == "__main__":
    typer.run(main)
