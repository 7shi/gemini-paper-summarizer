# Changelog

## [0.8.1] - 2025-05-21
### Changed
- Updated default model to `gemini-2.5-flash-preview-05-20`

## [0.8.0] - 2025-04-22
### Changed
- Migrated client library from `google-generativeai` to `google-genai`
- Refactored retry mechanism and removed the `--rpm` option
- Updated default model to `gemini-2.5-flash-preview-04-17`

## [0.7.0] - 2025-02-19
### Added
- Support for input file formats beyond PDF

## [0.6.1] - 2025-02-08
### Changed
- Updated prompts to specify only title translation
- Updated examples

## [0.6.0] - 2025-02-08
### Changed
- Translation for paper's title

## [0.5.4] - 2025-02-08
### Added
- `--suffix` option for custom file naming
- `--ccache` option for reducing API usage costs

## [0.5.3] - 2025-02-07
### Changed
- Updated default model to `gemini-2.0-flash`
### Added
- `-m/--model` option to specify Gemini model
- `--rpm` option to set maximum requests per minute (default: 15)

## [0.5.2] - 2025-01-15
### Improved
- Improved waiting time display with progress bar in `generate_content`
- Improved prompt display with current and total PDF count

## [0.5.1] - 2025-01-14
### Added
- `--version` option to display package version
- Added examples

## [0.5.0] - 2025-01-14
### Added
- Multilingual support for `de`, `en`, `es`, `fr`, `ja`, `ko`, `zh` language modules
- Support for processing multiple PDF files in a single run
- Output directory option (`-d` or `--output-dir`)
### Improved
- Enhanced Gemini API call reliability with retry mechanism and logging
- Added Windows file globbing support

## [0.4.0] - 2025-01-11
### Changed
- Refactored project structure to use `gp_summarize` package
- Standardized test cases using pytest format
- Reorganized statistical display items and calculated TPS (Tokens Per Second)

## [0.3.0] - 2025-01-06
### Changed
- Updated system prompt to output in a more formal Japanese style (だ・である調)
- Modified intermediate file generation to save files in the same location as the specified output file

## [0.2.0] - 2025-01-05
### Changed
- Restructured section files to be created in source-named directories to distribute numerous files
- Limited API requests to 10 per minute (65 seconds margin) to align with Gemini's free tier limitations

## [0.1.0] - 2025-01-04
### Added
- Initial release of the project
