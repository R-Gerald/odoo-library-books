# Odoo 17 – Module `library_book`

This repository contains a custom Odoo 17 module used to learn and practice Odoo development (backend + frontend with OWL).

The module implements a small **library management** example with:

- custom models,
- menus and views,
- security rules,
- server actions using the ORM,
- inheritance of standard models (`crm.lead`, `res.partner`),
- and an **OWL dashboard (client action)** that calls the Odoo ORM from the frontend.

## Features

### 1. Custom application "Bibliothèque"

- New top menu **Bibliothèque**.
- Sub-menus:
  - **Dashboard** (OWL client action),
  - **Livres** (`library.book`),
  - **Catégories** (`library.book.category`).

### 2. Models

#### `library.book`
Represents a book:

- `name` (Char): title (required),
- `author` (Char): author,
- `published_date` (Date): publication date,
- `is_available` (Boolean): availability,
- `category_id` (Many2one → `library.book.category`): category.

Server actions:

- `action_mark_unavailable`: mark selected books as unavailable.
- `action_test_orm`: demo of ORM usage (`create`, `search_count`) with logging.
- `action_mark_all_unavailable`: mark all books in the DB as unavailable.
- `action_delete_unavailable`: delete all unavailable books.

#### `library.book.category`
Represents a book category:

- `name` (Char),
- `description` (Text),
- `book_count` (Integer, computed): total number of books in the category,
- `available_book_count` (Integer, computed): number of available books.

Smart button:

- Opens a filtered list/form view of books belonging to this category.

### 3. Inheritance of standard models

#### `crm.lead`
- `_inherit = 'crm.lead'`.
- Adds:
  - `project_type` (Selection): small / medium / big project.
- View inheritance:
  - Inserts the field into the standard CRM form via `inherit_id="crm.crm_lead_view_form"` and `xpath`.

#### `res.partner`
- `_inherit = 'res.partner'`.
- Adds:
  - `library_book_ids` (Many2many → `library.book`): books “borrowed” by the partner.
- Business constraint:
  - `@api.constrains('library_book_ids')` prevents linking books that are not available (`is_available=False`), raises a `ValidationError`.

### 4. Views and security

- List and form views for `library.book` and `library.book.category`.
- Buttons in the book form header to trigger server actions.
- Smart button on categories with a counter and action.
- Access rights in `security/ir.model.access.csv` for internal users (`base.group_user`).

### 5. OWL Dashboard (Client Action)

Component: `LibraryDashboard`

- Files:
  - `static/src/components/library_dashboard.js`
  - `static/src/components/library_dashboard.xml`
- Declared in `__manifest__.py` under `web.assets_backend`.
- Registered as a client action in JS via:

  ```js
  registry.category("actions").add("library_book.dashboard_action", LibraryDashboard);