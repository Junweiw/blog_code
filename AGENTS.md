# AGENTS.md

## Cursor Cloud specific instructions

### What this repo is
This repo (`blog_code`) is a collection of independent tutorial/demo projects, not a
single deployable application. Each top-level folder is self-contained. There is no
root build system, no shared backend, no unified dev/lint/test command, and no
package manager manifest at the repo root.

### Runtimes available in this environment
- `python3` and `node` are preinstalled.
- `php`, `composer`, and `mysql` are NOT installed.

### What can actually be run/tested end-to-end here
- Fully local, no credentials needed: the static client-side apps, especially
  `shenzhen-gjj-calculator/` (the actively-developed product, deployed to GitHub
  Pages by `.github/workflows/deploy-gjj-calculator.yml` on push to `master` when
  that folder changes). Other static demos: `css_button/`, `disable_inputs/`,
  `fixed_navigation_bar/`, `star_rating/`.
- NOT runnable end-to-end without external setup: the PHP demos
  (`facebook_login_php/`, `twitter_login_php/`, `twitter_tweet_php/`,
  `instagram_*/`, `reddit_api_php/`, `fortnite_*/`, `wow_game_data_api/`,
  `star_rating_saves/`). They require `php` (not installed) plus third-party API
  credentials, and two of them also require MySQL. Treat these as reference code.

### Running a static app in development
Serve the folder over localhost (Cursor's browser cannot load `file://`):
```
cd shenzhen-gjj-calculator   # or another static folder
python3 -m http.server 8080 --bind 127.0.0.1
```
Then open `http://127.0.0.1:8080/index.html`.

### Lint / test / build
There is no lint, automated test, or build tooling in this repo. The static apps
are plain HTML/CSS/JS with no build step; "running" them is serving the folder.
