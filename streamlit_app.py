import streamlit as st
import sqlite3
import threading
import time
import random
from pathlib import Path
from datetime import datetime

# =========================================================
# HOSTELFLOW | HOSTEL ROOM & BED ALLOCATION SYSTEM
# =========================================================

st.set_page_config(
    page_title="HOSTELFLOW | Smart Hostel Management",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_PATH = Path(__file__).parent / "hostelflow.db"
ALLOCATION_LOCK = threading.Lock()

# =========================================================
# PREMIUM UI DESIGN
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #080e1c;
    --panel: #101a2d;
    --panel2: #142139;
    --cyan: #37e6f5;
    --blue: #5795ff;
    --muted: #91a4c1;
    --white: #f2f7ff;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, rgba(31,91,155,.22), transparent 35%),
        radial-gradient(ellipse at 90% 20%, rgba(0,200,220,.10), transparent 30%),
        #080e1c;
    color: var(--white);
    font-family: 'DM Sans', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101b30, #091222);
    border-right: 1px solid rgba(90,160,220,.16);
}

[data-testid="stSidebar"] * {
    color: #e8f2ff;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #f4f8ff !important;
}

p, label, span, div {
    font-family: 'DM Sans', sans-serif;
}

.hero {
    padding: 30px 34px;
    border-radius: 22px;
    background: linear-gradient(115deg, rgba(20,48,79,.96), rgba(12,27,48,.95));
    border: 1px solid rgba(55,230,245,.22);
    box-shadow: 0 15px 55px rgba(0,0,0,.22);
    position: relative;
    overflow: hidden;
    margin-bottom: 25px;
}

.hero:after {
    content: "";
    position: absolute;
    width: 260px;
    height: 260px;
    right: -75px;
    top: -120px;
    border-radius: 50%;
    background: rgba(55,230,245,.10);
    filter: blur(3px);
}

.hero-tag {
    color: #53e8f2;
    letter-spacing: 3px;
    font-size: 11px;
    font-weight: 800;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 38px;
    font-weight: 800;
    margin: 9px 0 5px;
    color: #ffffff;
}

.hero-sub {
    color: #a9bdd7;
    font-size: 14px;
}

.stat-card {
    background: linear-gradient(145deg, #14243c, #0e192c);
    border: 1px solid rgba(117,165,220,.15);
    padding: 20px;
    border-radius: 17px;
    min-height: 125px;
    box-shadow: 0 8px 28px rgba(0,0,0,.15);
    transition: .25s ease;
}

.stat-card:hover {
    transform: translateY(-4px);
    border-color: rgba(55,230,245,.55);
}

.stat-label {
    font-size: 12px;
    color: #9bb0cc;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-weight: 700;
}

.stat-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 32px;
    font-weight: 800;
    color: #f5f9ff;
    margin-top: 9px;
}

.stat-foot {
    font-size: 11px;
    color: #48dce9;
    margin-top: 3px;
}

.section-label {
    color: #4fe2ef;
    letter-spacing: 2px;
    font-size: 11px;
    font-weight: 800;
    margin-bottom: 7px;
}

.panel {
    background: rgba(17,29,49,.90);
    border: 1px solid rgba(119,164,215,.15);
    border-radius: 17px;
    padding: 22px;
    margin-bottom: 18px;
}

.bed {
    border-radius: 12px;
    padding: 13px 7px;
    text-align: center;
    margin: 5px 0;
    font-weight: 700;
    font-size: 12px;
}

.bed-free {
    background: rgba(45,211,151,.13);
    border: 1px solid rgba(45,211,151,.45);
    color: #6cf0bb;
}

.bed-taken {
    background: rgba(255,91,112,.12);
    border: 1px solid rgba(255,91,112,.4);
    color: #ff8797;
}

.bed-demo {
    background: rgba(55,230,245,.12);
    border: 1px solid rgba(55,230,245,.45);
    color: #62eff5;
}

.status-pill {
    display: inline-block;
    padding: 5px 11px;
    border-radius: 30px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .5px;
}

.pill-green {
    color: #64eab6;
    background: rgba(45,211,151,.12);
}

.pill-red {
    color: #ff8797;
    background: rgba(255,91,112,.12);
}

