# Changelog

Notable changes to Delair-Stack Python SDK are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.7.6] - 2020-04-24

### Changed

- Use tox to execute unit tests against several Python versions (3.4 to 3.8) (DAI-5488)

### Added

- Add functions to retrieve the logs of your custom analytic executions `sdk.products.retrieve_logs` and `sdk.products.follow_logs` (DAI-5403)
- Add functions to interact with Analytics and Products: `sdk.analytics` and `sdk.products` (DAI-5460)
- Add `has_headerfile` parameter in `sdk.datasets.create_raster_dataset` to support ENVI header file (DAI-5282)
   
## [1.7.5] - 2020-03-03

### Added

- Support the connection through a proxy server (DAI-5047)

## [1.7.4] - 2020-02-04

### Changed

- Move `CHANGELOG.md` in `docs` and use recommonmark to render it in the documentation (DAI-4868)

### Added

- Add a **Getting started Jupyter Notebook** (DAI-4868)

## [1.7.3] - 2020-02-03

### Changed

- Prepare for public release on Github (DAI-4868)

### Added

- Parameter to specify the `domain` at SDK instantiation (DAI-4877)

## [1.7.2] - 2020-01-20

### Changed

- Show `deleted` and hide `dxobjects` in `Project` resources (DAI-4592)
- Improve the logic to download datasets with various filenames and encodings (update `extract_filename_from_headers` to support attachment headers respecting RFC6266) (DAI-4592)

## [1.7.1] - 2020-01-06

### Added

- Retry a chunk upload (multipart) when the token is expired (DAI-4363)

## [1.7.0] - 2019-12-03

### Changed

- `missions.search`: Deprecate the use of the `name` parameter and use UI-Services instead of Project Manager for the other cases (DAI-4204)
- `projects.search`, `projects.delete`: Use UI-Services API instead of Project Manager (DAI-4204)
- `missions.delete`: Use the UI-services API to delete a survey instead of Project Manager (DAI-3855)
- Replace the default configuration file `config-connection.json` by a hardcoded default (DAI-3912)
- Instantiate providers and resources without `config-resources.json` (to allow code completion in the editor) (DAI-3912)
- Make it possible to use various clients (DAI-4009)

### Added

- `projects.search`: Add `deleted` parameter to search for deleted projects (DAI-4204)
- Add the `deleted` option in `projects.describe` to allow the description of a deleted project (`False` by default) (DAI-4024)
