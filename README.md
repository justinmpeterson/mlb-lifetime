# Running A Fantasy Season

## Initializing The Season

1. Have a draft.
1. Put your picks in the order in which they occurred in a file named like `data/drafts/(season)-(season_type)-picks.txt`.
1. Rename `data/team_owners.json.sample` to `data/team_owners.json` and update it to add, activate, or deactivate people as necessary.
1. Upload picks.txt and owners.json to an S3 bucket
    * `s3://(bucket-name)/fantasy/(fantasy-league-type)/(fantasy-league)/(fantasy-season)/(fantasy-season-type)/`
    * e.g., `s3://jmp.fantasy/fantasy/lifetime/mlb/2020/regular/`
1. Rename `.env.sample` to `.env` and change whatever needs to change: league, season type, draft rounds, etc.
1. Run `scripts/deploy.sh` to build this season's Docker image.
    * Pass a `--github` flag to upload the image to GitHub Packages.
    * Pass a `--arm` flag if you are building this image on a Raspberry Pi or other machine running an ARM processor
    * Pass a `--s3` flag if, rather than using the local picks.txt and owners.json files, it should pull them from an S3 bucket

## Periodic Stat Updates

1. Run `scripts/grab_html_output.sh` in the Docker image you created in the previous section. That script will generate static HTML files using the latest data, then send them to the web server. The call will look something like this:

```shell
$ docker run -it --rm -e MSF_API_KEY -e MSF_PASSWORD -e NEOCITIES_API_KEY \
    docker.pkg.github.com/justinmpeterson/mlb-lifetime/fantasy-lifetime-mlb:2020-regular scripts/grab_html_output.sh
```

## Environment Variables

The application and container are heavily (overly?) reliant on environment variables. In addition to the handful you find in `.env.sample`, you may wish to initialize others that will help you do various things with the application.

* `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` -- if you want to be able to pull seed data files from an S3 bucket, you'll need an AWS key and secret that will allow you to access the bucket in which they're stored.
* `GITHUB_PACKAGE_TOKEN` -- if you want to deploy your locally-built Docker image to GitHub's image repository, you'll need an API token to be able to do so.
* `MSF_API_KEY` and `MSF_PASSWORD` -- if you want to access data using the MySportsFeeds API, you'll need to provide an API key and your account password.
* `NEOCITIES_API_KEY` -- if you want to upload static content to Neocities to make your league's data publicly accessible, you'll need an API key.

A reasonable best practice might be to store all of these credentials and secrets in your CI/CD platform of choice (e.g., Jenkins), then have your build job load them as environment variables before running any of the scripts in this repo.

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