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
| A\_1              | Creation of Use Case             |
| A\_2              | Editing Use Case                 |
| A\_3              | Deleting Use Case                |
| A\_4              | Publishing/retracting Use Case   |

Coverage matrix:

| AId  | 1     | 2     | 3     | 4     | 5     | 6     | 7     |
|------|-------|-------|-------|-------|-------|-------|-------|
| P\_1 | x     | ----- | ----- | x     | x     | x     | x     |
| P\_2 | ----- | x     | x     | x     | x     | x     | x     |
| P\_3 | x     | x     | x     | ----- | ----- | ----- | x     |
| A\_1 | ----- | x     | x     | ----- | ----- | ----- | ----- |
| A\_2 | ----- | ----- | ----- | ----- | ----- | ----- | x     |
| A\_3 | ----- | ----- | ----- | ----- | ----- | x     | ----- |
| A\_4 | ----- | ----- | ----- | x     | x     | ----- | ----- |


## Feature-Test matrix

| Feature file      | 1   | 2   | 3   | 4   | 5   | 6   | 7   |
|-------------------|-----|-----|-----|-----|-----|-----|-----|
| use_cases.feature | x   | x   | x   | x   | x   | x   | x   |


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
