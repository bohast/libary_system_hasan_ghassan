import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta # all the imports

#this is for setting up the page title, icon, and wide layout
st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide",
)

#this block of code is for styling the metric boxes and status card on the home page
st.markdown(
    """
    <style>
        div[data-testid="stMetric"] {
            background-color: rgba(128, 128, 128, 0.06);
            border: 1px solid rgba(128, 128, 128, 0.16);
            padding: 14px 18px;
            border-radius: 12px;
        }
        .status-card {
            background-color: rgba(128, 128, 128, 0.05);
            border: 1px solid rgba(128, 128, 128, 0.15);
            border-radius: 12px;
            padding: 18px 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

#this block if code is for navagation of menu
with st.sidebar:
    page_chosen = st.radio(
        "MENU",
        ("Home","Add Book", "Check-in/Check-out","Search Catalog","View Inventory")
    )
COLUMNS = ["author", "book", "genre", "isbn", "status"]#this are 

# this code are to help call the due date for the he are checked out books
today = datetime.now().date()
due = today + timedelta(days=14)

#tthis block of code is used o call the csv if it is there and save the data of the session
if "books_df" not in st.session_state:
  try:
    st.session_state.books_df = pd.read_csv("books.csv")
  except FileNotFoundError:
    st.session_state.books_df = pd.DataFrame(columns=COLUMNS)
    st.divider()
    st.subheader("CSV Import & Export")
    col_up, col_dl = st.columns(2)
    with col_up:
      uploaded_file = st.file_uploader(
          "Upload a books CSV to replace current session data", type="csv"
      )
      if uploaded_file is not None:
        uploaded_df = pd.read_csv(uploaded_file)
#this is to make sure checkout_date and due_date columns exist in uploaded csv
        for col in ["checkout_date", "due_date"]:
          if col not in uploaded_df.columns:
            uploaded_df[col] = ""
          else:
            uploaded_df[col] = uploaded_df[col].fillna("").astype("object")

        st.session_state.books_df = uploaded_df
        uploaded_df.to_csv("books.csv", index=False)
        st.success("Uploaded CSV into session and saved to `books.csv`.")
        st.rerun()
#this code is for downloading the csv
    with col_dl:
      csv_bytes = (
          st.session_state.books_df.to_csv(index=False).encode("utf-8")
      )
      st.download_button(
          label="Download Current Inventory (CSV)",
          data=csv_bytes,
          file_name="books_inventory.csv",
          mime="text/csv",
      )

#this loop is to make sure checkout_date and due_date columns are always in the session table
for col in ["checkout_date", "due_date"]:
  if col not in st.session_state.books_df.columns:
    st.session_state.books_df[col] = pd.Series(dtype="object")
  else:
    st.session_state.books_df[col] = (
        st.session_state.books_df[col].fillna("").astype("object")
    )
#this is for due alerts if book are not on due date
df_alerts = st.session_state.books_df
if not df_alerts.empty and "due_date" in df_alerts.columns:
  parsed_due = pd.to_datetime(df_alerts["due_date"], errors="coerce").dt.normalize()
  today_ts = pd.Timestamp.now().normalize()
  overdue_books = df_alerts[
      (df_alerts["status"] == "Checked Out")
      & parsed_due.notna()
      & (parsed_due < today_ts)
  ]
  if not overdue_books.empty:
    overdue_titles = ", ".join(overdue_books["book"].astype(str).tolist())
    st.error(
        f"**Overdue Alert:** {len(overdue_books)} book(s) past due date — "
        f"**{overdue_titles}**"
    )
#this for pop up after book beaing add
@st.dialog("Book Added Successfully")
def show_book_popup(book_details: dict):
  st.write("Here are the details of the book you just added:")
  st.markdown(f"""
    - **Title:** {book_details['book']}
    - **Author:** {book_details['author']}
    - **Genre:** {book_details['genre']}
    - **ISBN:** {book_details['isbn']}
    - **Status:** {book_details['status']}
    """)
  if st.button("Close"):
    st.rerun()
#this function is to build the pie chart for available, checked out, and overdue books
def build_status_pie_chart(available: int, on_time_checked_out: int, overdue: int) -> go.Figure:
    labels = ["Available", "Checked Out (On Time)", "Overdue"]
    values = [available, on_time_checked_out, overdue]
    colors = ["#10B981", "#3B82F6", "#EF4444"] #this is for the slice colors (green, blue, red)

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.45,  # bigger hole the bigger numberset to 0 for a classic solid pie chart
                marker=dict(
                    colors=colors,
                    line=dict(color="#111827", width=2),
                ),
                textinfo="percent+value",
                textfont=dict(size=13, color="#FFFFFF"),
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Books: %{value}<br>"
                    "Share: %{percent}<extra></extra>"
                ),
            )
        ]
    )
#this is for setting the chart title, legend position, and transparent background
    fig.update_layout(
        title=dict(
            text="Catalog Status Breakdown",
            font=dict(size=18),
            x=0.02,
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.18,
            xanchor="center",
            x=0.5,
            font=dict(size=13),
        ),
        margin=dict(t=55, b=60, l=20, r=20),
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig
#this the home page layout
if page_chosen == "Home":
    st.title("📚 Library Management System")
    st.caption("Overview of catalog availability, active loans, and overdue items.")

    df = st.session_state.books_df
    if df.empty:
        st.info("Your library is empty. Switch to 'Add Book' to add your first title.")
    else:
        total_books = len(df)#this is to count total, available, checked out, and overdue books
        available_count = int((df["status"] == "Available").sum())
        total_checked_out = int((df["status"] == "Checked Out").sum())
        overdue_count = len(overdue_books)
        on_time_checked_out = max(total_checked_out - overdue_count, 0)
#this is to show the 4 metric cards at the top of home page
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Books", total_books)
        c2.metric("Available", available_count)
        c3.metric("Checked Out", total_checked_out)
        c4.metric("Overdue", overdue_count, delta_color="inverse")

        st.divider()
#this block of code is to place the pie chart and summary card side by side
        chart_col, summary_col = st.columns([1.25, 1])

        with chart_col:
            pie_fig = build_status_pie_chart(
                available=available_count,
                on_time_checked_out=on_time_checked_out,
                overdue=overdue_count,
            )
            st.plotly_chart(pie_fig, use_container_width=True)

        with summary_col:
            avail_pct = (available_count / total_books) * 100 if total_books else 0
            ontime_pct = (on_time_checked_out / total_books) * 100 if total_books else 0
            overdue_pct = (overdue_count / total_books) * 100 if total_books else 0
#this is for displaying the circulation snapshot box next to the chart
            st.markdown(
                f"""
                <div class="status-card">
                    <h4 style="margin-top:0;">data info</h4>
                    <p style="margin: 10px 0;">🟢 <b>Available:</b> {available_count} ({avail_pct:.1f}%)</p>
                    <p style="margin: 10px 0;">🔵 <b>Checked Out (On Time):</b> {on_time_checked_out} ({ontime_pct:.1f}%)</p>
                    <p style="margin: 10px 0;">🔴 <b>Overdue:</b> {overdue_count} ({overdue_pct:.1f}%)</p>
                    <hr style="opacity:0.2;">
                    <p style="margin-bottom:0; font-size:0.9rem; opacity:0.85;">
                        Standard loan period: <b>14 days</b>
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
#this section is for showing the table of books that are currently checked out
        st.divider()
        st.subheader("Currently Checked Out")
        checked_out_df = df[df["status"] == "Checked Out"]
        if checked_out_df.empty:
            st.write("No books are currently checked out.")
        else:
            cols = [
                c
                for c in ["book", "author", "borrower", "checkout_date", "due_date"]
                if c in checked_out_df.columns
            ]
            st.dataframe(checked_out_df[cols], use_container_width=True, hide_index=True)
#this is the add book page layout
if page_chosen == "Add Book":
    st.title("Adding Books")#this form is used to get new book details from the user
    with st.form("add_book_form", clear_on_submit=True):
        author = st.text_input("Author name").strip()
        book = st.text_input("Book title").strip()
        genre = st.selectbox(
            "Genre",
        [
            "Sci-fi",
            "Romance",
            "Fantasy",
            "Horror",
            "Historical Fiction",
            "Thriller",
        ],
        )
        isbn = int(st.number_input("ISBN number", min_value=0, step=1))
        status = st.radio(
            "Current status",
            ["Available", "Checked Out"],
            index=0,
        )
        submitted = st.form_submit_button("Add Book")
    #this is for saving the new book to the dataframe and csv when submitted
    if submitted:
        if not author or not book:
            st.warning("Please enter both a book title and an author.")
        else:
            book_details = {
                "author": author,
                "book": book,
                "genre": genre,
                "isbn": isbn,
                "status": status,
            }
            new_row = pd.DataFrame([book_details])
            st.session_state.books_df = pd.concat(
                [st.session_state.books_df, new_row], ignore_index=True
            )
            st.session_state.books_df.to_csv("books.csv", index=False)
            show_book_popup(book_details)

#this is the check-in and check-out page layout
if page_chosen == "Check-in/Check-out":
    st.title("Check-in/Check-out Page")
    df = st.session_state.books_df
    if df.empty:
        st.info("No books in the catalog yet. Add a book first.")
    else:#this is for searching the book by title or isbn before checking in/out
        query = (
            st.text_input("Search by book title or ISBN").strip().lower()
        )
        if query:
            mask = df["book"].astype(str).str.lower().str.contains(
                query, na=False
            ) | df["isbn"].astype(str).str.lower().str.contains(query, na=False)
            matches = df[mask]
        else: #this is to let the user pick a book from the matching results
            matches = df
        if matches.empty:
            st.warning("No matching books found.")
        else:
            options = {
                f"{row['book']} — ISBN: {row['isbn']} ({row['status']})": idx
                for idx, row in matches.iterrows()
            }
            selected_label = st.selectbox("Select a book", list(options.keys()))
            book_idx = options[selected_label]
            current_status = df.loc[book_idx, "status"]
            st.write(f"**Current Status:** {current_status}")
            if current_status == "Checked Out" and df.loc[book_idx, "due_date"]:
                st.write(f"**Due Date:** {df.loc[book_idx, 'due_date']}")
            if current_status == "Available":
            #this block is for checking out an available book for 14 days
              if st.button("Check Out Book (14-Day Loan)", type="primary"):
                  today = datetime.now().date()
                  due = today + timedelta(days=14)
                  st.session_state.books_df.loc[book_idx, "status"] = ("Checked Out")
                  st.session_state.books_df.loc[book_idx, "checkout_date"] = (today.isoformat())
                  st.session_state.books_df.loc[book_idx, "due_date"] = (due.isoformat())
                  st.session_state.books_df.to_csv("books.csv", index=False)
                  st.success(f"Checked out! Due back on **{due.isoformat()}**.")
                  st.rerun()
              else:
                  due_str = str(df.loc[book_idx, "due_date"]).strip()
                  if due_str:
                      try:
                          due_dt = datetime.strptime(due_str, "%Y-%m-%d").date()
                          today = datetime.now().date()
                          if today > due_dt:
                              days_late = (today - due_dt).days
                              st.warning(f"This book was due on **{due_dt.isoformat()}** (overdue"f" by **{days_late}** day(s)).")
                      except ValueError:
                          pass
            else: #this block is for checking a book back in and resetting its dates
                if st.button("Check In Book", type="primary"):
                    st.session_state.books_df.loc[book_idx, "status"] = "Available"
                    st.session_state.books_df.loc[book_idx, "checkout_date"] = ""
                    st.session_state.books_df.loc[book_idx, "due_date"] = ""
                    st.session_state.books_df.to_csv("books.csv", index=False)
                    st.success("Book checked in and marked as **Available**.")
                    st.rerun()

#this is the search catalog page layout
if page_chosen == "Search Catalog":
    st.title("Search Catalog")
    df = st.session_state.books_df
    if df.empty:
        st.info("No books in the catalog yet. Add a book first.")
    else:#this is for the search bar and availability filter dropdow
        col1, col2 = st.columns([3, 1])
        with col1:
            search_query = (st.text_input("Search by book title or author").strip().lower())
        with col2:
            status_filter = st.selectbox(
                "Availability", ["All", "Available", "Checked Out"])
            filtered = df.copy()
        if search_query:#this is to filter the table based on title, author, and status
            title_match = (filtered["book"].astype(str).str.lower().str.contains(search_query, na=False))
            author_match = (
                filtered["author"].astype(str).str.lower().str.contains(search_query, na=False))
            filtered = filtered[title_match | author_match]
        if status_filter != "All":
            filtered = filtered[filtered["status"] == status_filter]
        if filtered.empty:
            st.warning("No books match your search.")
        else:
            st.caption(f"Showing {len(filtered)} book(s)")
            display_cols = [c for c in ["book", "author", "genre", "isbn", "status", "due_date"]
                            if c in filtered.columns]
            st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True)
 #this is the view inventory page layout   
