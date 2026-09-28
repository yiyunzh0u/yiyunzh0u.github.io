# Yiyun Zhou's academic homepage

A lightweight, responsive academic homepage built with Jekyll and hosted on GitHub Pages.

## Content

- Edit publication entries in `_data/publications.yml`.
- Edit recent updates in `_data/news.yml`.
- Edit biography, honors, service, and education in `index.html`.
- Edit visual styles in `assets/css/site.css`.

Publication images preserve their original aspect ratio. The layout uses a bounded visual area with `object-fit: contain`, so wide and near-square figures are displayed without stretching or cropping.

## Local preview

```bash
bundle install
bundle exec jekyll serve
```

Then open `http://127.0.0.1:4000`.
