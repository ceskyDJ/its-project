# ITS Project 1

- **Author:** Michal Šmahel (xsmahe01)
- **Date:** 2022-04-17

## Artifacts coverage matrix

| Artifact Id (AId) | Artifact Description             |
|-------------------|----------------------------------|
| P\_1              | Web page with Use Cases          |
| P\_2              | Web page with Use Case detail    |
| P\_3              | Web page with Use Case edit form |
| P\_4              | Web page with Tools              |
| P\_5              | Web page with Tool detail        |
| P\_6              | Web page with Tool edit form     |
| P\_7              | Web page with Methods            |
| P\_8              | Web page with Method detail      |
| P\_9              | Web page with Method edit form   |
| A\_1              | Creation of Use Case             |
| A\_2              | Editing Use Case                 |
| A\_3              | Deleting Use Case                |
| A\_4              | Publishing/retracting Use Case   |
| A\_5              | Creation of Tool                 |
| A\_6              | Publishing/retracting Tool       |
| A\_7              | Reviewing Tool for submit        |
| A\_8              | Creation of Method               |
| A\_9              | Editing Method                   |

Coverage matrix:

| AId  | 1     | 2     | 3     | 4     | 5     | 6     | 7     | 8     | 9     | 10    | 11    | 12    | 13    | 14    | 15    |
|------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| P\_1 | x     | ----- | ----- | x     | x     | x     | x     | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| P\_2 | ----- | x     | x     | x     | x     | x     | x     | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| P\_3 | x     | x     | x     | ----- | ----- | ----- | x     | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| P\_4 | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | x     | x     | x     | ----- | ----- | ----- | ----- |
| P\_5 | ----- | ----- | ----- | ----- | ----- | ----- | ----- | x     | x     | x     | x     | ----- | ----- | ----- | ----- |
| P\_6 | ----- | ----- | ----- | ----- | ----- | ----- | ----- | x     | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| P\_7 | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | x     | ----- | ----- |
| P\_8 | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | x     | x     | ----- | ----- |
| P\_9 | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | x     | x     | x     | x     |
| A\_1 | ----- | x     | x     | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| A\_2 | ----- | ----- | ----- | ----- | ----- | ----- | x     | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| A\_3 | ----- | ----- | ----- | ----- | ----- | x     | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| A\_4 | ----- | ----- | ----- | x     | x     | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| A\_5 | ----- | ----- | ----- | ----- | ----- | ----- | ----- | x     | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| A\_6 | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | x     | ----- | ----- | ----- | ----- | ----- | ----- |
| A\_7 | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | x     | x     | ----- | ----- | ----- | ----- |
| A\_8 | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | x     | ----- | x     | x     |
| A\_9 | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | x     | ----- | ----- |


## Feature-Test matrix

| AId               | 1     | 2     | 3     | 4     | 5     | 6     | 7     | 8     | 9     | 10    | 11    | 12    | 13    | 14    | 15    |
|-------------------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| use_cases.feature | x     | x     | x     | x     | x     | x     | x     | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| tools.feature     | ----- | ----- | ----- | ----- | ----- | ----- | ----- | x     | x     | x     | x     | ----- | ----- | ----- | ----- |
| methods.feature   | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | x     | x     | x     | x     |


## Found (possible) bugs (not part of the ITS project)

### Empty BUT's creator page

- Log in as user with admin privileges ("itsadmin" for example).
- Go to page "Organizations".
- Click on the "BUT" in the "Creator" column in the shown table.
- Empty page is displayed (http://localhost:8080/repo/author/BUT).

But for "administrator" account it correctly displays page with latest created content:

- Log in as user with admin privileges ("itsadmin" for example).
- Go to page "Methods".
- Click on the "administrator" in the underline comment under the heading "Method":
"by administrator -- last modified ...".
- Correct page that contains contributions of user "administrator" is displayed.

### Invalid descriptions of inputs in Add Tool --> Ownership

- Log in as user with admin privileges ("itsadmin" for example).
- Open "Add Tool" form.
- Go to "Ownership" tab.
- "Creators" input field has invalid part of description: "Please enter a list of usernames,
one per line." - the input doesn't allow multiline content, it's based on selection
of the values from search box displayed after typing something into the "Creators" input field.
- "Contributors" input field contains similar sentence - "Each contributor should be on
a separate line." but works similarly to the "Creators" input field.

### Missing type checking for drag-n-drop input fields

- Log in as user with admin privileges ("itsadmin" for example).
- Open "Add method" form (but it is in every form that contains drag-n-drop fields).
- Go to "Relations" tab.
- Choose some item in "Tools" field.
- Choose some item in "Standards" field.
- Move chosen item from "Tools" to "Standards". It mostly must be tried more than once, but
it could be done. Tried on desktop and mobile, both platforms allow this. This shouldn't be
possible, some check for type of dropped item is missing.
- There is an inconsistency - tool is in "Standards" field.
- Click "Save" button.
- **No error message** is showed.
- Added method's detail is displayed and here is everything ok.

### Redundant filter item in "Methods" page

- Have no Method with "Type of Component Under Evaluation" set to "Model".
- Go to page "Methods".
- There is a "Model" item in filter named "Type Of Component Under Evaluation Dimension".
This item isn't select any Method, because no Method has it set.

### No input field for reject reason of submit request

- Log in as user with at least reviewer privileges ("itsreviewer" for example).
- Find some Tool in state "Pending review".
- In menu --> "State: Pending review" move mouse above "Send back".
- Shown tooltip contains: "You should preferably include a reason for why it was not
published.". There is no input field for entering reason. After you click on "Send
back", it just changes the state of the Tool, no dialog/form is displayed for entering
reason.

### Unhandled exception for cutting and pasting some tool

- Log in as user with admin privileges ("itsadmin" for example).
- Go to the detail of some Tool.
- In menu --> "Actions" click on "Cut".
- In menu --> "Actions" click on "Paste".
- Unhandled exception is thrown and page contains information about it (see below).

Error message: "Disallowed subobject type: tool"

Exception details:
```
Traceback (innermost last):
  Module ZPublisher.WSGIPublisher, line 162, in transaction_pubevents
  Module ZPublisher.WSGIPublisher, line 359, in publish_module
  Module ZPublisher.WSGIPublisher, line 262, in publish
  Module ZPublisher.mapply, line 85, in mapply
  Module ZPublisher.WSGIPublisher, line 63, in call_object
  Module plone.app.content.browser.actions, line 252, in __call__
  Module plone.app.content.browser.actions, line 315, in do_action
  Module plone.app.content.browser.actions, line 221, in do_redirect
ValueError: Disallowed subobject type: tool
```

### "Clear" and "Today" buttons don't close opened dropdown menus of fields in Publishing process

- Log in as user with admin privileges ("itsadmin" for example).
- Open detail of some Tool.
- In menu --> "State: XXX" click on "Advanced...".
- In dialog window click on "Enter date..." field and on "Enter time..." field.
- Dropdown menus of "Enter date..." and "Enter time..." input fields are visible.
- Click on Today or Clear button. Maybe click outside, too?
- Dropdown menus of "Enter date..." and "Enter time..." input fields are still visible. They could be hidden.

### Delayed publishing changes the state immediately

- Log in as user with admin privileges ("itsadmin" for example).
- Open detail of some Tool with state "Private".
- In menu --> "State: XXX" click on "Advanced...".
- Fill in future date as "Publishing date".
- Set "Change State" to "Publish".
- Click on "Save".
- It closes the dialog windows and immediately sets the Tool as "Published". It should not do that, because
some date in the future was specified for this event.