if page_chosen == "View Inventory":
    st.title("Library Inventory")
    df = st.session_state.books_df
    if df.empty:
        st.info("Your inventory is currently empty.")
    else:
        total_books = len(df)#this is to show total, available, and checked out counts above the full table
        available_count = int((df["status"] == "Available").sum())
        checked_out_count = int((df["status"] == "Checked Out").sum())
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Books", total_books)
        m2.metric("Available", available_count)
        m3.metric("Checked Out", checked_out_count)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.divider()
        st.subheader("CSV Import & Export")#this block of code is for uploading a new csv or downloading the current inventory
        col_up, col_dl = st.columns(2)
        with col_up:
            uploaded_file = st.file_uploader("Upload a books CSV to replace current session data", type="csv")
            if uploaded_file is not None:
                uploaded_df = pd.read_csv(uploaded_file)
                for col in ["checkout_date", "due_date"]:
                    if col not in uploaded_df.columns:
                        uploaded_df[col] = ""
                    else:
                        uploaded_df[col] = uploaded_df[col].fillna("").astype("object")
                st.session_state.books_df = uploaded_df
                uploaded_df.to_csv("books.csv", index=False)
                st.success("Uploaded CSV into session and saved to `books.csv`.")
                st.rerun()
#this code is for downloading the current inventory as a csv file
        with col_dl:
            csv_bytes = (st.session_state.books_df.to_csv(index=False).encode("utf-8"))
            st.download_button(
                label="Download Current Inventory (CSV)",
                data=csv_bytes,
                file_name="books_inventory.csv",
                mime="text/csv",
            )

    
