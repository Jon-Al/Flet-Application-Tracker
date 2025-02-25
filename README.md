### Roadmap of Future Development

1. Enable link replacement
2. Enable On-Off placeholders
3. Enable Multi-level Placeholders
4. Enable a methodology to extract various keywords from job postings.
5. Enable 'history' of sorts - allow to pick from past values.
6. Expand on use of variable, tags.
7. Add communication tracking.
8. Add contacts.
9. Improve the consistency of placeholders' behaviour.
10. _Done_ ~~Add a ``requirments.txt``~~
11. Use [Black](https://github.com/psf/black) for code formatting (as advised by [Flet](https://flet.dev/)'s official dev team)
12. Improve the visual presentation in the app.
13. Deploy on GitHub pages (or elsewhere).
14. Extend functionality to ``.odt`` (Libra Office's Writer file format)
15. Extend functionality to ``.pages`` (Apple's Pages file format)

### Current features _(partial list)_

1. Placeholders names ``position`` can be replaced automatically, using the values from the drop-down menu in the appropriate window.
2. Auto-increments file names if the name already exists (in the ``docs\Applications`` folder).
3. Automatically prepends the creation date to older PDFs file names if there's a conflict with a new pdf.
4. Automatically fills in the last used templates.
5. Placeholders with identical labels are treated as identical, allowing you to save time by re-using common placeholders (see ``position`` above).
6. Where a placeholder spans multiple Runs, formatting will be based on the first Run in the group.
    1. a Run is the main structure of ``docx`` files.

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

### On-Off Placeholders

Once implemented, these will allow dynamic use of a [Flet](https://flet.dev/) [Switch](https://flet.dev/docs/controls/switch/) to remove entire sections of the text.

### Multi-level Placeholders

Once implemented, these will enable nesting, where one placeholder can resolve into another, allowing for structured replacements.

### Other Useful Information

Feedback is welcome; please use "Feedback: Flet_Application_Tracker" in your email's subject. [JASoftware@proton.me](mailto:JASoftware@proton.me) _Feedback welcome!_

### Related Links

* [Felt GitHub repository](https://github.com/flet-dev/flet)
* [Flet website](https://flet.dev/)