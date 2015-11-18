# openfisca-douanes
Simulateur ouvert de taxes de douanes - en développement

## Generate diagram

Due to a bug in mermaid:

- Copy-paste diagram source in http://knsv.github.io/mermaid/live_editor/
- Click on "Download SVG" link
- Run in your shell:
  ```
  rpl http://knsv.github.io/mermaid/live_editor/ "" notes/architecture.svg
  rpl "<br>" "<br/>" notes/architecture.svg
  ```
  > rpl is installable by apt-get
