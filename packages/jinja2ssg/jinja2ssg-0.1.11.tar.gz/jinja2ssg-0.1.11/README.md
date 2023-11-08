# Jinja2 SSG

A very simple static site generator.

- The filesystem structure in `--src` is copied into `--dest`.
- Files and folders starting with `_` are skipped.
- By default only html, txt, js files are used and the rest of them are skipped.
- YAML files can be used to provide data inside templates.

```bash
python3 -m pip install jinja2ssg
python3 -m jinja2ssg --src src --dest publish build
```

# Example

```
site/src/
├── _base.html
├── _social_links.yaml
├── donate
│   └── index.html
├── _footer.html
├── index.html
└── _nav.html
```

Results in a DEST structure like:

```
site/www/
├── index.html
└── donate
    └── index.html
```


## Common patterns

- Run with  `inotify` to rebuild on source file changes.
  ```bash
      inotifywait --recursive --monitor --format "%e %w%f" \
      --event modify,move,create,delete ./src \
      | while read changed; do
          echo $changed
          (python3 -m jinja2ssg build)
      done
  ```
- Put social links inside `_social.yaml` files and access as `{{ yaml._social.facebook }}`
- Access all build paths using `{{ build_paths }}`. Useful while writing
  service worker code to cache the site as a PWA.
- Access `{{ relative_path }}` to know the path of the current file being rendered.
