import streamlit as st
import mysql.connector
import datetime


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root",   
    database="email_system"
)

c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS emails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender VARCHAR(100),
    subject VARCHAR(200),
    body TEXT,
    status VARCHAR(50),
    allocated_to VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
conn.commit()

st.title("Email Management System")


with st.form("new_email"):
    sender = st.text_input("Sender")
    subject = st.text_input("Subject")
    body = st.text_area("Body")
    submitted = st.form_submit_button("Add Email")   

    if submitted:
        c.execute("INSERT INTO emails (sender, subject, body, status, allocated_to) VALUES (%s, %s, %s, %s, %s)",
                  (sender, subject, body, "New", "Unassigned"))
        conn.commit()
        st.success("Email added successfully!")


st.subheader("Dashboard")
c.execute("SELECT status, COUNT(*) FROM emails GROUP BY status")
rows = c.fetchall()
for status, count in rows:
    st.write(f"{status}: {count}")


if st.button("Auto Allocate Emails"):
    c.execute("UPDATE emails SET allocated_to='Agent1', status='In-progress' WHERE status='New'")
    conn.commit()
    st.success("Emails auto allocated!")
