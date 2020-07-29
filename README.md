# Running A Fantasy Season

## Initializing The Season

1. Have a draft.
1. Put your picks in the order in which they occurred in a file named like `data/drafts/(season)-(season_type)-picks.txt`.
1. Update your `.env` file to change whatever needs to change: league, response format, season, season type, draft rounds, etc.
1. Update `data/team_owners.json` to add, activate, or deactivate people as necessary.
1. Run `deployment/deploy.sh` to build this season's Docker image.

## Periodic Stat Updates

1. Run `scripts/grab_html_output.sh` in the Docker image you created in the previous section. Something like this:

```shell
$ docker run -it --rm -e MSF_API_KEY -e MSF_PASSWORD fantasy-lifetime-mlb:2020-regular scripts/grab_html_output.sh
```

# TODO

- [ ] Refactor so it can work for other leagues and other fantasy formats
- [ ] Pass the SSH key at runtime rather than baking it into the Dockerfile
- [ ] Create an HTML page that lists unreconciled players per owner
- [ ] Put a navbar at the top of each page
- [ ] Add **Last Date Played** to the Stats page, or **On IL**, or something that makes sense
- [ ] Add **Next Probable Start** to the Stats page
- [ ] Enable `?person=John` in the query string so that John's players appear first
- [ ] Update `export_html.py` to use environment variables for season and season type, like `mvp.py` does