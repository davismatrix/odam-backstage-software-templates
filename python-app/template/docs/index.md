# Welcome to Dmatrix ${{ values.app_name }}!

Your app is a small Flask-based web app for managing notes and uploaded PDFs.
-   It’s a lightweight personal note-taking and PDF upload app, with a few demo API endpoints and a greeting route layered in.

# What it does:

-   Serves a homepage at  `/`
    -   Shows all saved notes
    -   Lists uploaded PDF files
-   Allows creating notes via a form at  `/create`
-   Allows deleting notes via  /delete/<note_id>
-   Allows uploading PDF files via  `/upload`
-   Allows downloading files via  /download/<filename>
-   Has a simple greeting route at  /greet/<name>
-   Exposes JSON APIs:
    -   /api/v1/details
    -   `/api/v1/healthz`

## Technical details:

-   Uses Flask
-   Uses Flask-SQLAlchemy with SQLite (notes.db)
-   Stores notes in a  Note  table with:
    -   id
    -   title
    -   content
-   Uploads are saved to the  t4s  folder
-   Only PDF files are allowed
-   Runs on:
    -   host:  `0.0.0.0`
    -   port:  `5001`
    -   debug mode: enabled