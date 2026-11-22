# libary\_system\_hasan\_ghassan

&#x20;Markdown

\# Library Management System



A \*\*Library Management System\*\* built with \*\*Streamlit\*\*, \*\*Pandas\*\*, and \*\*Plotly\*\* to manage a book catalog, track 14-day checkouts and check-ins, monitor overdue items, and import/export inventory data via CSV.



\## Features



\- \*\*Home Dashboard:\*\* Displays summary metrics (\*\*Total Books\*\*, \*\*Available\*\*, \*\*Checked Out\*\*, and \*\*Overdue\*\*), an interactive \*\*Plotly\*\* donut/pie breakdown of catalog status, a \*\*Circulation Snapshot\*\* card, overdue alerts, and a table of currently checked-out books.

\- \*\*Add Book:\*\* Form to add new books with \*\*Title\*\*, \*\*Author\*\*, \*\*Genre\*\* (`Sci-fi`, `Romance`, `Fantasy`, `Horror`, `Historical Fiction`, `Thriller`), \*\*ISBN\*\*, and initial \*\*Status\*\* (`Available` or `Checked Out`), saving updates to session state and `books.csv`, with a confirmation dialog.

\- \*\*Check-in / Check-out:\*\* Search by book title or ISBN, check out available books with an automatic \*\*14-day loan period\*\* (`checkout\_date` and `due\_date`), view overdue status, and check books back in while resetting loan dates.

\- \*\*Search Catalog:\*\* Filter books by title or author and narrow results by availability (`All`, `Available`, `Checked Out`).

\- \*\*View Inventory \& CSV Import/Export:\*\* View full catalog metrics and data, upload a CSV file to replace/update session data and save to `books.csv`, and download the current inventory as `books\_inventory.csv`.



\## Project Structure



```text

libary\_system\_hasan\_ghassan/

├── ga\_pro1/

│   └── project1-hasan\_ghassan.py   # Main Streamlit application

└── requirements.txt               # Python dependencies (streamlit, pandas, plotly)



deploy link i think:

https://libarysystemhasanghassan-hkxkpztvj8nwnrhgjvwiur.streamlit.app/



google drive link: 

https://drive.google.com/drive/folders/1cTLnLjYjsEkcH60EkV9iuz2-gjCBVmVI?usp=sharing

