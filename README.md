# Job Seekers' Friendly Tool For Quick Search Management

Application Tracker, Resume and Cover Letter Maker

## Current features _(partial list)_

1. Database to keep track of previous job applications, including the specific values used for each placeholder.
2. Autofill for placeholders named ``position`` (case-sensitive; substring or otherwise): as a substring will be automatically replaced with the position's title (requires picking the relevant position first).
    1. This is done only in empty fields.
3. Auto-increments file names if the name already exists (in the ``docs\Applications`` folder).
4. Automatically prepends the creation date to older PDFs file names if there's a conflict with a new pdf.
5. Automatically fills in the last used templates.
6. Placeholders with identical labels are treated as identical, allowing you to save time by re-using common placeholders (see ``position`` above).
7. Where a placeholder spans multiple Runs, formatting will be based on the first Run in the group.
    1. a Run is the main structure of ``docx`` files.
8. Tested on Windows, functionality may differ on other platforms.

### Placeholders Explanation

Placeholders are special markers in the text that get replaced with actual values dynamically.

- **``[[ ... ]]`` Default**: These contain a default value. If not replaced, they retain the pre-existing content .
    - Example: `[[Job Title]]` → If not changed, will remain "Job Title".
- **``{{ ... }}`` Required**: These are "mandatory" fields that must be replaced. They have no internal value by default.
    - Example: `{{Company Name}}` → Should be filled in.

- **``| ... |`` Labels**: This portion will be used as the field's placeholder.
    - Only use-able with square brackets; this is the normal functionality for required placeholders.
    - Example: `{{|Company Name|Enter the name of the hiring company}}` → The box will be labeled "Company Name".
    - **``@`` (Grouping Separator, Not Fully Implemented)**: Used to split placeholders into groups for structured replacements.
        - Example: `[[|Job Title@Company Name|Company]]` → Indicates a grouping; only "Company Name" will be used for the label.

#### On-Off Placeholders

Once implemented, these will allow dynamic use of a [Flet](https://flet.dev/) [Switch](https://flet.dev/docs/controls/switch/) to remove entire sections of the text.

#### Multi-level Placeholders

Once implemented, these will enable nesting, where one placeholder can resolve into another, allowing for structured replacements.

## Related Links

* [Felt GitHub repository](https://github.com/flet-dev/flet)
* [Flet website](https://flet.dev/)

## Plans for Future Development

1. Enable link replacement
2. Add additional automatic-replacements capabilities (similar to 'position').
3. Enable On-Off placeholders
4. Enable Multi-level Placeholders
5. Enable a methodology to extract keywords from job postings for faster automatic replacement.
6. Enable use of links in placeholders.
7. Enable 'history' to allow to pick from past values.
8. Add optional links to employers.
9. Allow multiple links for each job posting and employer for increased flexibility.
10. Expand on use of variables and tags.
11. Add contacts.
12. Add communication tracking.
13. Improve the consistency of placeholders' behaviour.
14. _Done_ ~~Add a ``requirments.txt``~~
15. Improve the data view window.
16. Portability:
    1. Make portable to non-windows platforms (Mac, Linux, iOS, Android)
17. Deployment:
    1. Desktop (downloadable installation/exe).
    2. Web or Website.
    3. Android and/or iOS app.
18. Use [Black](https://github.com/psf/black) for code formatting (as advised by [Flet](https://flet.dev/)'s official dev team).
19. Enable working with job search engines (LinkedIn, Indeed, Monster).
20. More informative presentation of placeholders.
21. Improve accessibility.
22. Improve portability.
23. Create a wiki, tutorials and/or how-to guides.
24. ``DocManager``:
    1. Extend functionality to ``.odt`` files (Libra Office's Writer file format).
    2. Extend functionality to ``.pages`` files (Apple's Pages file format).
25. ``PathManager``:
    1. Edge cases.
        1. Ensure ``PathManager`` handles cases where the provided path already includes Year/Month/Day to prevent redundant nesting and recursive path creation. 