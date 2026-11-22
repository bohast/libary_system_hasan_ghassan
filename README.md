# libary\_system\_hasan\_ghassan


Library Management System

A Library Management System built with Streamlit, Pandas, and Plotly to manage a book catalog, track 14-day checkouts and check-ins, monitor overdue items, and import/export inventory data via CSV.

Features

Home Dashboard: Displays summary metrics (Total Books, Available, Checked Out, and Overdue), an interactive Plotly donut/pie breakdown of catalog status, a Circulation Snapshot card, overdue alerts, and a table of currently checked-out books.

Add Book: Form to add new books with Title, Author, Genre (Sci-fi, Romance, Fantasy, Horror, Historical Fiction, Thriller), ISBN, and initial Status (Available or Checked Out), saving updates to session state and books.csv, with a confirmation dialog.

Check-in / Check-out: Search by book title or ISBN, check out available books with an automatic 14-day loan period (checkout_date and due_date), view overdue status, and check books back in while resetting loan dates.

Search Catalog: Filter books by title or author and narrow results by availability (All, Available, Checked Out).

View Inventory & CSV Import/Export: View full catalog metrics and data, upload a CSV file to replace/update session data and save to books.csv, and download the current inventory as books_inventory.csv.

Project Structure
libary_system_hasan_ghassan/
├── ga_pro1/
│   └── project1-hasan_ghassan.py
└── requirements.txt

Work Completed

Built the multi-page Streamlit application (Home, Add Book, Check-in/Check-out, Search Catalog, and View Inventory) with custom CSS styling for metric and summary cards.

Implemented persistent session state (st.session_state.books_df) backed by books.csv, including automatic handling for checkout_date and due_date columns.

Added 14-day loan due-date calculation on checkout, date resetting on check-in, and overdue book detection alerts.

Integrated a Plotly status breakdown chart and circulation percentage summary on the Home page, alongside CSV upload and download functionality.

Added requirements.txt with streamlit, pandas, and plotly for deployment on Streamlit Community Cloud and resolved pandas timestamp comparison typing (TypeError) during overdue date checks.

Running Locally

Install dependencies:
pip install -r requirements.txt

Run the Streamlit app:
streamlit run ga_pro1/project1-hasan_ghassan.py


deploy link i think:

https://libarysystemhasanghassan-hkxkpztvj8nwnrhgjvwiur.streamlit.app/



google drive link: 

https://drive.google.com/drive/folders/1cTLnLjYjsEkcH60EkV9iuz2-gjCBVmVI?usp=sharing

