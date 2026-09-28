# Yiyun Zhou's academic homepage

This repository contains the Jekyll source for Yiyun Zhou's academic homepage.

## Editing content

- Biography: `_pages/includes/intro.md`
- News: `_pages/includes/news.md`
- Publications: `_pages/includes/pub.md`
- Honors, service, and education: `_pages/includes/`
- Site styles: `assets/css/main.scss`

Publication images include their intrinsic pixel dimensions and are rendered with `width: auto`, `max-width: 100%`, and `height: auto`. No fixed image height, crop, or forced aspect ratio is used.

## Local preview

```bash
bundle install
bundle exec jekyll serve
```

Then open `http://127.0.0.1:4000`.
