# Yiyun Zhou's academic homepage

This repository contains the Jekyll source for Yiyun Zhou's academic homepage.

## Editing content

- Biography: `_pages/includes/intro.md`
- News: `_pages/includes/news.md`
- Publications: `_pages/includes/pub.md`
- Honors, service, and education: `_pages/includes/`
- Site styles: `assets/css/main.scss`

Publication images use their intrinsic dimensions. Their width may scale with the page, while their height is always calculated automatically from the original aspect ratio.

## Local preview

```bash
bundle install
bundle exec jekyll serve
```

## Google Scholar citation updates

The `Update Google Scholar citations` workflow refreshes the
`google-scholar-stats` branch every day and can also be started manually.
Google Scholar blocks GitHub-hosted runner IP addresses, so the workflow uses
the dedicated [SerpAPI Google Scholar Author API](https://serpapi.com/google-scholar-author-api).
Add a repository Actions secret named `SERPAPI_API_KEY` containing a SerpAPI
key. The crawler validates the returned Scholar ID and citation count before
publishing; failed requests leave the previous valid data untouched.