.pill-blue {
    color: #6debf5;
    background: rgba(55,230,245,.12);
}

div.stButton > button {
    background: linear-gradient(100deg, #1db9d1, #397df0);
    color: white;
    border: 0;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: 800;
    transition: .2s;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(39,190,230,.25);
    color: white;
    border: 0;
}

div[data-testid="stMetric"] {
    background: #132139;
    border: 1px solid rgba(100,160,220,.15);
    padding: 16px;
    border-radius: 14px;
}

[data-testid="stMetricValue"] {
    color: #55e6f2;
    font-family: 'Space Grotesk', sans-serif;
}

.stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
    background-color: #111f35;
    color: white;
    border-radius: 9px;
}

.stProgress > div > div {
    background: linear-gradient(90deg, #1ec9d6, #4e8dff);
}

hr {
    border-color: rgba(110,160,210,.15);
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# DATABASE
# =========================================================

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            block TEXT NOT NULL,
            floor INTEGER NOT NULL,
            room_number TEXT NOT NULL,
            UNIQUE(block, room_number)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS beds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER NOT NULL,
            bed_number TEXT NOT NULL,
            FOREIGN KEY(room_id) REFERENCES rooms(id),
            UNIQUE(room_id, bed_number)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            roll_number TEXT NOT NULL UNIQUE,
            department TEXT NOT NULL,
            year INTEGER NOT NULL,
            phone TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS allocations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            bed_id INTEGER NOT NULL,
            allocated_at TEXT NOT NULL,
            checkout_at TEXT,
            status TEXT NOT NULL DEFAULT 'Active',
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(bed_id) REFERENCES beds(id)
        )
    """)

    conn.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS one_active_allocation_per_bed
        ON allocations(bed_id) WHERE status = 'Active'
    """)

    conn.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS one_active_allocation_per_student
        ON allocations(student_id) WHERE status = 'Active'
    """)

    conn.commit()

    # Create initial hostel structure once.
    room_count = conn.execute("SELECT COUNT(*) FROM rooms").fetchone()[0]

    if room_count == 0:
        blocks = {
            "BLOCK A": 3,
            "BLOCK B": 2,
            "BLOCK C": 2
        }

        for block, floors in blocks.items():
            for floor in range(1, floors + 1):
                for room_num in range(1, 5):
                    room_number = f"{floor}{room_num:02d}"

                    cursor = conn.execute(
                        "INSERT INTO rooms (block, floor, room_number) VALUES (?, ?, ?)",
                        (block, floor, room_number)
                    )

                    room_id = cursor.lastrowid

                    for bed_num in range(1, 5):
                        conn.execute(
                            "INSERT INTO beds (room_id, bed_number) VALUES (?, ?)",
                            (room_id, f"BED-{bed_num}")
                        )

    conn.commit()
    conn.close()


initialize_database()


# =========================================================
# DATABASE HELPERS
# =========================================================

def get_dashboard_stats():
    conn = get_db()

    total_beds = conn.execute("SELECT COUNT(*) FROM beds").fetchone()[0]

    occupied = conn.execute("""
        SELECT COUNT(*) FROM allocations WHERE status = 'Active'
    """).fetchone()[0]

    total_students = conn.execute("""
        SELECT COUNT(*) FROM students
    """).fetchone()[0]

    total_rooms = conn.execute("""
        SELECT COUNT(*) FROM rooms
    """).fetchone()[0]

    conn.close()

    available = total_beds - occupied
    percentage = round((occupied / total_beds) * 100, 1) if total_beds else 0

    return {
        "beds": total_beds,
        "occupied": occupied,
        "available": available,
        "students": total_students,
        "rooms": total_rooms,
        "percentage": percentage
    }


def get_beds():
    conn = get_db()

    rows = conn.execute("""
        SELECT
            b.id AS bed_id,
            b.bed_number,
            r.block,
            r.floor,
            r.room_number,
            CASE
                WHEN a.id IS NULL THEN 'Available'
                ELSE 'Occupied'
            END AS status,
            s.student_name,
            s.roll_number
        FROM beds b
        JOIN rooms r ON b.room_id = r.id
        LEFT JOIN allocations a
            ON a.bed_id = b.id AND a.status = 'Active'
        LEFT JOIN students s ON a.student_id = s.id
        ORDER BY r.block, r.floor, r.room_number, b.bed_number
    """).fetchall()

    conn.close()
    return rows


def get_available_beds():
    return [bed for bed in get_beds() if bed["status"] == "Available"]


def allocate_student(name, roll, department, year, phone, bed_id):
    """
    Critical section:
    Only one thread can check and allocate a bed at a time.
    The database also enforces a unique active allocation per bed.
    """

    with ALLOCATION_LOCK:
        conn = get_db()

        try:
            conn.execute("BEGIN IMMEDIATE")

            existing_student = conn.execute(
                "SELECT id FROM students WHERE roll_number = ?",
                (roll,)
            ).fetchone()

            if existing_student:
                student_id = existing_student["id"]

                active = conn.execute("""
                    SELECT id FROM allocations
                    WHERE student_id = ? AND status = 'Active'
                """, (student_id,)).fetchone()

                if active:
                    conn.rollback()
                    return False, "This student already has an active bed."

                conn.execute("""
                    UPDATE students
                    SET student_name = ?, department = ?, year = ?, phone = ?
                    WHERE id = ?
                """, (name, department, year, phone, student_id))

            else:
                cursor = conn.execute("""
                    INSERT INTO students
                    (student_name, roll_number, department, year, phone)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, roll, department, year, phone))

                student_id = cursor.lastrowid

            occupied = conn.execute("""
                SELECT id FROM allocations
                WHERE bed_id = ? AND status = 'Active'
            """, (bed_id,)).fetchone()

            if occupied:
                conn.rollback()
                return False, "Bed is already occupied. Allocation blocked."

            conn.execute("""
                INSERT INTO allocations
                (student_id, bed_id, allocated_at, status)
                VALUES (?, ?, ?, 'Active')
            """, (student_id, bed_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

            conn.commit()
            return True, "Bed allocated successfully."

        except sqlite3.IntegrityError:
            conn.rollback()
            return False, "Allocation prevented by database safety constraint."

        except Exception as error:
            conn.rollback()
            return False, str(error)

        finally:
            conn.close()


def checkout_student(allocation_id):
    with ALLOCATION_LOCK:
        conn = get_db()

        conn.execute("""
            UPDATE allocations
            SET status = 'Checked Out', checkout_at = ?
            WHERE id = ? AND status = 'Active'
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            allocation_id
        ))

        conn.commit()
        conn.close()


def get_active_allocations():
    conn = get_db()

    rows = conn.execute("""
        SELECT
            a.id AS allocation_id,
            s.student_name,
            s.roll_number,
            s.department,
            s.year,
            s.phone,
            r.block,
            r.floor,
            r.room_number,
            b.bed_number,
            a.allocated_at
        FROM allocations a
        JOIN students s ON a.student_id = s.id
        JOIN beds b ON a.bed_id = b.id
        JOIN rooms r ON b.room_id = r.id
        WHERE a.status = 'Active'
        ORDER BY a.allocated_at DESC
    """).fetchall()

    conn.close()
    return rows


def get_allocation_history():
    conn = get_db()

    rows = conn.execute("""
        SELECT
            s.student_name,
            s.roll_number,
            r.block,
            r.room_number,
            b.bed_number,
            a.allocated_at,
            a.checkout_at,
            a.status
        FROM allocations a
        JOIN students s ON a.student_id = s.id
        JOIN beds b ON a.bed_id = b.id
        JOIN rooms r ON b.room_id = r.id
        ORDER BY a.id DESC
    """).fetchall()

    conn.close()
    return rows


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("""
    <div style="padding:15px 5px 24px">
        <div style="font-size:30px;font-weight:900;color:#55e8f1;
        font-family:Space Grotesk">HOSTEL<span style="color:white">FLOW</span></div>
        <div style="font-size:10px;letter-spacing:3px;color:#91a9c6">
        SMART CAMPUS LIVING</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "Hostel Explorer",
            "Allocations",
            "Mutex Control Center",
            "Reports"
        ],
        label_visibility="visible"
    )

    st.markdown("---")

    stats = get_dashboard_stats()

    st.markdown("### SYSTEM STATUS")
    st.markdown(
        '<span class="status-pill pill-green">● DATABASE ONLINE</span>',
        unsafe_allow_html=True
    )

    st.write("")
    st.caption("HOSTEL CAPACITY")
    st.progress(stats["percentage"] / 100)
    st.write(f"**{stats['occupied']} / {stats['beds']}** beds occupied")

    st.markdown("---")
    st.caption("HOSTELFLOW • OS PROJECT")
    st.caption("Mutual Exclusion & Race Condition Prevention")


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="hero">
    <div class="hero-tag">HOSTEL MANAGEMENT SYSTEM / 2026</div>
    <div class="hero-title">Smart living. Smarter allocation.</div>
    <div class="hero-sub">
        A centralized hostel allocation platform powered by secure
        resource management and operating-system synchronization.
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# OVERVIEW
# =========================================================

if page == "Overview":

    stats = get_dashboard_stats()

    st.markdown('<div class="section-label">CAMPUS OVERVIEW</div>', unsafe_allow_html=True)
    st.title("Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    cards = [
        (c1, "TOTAL BEDS", stats["beds"], "Registered capacity"),
        (c2, "OCCUPIED BEDS", stats["occupied"], "Currently allocated"),
        (c3, "AVAILABLE BEDS", stats["available"], "Ready for allocation"),
        (c4, "REGISTERED STUDENTS", stats["students"], "Student database")
    ]

    for col, label, value, foot in cards:
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">{label}</div>
                <div class="stat-value">{value}</div>
                <div class="stat-foot">↗ {foot}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    left, right = st.columns([1.15, 0.85])

    with left:
        st.markdown("### Occupancy analytics")

        st.markdown('<div class="panel">', unsafe_allow_html=True)

        st.write("Overall hostel occupancy")
        st.progress(stats["percentage"] / 100)

        st.markdown(f"""
        <h2 style="color:#55e8f1;margin-bottom:0">{stats['percentage']}%</h2>
        <span style="color:#91a9c6;font-size:13px">
        of total hostel capacity is currently occupied
        </span>
        """, unsafe_allow_html=True)

        st.write("")
        m1, m2 = st.columns(2)

        m1.metric("Occupied", stats["occupied"])
        m2.metric("Available", stats["available"])

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("### System architecture")

        st.markdown("""
        <div class="panel">
            <div style="color:#55e8f1;font-weight:800">STUDENT REQUEST</div>
            <div style="text-align:center;color:#829bb9;font-size:20px">↓</div>
            <div style="background:#172c49;padding:13px;border-radius:10px;
            text-align:center">
                <b> MUTEX LOCK </b><br>
                <small style="color:#91b0d1">Acquire critical section</small>
            </div>
            <div style="text-align:center;color:#829bb9;font-size:20px">↓</div>
            <div style="background:#172c49;padding:13px;border-radius:10px;
            text-align:center">
                <b>CHECK BED STATUS</b><br>
                <small style="color:#91b0d1">Available or occupied?</small>
            </div>
            <div style="text-align:center;color:#829bb9;font-size:20px">↓</div>
            <div style="background:rgba(45,211,151,.12);
            border:1px solid rgba(45,211,151,.3);
            padding:13px;border-radius:10px;text-align:center">
                <b style="color:#6cf0bb">SAFE ALLOCATION</b><br>
                <small style="color:#91b0d1">Release mutex lock</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Recent active allocations")

    active = get_active_allocations()

    if active:
        st.dataframe(
            [
                {
                    "Student": r["student_name"],
                    "Roll Number": r["roll_number"],
                    "Block": r["block"],
                    "Room": r["room_number"],
                    "Bed": r["bed_number"],
                    "Allocated At": r["allocated_at"]
                }
                for r in active[:6]
            ],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No active allocations yet. Go to Allocations to assign the first bed.")


# =========================================================
# HOSTEL EXPLORER
# =========================================================

elif page == "Hostel Explorer":

    st.markdown('<div class="section-label">CAMPUS INFRASTRUCTURE</div>', unsafe_allow_html=True)
    st.title("Hostel Explorer")
    st.caption("Explore every block, floor, room and individual bed.")

    beds = get_beds()

    blocks = sorted(set(b["block"] for b in beds))

    selected_block = st.selectbox("Select hostel block", blocks)

    block_beds = [b for b in beds if b["block"] == selected_block]

    floors = sorted(set(b["floor"] for b in block_beds))

    selected_floor = st.selectbox("Select floor", floors)

    floor_beds = [
        b for b in block_beds if b["floor"] == selected_floor
    ]

    room_numbers = sorted(set(b["room_number"] for b in floor_beds))

    total = len(floor_beds)
    occupied = sum(1 for b in floor_beds if b["status"] == "Occupied")

    x1, x2, x3 = st.columns(3)
    x1.metric("Rooms", len(room_numbers))
    x2.metric("Total beds", total)
    x3.metric("Available beds", total - occupied)

    st.markdown("---")

    for room in room_numbers:

        room_data = [b for b in floor_beds if b["room_number"] == room]

        st.markdown(f"#### ROOM {room}")

        cols = st.columns(4)

        for index, bed in enumerate(room_data):

            with cols[index % 4]:

                if bed["status"] == "Available":
                    st.markdown(f"""
                    <div class="bed bed-free">
                        <div>🛏️</div>
                        {bed['bed_number']}
                        <div style="font-size:10px">AVAILABLE</div>
                    </div>
                    """, unsafe_allow_html=True)

                else:
                    st.markdown(f"""
                    <div class="bed bed-taken">
                        <div>🔒</div>
                        {bed['bed_number']}
                        <div style="font-size:10px">OCCUPIED</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.caption(f"Assigned: {bed['student_name']}")

        st.markdown("")


# =========================================================
# ALLOCATIONS
# =========================================================

elif page == "Allocations":

    st.markdown('<div class="section-label">STUDENT RESOURCE MANAGEMENT</div>', unsafe_allow_html=True)
    st.title("Bed Allocations")

    tab1, tab2 = st.tabs(["＋ New Allocation", "↗ Checkout"])

    with tab1:

        st.markdown("### Register student and assign bed")
        st.caption("The system checks bed availability before confirming an allocation.")

        available_beds = get_available_beds()

        if not available_beds:
            st.warning("There are currently no available beds.")
        else:

            with st.form("allocation_form"):

                a, b = st.columns(2)

                with a:
                    student_name = st.text_input("Student full name")
                    roll_number = st.text_input("University roll number")
                    department = st.selectbox(
                        "Department",
                        ["CSE", "CSE-DS", "ECE", "EEE", "Mechanical", "Civil", "Other"]
                    )

                with b:
                    year = st.selectbox("Academic year", [1, 2, 3, 4])
                    phone = st.text_input("Phone number (optional)")

                    bed_options = {
                        f"{bed['block']} | Floor {bed['floor']} | Room {bed['room_number']} | {bed['bed_number']}": bed["bed_id"]
                        for bed in available_beds
                    }

                    selected_bed = st.selectbox(
                        "Choose available bed",
                        list(bed_options.keys())
                    )

                submitted = st.form_submit_button(
                    "CONFIRM BED ALLOCATION",
                    use_container_width=True
                )

                if submitted:

                    if not student_name.strip() or not roll_number.strip():
                        st.error("Please enter the student's name and roll number.")

                    else:
                        success, message = allocate_student(
                            student_name.strip(),
                            roll_number.strip(),
                            department,
                            year,
                            phone.strip(),
                            bed_options[selected_bed]
                        )

                        if success:
                            st.success("✓ " + message)
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(message)

    with tab2:

        st.markdown("### Checkout student")

        active = get_active_allocations()

        if active:

            allocation_options = {
                f"{r['student_name']} | {r['roll_number']} | {r['block']} / Room {r['room_number']} / {r['bed_number']}": r["allocation_id"]
                for r in active
            }

            selected_allocation = st.selectbox(
                "Select active allocation",
                list(allocation_options.keys())
            )

            if st.button("CHECKOUT SELECTED STUDENT", use_container_width=True):

                checkout_student(allocation_options[selected_allocation])

                st.success("Student checked out. Bed is now available.")
                st.rerun()

            st.markdown("---")

            st.dataframe(
                [
                    {
                        "Student": r["student_name"],
                        "Roll": r["roll_number"],
                        "Location": f"{r['block']} / {r['room_number']} / {r['bed_number']}"
                    }
                    for r in active
                ],
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("There are no active allocations to check out.")


# =========================================================
# MUTEX CONTROL CENTER
# =========================================================

elif page == "Mutex Control Center":

    st.markdown('<div class="section-label">OPERATING SYSTEMS / SYNCHRONIZATION LAB</div>', unsafe_allow_html=True)
    st.title("Mutex Control Center")

    st.markdown("""
    <div class="panel">
        <h3 style="color:#55e8f1">Race Condition Prevention</h3>
        <p style="color:#a8bdd8">
        Imagine five students requesting the exact same bed at almost the same time.
        Without synchronization, multiple processes could read the bed as available
        and attempt to claim it. This is a race condition.
        </p>
        <p style="color:#a8bdd8">
        HOSTELFLOW uses a mutex lock to protect the critical section.
        Only one thread can check and allocate the bed at a time.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Live synchronization demonstration")

    c1, c2, c3 = st.columns(3)
    c1.metric("Concurrent threads", "5")
    c2.metric("Shared resource", "1 bed")
    c3.metric("Expected successful allocations", "1")

    st.info(
        "This test uses a dedicated demonstration bed. "
        "It releases the winning test allocation after the test, so your actual hostel records stay unaffected."
    )

    if st.button("▶ RUN 5-THREAD RACE CONDITION TEST", use_container_width=True):

        # A dedicated demonstration bed is created in the database.
        conn = get_db()

        demo_room = conn.execute("""
            SELECT id FROM rooms
            WHERE block = 'DEMO BLOCK' AND room_number = 'TEST-001'
        """).fetchone()

        if not demo_room:
            cursor = conn.execute("""
                INSERT INTO rooms (block, floor, room_number)
                VALUES ('DEMO BLOCK', 1, 'TEST-001')
            """)

            demo_room_id = cursor.lastrowid

            cursor = conn.execute("""
                INSERT INTO beds (room_id, bed_number)
                VALUES (?, 'DEMO-BED')
            """, (demo_room_id,))

            demo_bed_id = cursor.lastrowid

        else:
            demo_room_id = demo_room["id"]

            demo_bed = conn.execute("""
                SELECT id FROM beds
                WHERE room_id = ? AND bed_number = 'DEMO-BED'
            """, (demo_room_id,)).fetchone()

            if demo_bed:
                demo_bed_id = demo_bed["id"]
            else:
                cursor = conn.execute("""
                    INSERT INTO beds (room_id, bed_number)
                    VALUES (?, 'DEMO-BED')
                """, (demo_room_id,))
                demo_bed_id = cursor.lastrowid

        conn.commit()

        # Ensure the demonstration bed starts empty.
        conn.execute("""
            UPDATE allocations
            SET status = 'Checked Out', checkout_at = ?
            WHERE bed_id = ? AND status = 'Active'
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            demo_bed_id
        ))

        conn.commit()
        conn.close()

        barrier = threading.Barrier(5)
        results = []
        results_lock = threading.Lock()

        def student_request(number):

            barrier.wait()

            success, message = allocate_student(
                f"Demo Student {number}",
                f"DEMO-{number}-{int(time.time() * 1000)}-{random.randint(100,999)}",
                "CSE-DS",
                2,
                "",
                demo_bed_id
            )

            with results_lock:
                results.append({
                    "Thread": f"Thread {number}",
                    "Student": f"Demo Student {number}",
                    "Result": "SUCCESS" if success else "BLOCKED",
                    "Message": message
                })

        threads = []

        for number in range(1, 6):
            thread = threading.Thread(
                target=student_request,
                args=(number,)
            )
            threads.append(thread)

        start = time.time()

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        elapsed = round((time.time() - start) * 1000, 2)

        successful = [r for r in results if r["Result"] == "SUCCESS"]
        blocked = [r for r in results if r["Result"] == "BLOCKED"]

        # Release the demonstration winner after recording the result.
        conn = get_db()

        conn.execute("""
            UPDATE allocations
            SET status = 'Checked Out', checkout_at = ?
            WHERE bed_id = ? AND status = 'Active'
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            demo_bed_id
        ))

        conn.commit()
        conn.close()

        st.session_state["mutex_results"] = results
        st.session_state["mutex_success"] = len(successful)
        st.session_state["mutex_blocked"] = len(blocked)
        st.session_state["mutex_elapsed"] = elapsed

    if "mutex_results" in st.session_state:

        results = st.session_state["mutex_results"]

        st.markdown("---")
        st.markdown("### Test results")

        x1, x2, x3 = st.columns(3)

        x1.metric("Successful requests", st.session_state["mutex_success"])
        x2.metric("Blocked requests", st.session_state["mutex_blocked"])
        x3.metric("Execution time", f"{st.session_state['mutex_elapsed']} ms")

        if st.session_state["mutex_success"] == 1:
            st.success("MUTEX SUCCESS: Exactly one thread received the bed. No duplicate allocation occurred.")
        else:
            st.error("Unexpected result. Check the database and synchronization logic.")

        st.dataframe(results, use_container_width=True, hide_index=True)

        st.markdown("""
        <div class="panel">
            <div style="color:#55e8f1;font-weight:800">WHAT JUST HAPPENED?</div>
            <p style="color:#a8bdd8">
            1. Five threads started competing for one shared bed.<br>
            2. Each thread attempted to enter the critical section.<br>
            3. The mutex lock allowed one thread at a time.<br>
            4. The winning thread allocated the bed.<br>
            5. The remaining threads found it occupied and were blocked.<br>
            6. The demonstration allocation was released after the test.
            </p>
            <span class="status-pill pill-green">RACE CONDITION PREVENTED</span>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="panel" style="text-align:center;padding:35px">
            <div style="font-size:42px">⚙️</div>
            <h3>Synchronization engine ready</h3>
            <p style="color:#91a9c6">
            Run the test to see five simultaneous requests compete for one bed.
            </p>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# REPORTS
# =========================================================

elif page == "Reports":

    st.markdown('<div class="section-label">DATA & ANALYTICS</div>', unsafe_allow_html=True)
    st.title("Hostel Reports")

    stats = get_dashboard_stats()
    history = get_allocation_history()

    a, b, c = st.columns(3)

    a.metric("Total capacity", stats["beds"])
    b.metric("Current occupancy", stats["occupied"])
    c.metric("Occupancy rate", f"{stats['percentage']}%")

    st.markdown("---")

    st.markdown("### Occupancy by block")

    beds = get_beds()
    block_names = sorted(set(b["block"] for b in beds))

    chart_data = []

    for block in block_names:

        block_beds = [b for b in beds if b["block"] == block]

        occupied = sum(
            1 for b in block_beds if b["status"] == "Occupied"
        )

        available = len(block_beds) - occupied

        chart_data.append({
            "Block": block,
            "Occupied": occupied,
            "Available": available
        })

    if chart_data:
        import pandas as pd
        chart_df = pd.DataFrame(chart_data).set_index("Block")

        st.bar_chart(chart_df)

    st.markdown("### Allocation history")

    if history:

        history_data = [
            {
                "Student": r["student_name"],
                "Roll Number": r["roll_number"],
                "Block": r["block"],
                "Room": r["room_number"],
                "Bed": r["bed_number"],
                "Allocated": r["allocated_at"],
                "Checkout": r["checkout_at"] or "—",
                "Status": r["status"]
            }
            for r in history
        ]

        st.dataframe(
            history_data,
            use_container_width=True,
            hide_index=True
        )

        csv_data = pd.DataFrame(history_data).to_csv(index=False)

        st.download_button(
            "⬇ DOWNLOAD ALLOCATION REPORT (CSV)",
            data=csv_data,
            file_name="hostelflow_allocation_report.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:
        st.info("No allocation history available yet.")


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown("""
<div style="text-align:center;padding:15px;color:#7187a5;font-size:11px">
    <span style="color:#55e8f1;font-weight:800">HOSTELFLOW</span>
    &nbsp; • &nbsp; SMART HOSTEL MANAGEMENT SYSTEM
    <br><br>
    Built with Python · Streamlit · SQLite · Thread Synchronization
    <br>
    Operating Systems Project | 2026
</div>
""", unsafe_allow_html=True)