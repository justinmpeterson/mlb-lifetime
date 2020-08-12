# Running A Fantasy Season

## Initializing The Season

1. Have a draft.
1. Put your picks in the order in which they occurred in a file named like `data/drafts/(season)-(season_type)-picks.txt`.
1. Update your `.env` file to change whatever needs to change: league, response format, season, season type, draft rounds, etc.
1. Update `data/team_owners.json` to add, activate, or deactivate people as necessary.
1. Run `scripts/deploy.sh` to build this season's Docker image.
    * Pass a `--github` flag to upload the image to GitHub Packages.

## Periodic Stat Updates

1. Run `scripts/grab_html_output.sh` in the Docker image you created in the previous section. That script will generate static HTML files using the latest data, then send them to the web server. The call will look something like this:

```shell
$ docker run -it --rm -e MSF_API_KEY -e MSF_PASSWORD \
  -v ${HOME}/.ssh/tilde.team:/home/luke/.ssh/tilde.team \
  docker.pkg.github.com/justinmpeterson/mlb-lifetime/fantasy-lifetime-mlb:2020-regular scripts/grab_html_output.sh
```

# TODO

- [ ] Refactor so it can work for other leagues and other fantasy formats
- [x] Pass the SSH key at runtime rather than baking it into the Dockerfile
- [x] Create an HTML page that lists unreconciled players per owner
- [x] Put a navbar at the top of each page
- [ ] Add **Last Date Played** to the Stats page, or **On IL**, or something that makes sense
- [ ] Add **Next Probable Start** to the Stats page
- [ ] Enable `?person=John` in the query string so that John's players appear first
- [x] Update `export_html.py` to use environment variables for season and season type, like `the_app.py` does
- [ ] Figure out players like Ohtani who could legitimately contend as both a batter and a pitcher
- [ ] Refactor the `load_picks_from_file()` method in `src/classes/draft.py` to handle non-snake-style or other draft formats, as needed 