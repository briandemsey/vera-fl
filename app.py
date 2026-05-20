"""
VERA-FL: Verification Engine for Results & Accountability - Florida
Type 4 Dyslexia Screening using FAST and ACCESS for ELLs Assessment Data
B.E.S.T. Curriculum Standards Browser

H-EDU.Solutions | https://h-edu.solutions
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

APP_PASSWORD = "vera2026"

# Florida colors
FL_BLUE = "#002D72"
FL_ORANGE = "#F4811F"
FL_RED = "#C41E3A"
FL_GOLD = "#FFD700"

# ============================================================================
# SAMPLE DATA - Florida Districts
# ============================================================================

def load_districts():
    """Load Florida district data (alphabetical order)."""
    districts_data = [
        ("06", "Broward County", 256000, 38400, 15.0, 89.2, "B"),
        ("16", "Duval County", 130000, 13000, 10.0, 85.6, "B"),
        ("29", "Hillsborough County", 219000, 39420, 18.0, 87.8, "B"),
        ("13", "Miami-Dade County", 334000, 83500, 25.0, 88.5, "B"),
        ("48", "Orange County", 212000, 46640, 22.0, 86.4, "B"),
        ("49", "Osceola County", 82000, 28700, 35.0, 84.2, "B"),
        ("50", "Palm Beach County", 190000, 30400, 16.0, 91.2, "A"),
        ("52", "Pinellas County", 96000, 7680, 8.0, 90.8, "A"),
    ]

    df = pd.DataFrame(districts_data, columns=[
        'district_id', 'district_name', 'total_students',
        'ell_count', 'ell_percent', 'graduation_rate', 'school_grade'
    ])
    return df


def load_access_data():
    """Load sample ACCESS for ELLs assessment data."""
    access_data = []

    districts = [
        ("06", "Broward County"),
        ("16", "Duval County"),
        ("29", "Hillsborough County"),
        ("13", "Miami-Dade County"),
        ("48", "Orange County"),
        ("49", "Osceola County"),
        ("50", "Palm Beach County"),
        ("52", "Pinellas County"),
    ]

    for district_id, district_name in districts:
        for grade in range(3, 9):
            for year in [2024, 2025]:
                # Generate realistic ACCESS scores (scale 1.0-6.0)
                base_speaking = 3.2 + (grade * 0.1)
                base_writing = 2.8 + (grade * 0.08)

                # Add district-specific variation
                if district_id == "49":  # Osceola - highest EL%, larger delta
                    speaking_adj = 0.6
                    writing_adj = -0.2
                elif district_id == "13":  # Miami-Dade
                    speaking_adj = 0.5
                    writing_adj = 0.0
                elif district_id == "50":  # Palm Beach - higher performing
                    speaking_adj = 0.3
                    writing_adj = 0.3
                else:
                    speaking_adj = 0.4
                    writing_adj = 0.1

                access_data.append({
                    'district_id': district_id,
                    'district_name': district_name,
                    'grade': grade,
                    'year': year,
                    'total_tested': 2000 + (grade * 100) if district_id in ["13", "06"] else 500 + (grade * 50),
                    'listening_avg': min(6.0, base_speaking + speaking_adj - 0.1),
                    'speaking_avg': min(6.0, base_speaking + speaking_adj),
                    'reading_avg': min(6.0, base_writing + writing_adj + 0.2),
                    'writing_avg': min(6.0, base_writing + writing_adj),
                    'composite_avg': min(6.0, (base_speaking + speaking_adj + base_writing + writing_adj) / 2 + 0.3)
                })

    return pd.DataFrame(access_data)


def load_fast_data():
    """Load sample FAST (Florida Assessment of Student Thinking) data."""
    fast_data = []

    districts = [
        ("06", "Broward County"),
        ("16", "Duval County"),
        ("29", "Hillsborough County"),
        ("13", "Miami-Dade County"),
        ("48", "Orange County"),
        ("49", "Osceola County"),
        ("50", "Palm Beach County"),
        ("52", "Pinellas County"),
    ]

    for district_id, district_name in districts:
        for grade in range(3, 9):
            for year in [2024, 2025]:
                for subject in ['ELA', 'Math']:
                    # Generate realistic FAST proficiency (Achievement Levels 1-5)
                    if district_id == "50":  # Palm Beach - highest performing
                        level3_plus = 68 + (grade * 0.5)
                        level4_plus = 42 + (grade * 0.6)
                        level5 = 18 + (grade * 0.5)
                    elif district_id in ["49"]:  # Lower performing
                        level3_plus = 48 + (grade * 0.4)
                        level4_plus = 22 + (grade * 0.4)
                        level5 = 8 + (grade * 0.3)
                    elif district_id in ["13", "06"]:  # Large urban
                        level3_plus = 55 + (grade * 0.4)
                        level4_plus = 30 + (grade * 0.5)
                        level5 = 12 + (grade * 0.4)
                    else:  # Average
                        level3_plus = 60 + (grade * 0.4)
                        level4_plus = 35 + (grade * 0.5)
                        level5 = 15 + (grade * 0.4)

                    fast_data.append({
                        'district_id': district_id,
                        'district_name': district_name,
                        'grade': grade,
                        'subject': subject,
                        'year': year,
                        'total_tested': 25000 + (grade * 500) if district_id in ["13", "06"] else 5000 + (grade * 200),
                        'level3_plus_pct': min(95, level3_plus),
                        'level4_plus_pct': min(80, level4_plus),
                        'level5_pct': min(50, level5)
                    })

    return pd.DataFrame(fast_data)


# ============================================================================
# B.E.S.T. STANDARDS DATA
# ============================================================================

def load_best_standards():
    """Load sample B.E.S.T. standards data."""
    standards = [
        # ELA Grade 3
        ("ELA.3.F.1.3", "Grade 3", "ELA", "Foundational Skills", "Phonics and Word Analysis",
         "Use knowledge of grade-level phonics and word-analysis skills to decode words."),
        ("ELA.3.F.1.4", "Grade 3", "ELA", "Foundational Skills", "Fluency",
         "Read grade-level texts with accuracy, automaticity, and appropriate prosody or expression."),
        ("ELA.3.R.1.1", "Grade 3", "ELA", "Reading", "Literary Elements",
         "Explain how one or more characters develop throughout the plot in a literary text."),
        ("ELA.3.R.1.2", "Grade 3", "ELA", "Reading", "Theme",
         "Explain a theme and how it develops, using details, in a literary text."),
        ("ELA.3.R.2.1", "Grade 3", "ELA", "Reading", "Structure",
         "Explain how text features contribute to meaning and identify the text structures of problem/solution, sequence, and description."),

        # Math Grade 3
        ("MA.3.NSO.1.1", "Grade 3", "Math", "Number Sense", "Place Value",
         "Read and write numbers from 0 to 10,000 using standard form, expanded form and word form."),
        ("MA.3.NSO.1.2", "Grade 3", "Math", "Number Sense", "Comparison",
         "Compose and decompose four-digit numbers in multiple ways using thousands, hundreds, tens and ones."),
        ("MA.3.FR.1.1", "Grade 3", "Math", "Fractions", "Understanding",
         "Represent and interpret unit fractions in the form 1/n as the quantity formed by one part when a whole is partitioned into n equal parts."),

        # ELA Grade 4
        ("ELA.4.R.1.1", "Grade 4", "ELA", "Reading", "Literary Elements",
         "Explain how setting, events, conflict, and character development contribute to the plot in a literary text."),
        ("ELA.4.R.1.2", "Grade 4", "ELA", "Reading", "Theme",
         "Explain a stated or implied theme and how it develops, using details, in a literary text."),

        # Math Grade 4
        ("MA.4.NSO.1.1", "Grade 4", "Math", "Number Sense", "Place Value",
         "Express how the value of a digit in a multi-digit whole number changes if the digit moves one place to the left or right."),
        ("MA.4.FR.1.1", "Grade 4", "Math", "Fractions", "Equivalence",
         "Model and express a fraction, including mixed numbers and fractions greater than one, with the denominator 10 as an equivalent fraction with the denominator 100."),
    ]

    df = pd.DataFrame(standards, columns=[
        'benchmark_code', 'grade', 'subject', 'strand', 'standard', 'description'
    ])
    return df


# ============================================================================
# AUTHENTICATION
# ============================================================================

def check_password():
    st.session_state.authenticated = True
    return True


# ============================================================================
# TYPE 4 DETECTION
# ============================================================================

def compute_type4_analysis(access_df, district_id, grade, year):
    """
    Compute Type 4 (oral-written delta) analysis for a district.

    Type 4 candidates show strong oral skills but weak written skills.
    Delta = Speaking Score - Writing Score
    Flag threshold: Delta > 0.8 points (on ACCESS 1-6 scale)
    """
    filtered = access_df[
        (access_df['district_id'] == district_id) &
        (access_df['grade'] == grade) &
        (access_df['year'] == year)
    ]

    if filtered.empty:
        return None

    row = filtered.iloc[0]

    # Calculate delta (Speaking - Writing)
    speaking = row['speaking_avg']
    writing = row['writing_avg']
    delta = speaking - writing

    # Flag if delta exceeds threshold
    flagged = delta > 0.8

    return {
        'district_id': district_id,
        'district_name': row['district_name'],
        'grade': grade,
        'year': year,
        'speaking_avg': speaking,
        'writing_avg': writing,
        'delta': delta,
        'flagged': flagged,
        'total_tested': row['total_tested'],
        'estimated_flagged': int(row['total_tested'] * 0.15) if flagged else int(row['total_tested'] * 0.05)
    }


# ============================================================================
# DASHBOARD PAGES
# ============================================================================

def render_overview(districts_df, access_df, fast_df):
    """Render the overview dashboard."""
    st.header("Florida Education Overview")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Districts", len(districts_df))
    with col2:
        st.metric("Total Students", f"{districts_df['total_students'].sum():,}")
    with col3:
        st.metric("English Learners", f"{districts_df['ell_count'].sum():,}")
    with col4:
        avg_grad = districts_df['graduation_rate'].mean()
        st.metric("Avg Graduation Rate", f"{avg_grad:.1f}%")

    st.divider()

    # District overview table
    st.subheader("Pilot Districts")

    display_df = districts_df.copy()
    display_df['ell_percent'] = display_df['ell_percent'].apply(lambda x: f"{x:.1f}%")
    display_df['graduation_rate'] = display_df['graduation_rate'].apply(lambda x: f"{x:.1f}%")
    display_df.columns = ['District ID', 'District Name', 'Total Students', 'EL Count', 'EL %', 'Grad Rate', 'School Grade']

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # EL Population chart
    st.subheader("English Learner Population by District")

    fig = px.bar(
        districts_df.sort_values('ell_count', ascending=True),
        x='ell_count',
        y='district_name',
        orientation='h',
        color='ell_percent',
        color_continuous_scale=[[0, '#ffffff'], [0.5, FL_BLUE], [1, FL_ORANGE]],
        labels={'ell_count': 'English Learners', 'district_name': 'District', 'ell_percent': 'EL %'}
    )
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def render_best_browser(standards_df):
    """Render the B.E.S.T. standards browser."""
    st.header("B.E.S.T. Standards Browser")

    st.markdown("""
    **B.E.S.T. (Benchmarks for Excellent Student Thinking)** are Florida's academic standards
    adopted in 2020. Browse standards by grade level, subject, and strand.
    """)

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        grade_options = ["All Grades"] + sorted(standards_df['grade'].unique().tolist())
        selected_grade = st.selectbox("Grade Level", grade_options)

    with col2:
        subject_options = ["All Subjects"] + sorted(standards_df['subject'].unique().tolist())
        selected_subject = st.selectbox("Subject", subject_options)

    with col3:
        search_query = st.text_input("Search Standards", placeholder="e.g., 'fractions' or 'ELA.3'")

    # Filter data
    filtered = standards_df.copy()
    if selected_grade != "All Grades":
        filtered = filtered[filtered['grade'] == selected_grade]
    if selected_subject != "All Subjects":
        filtered = filtered[filtered['subject'] == selected_subject]
    if search_query:
        mask = (
            filtered['benchmark_code'].str.contains(search_query, case=False, na=False) |
            filtered['description'].str.contains(search_query, case=False, na=False) |
            filtered['standard'].str.contains(search_query, case=False, na=False)
        )
        filtered = filtered[mask]

    st.divider()

    st.write(f"Showing {len(filtered)} standards")

    # Display standards
    for _, row in filtered.iterrows():
        badge_color = FL_BLUE if row['subject'] == 'ELA' else FL_ORANGE

        st.markdown(f"""
        <div style="padding: 12px; margin: 8px 0; border-left: 4px solid {badge_color}; background: #f9f9f9;">
            <span style="background: {badge_color}; color: white; padding: 2px 8px; font-size: 0.75rem; border-radius: 3px;">{row['subject']}</span>
            <span style="background: #666; color: white; padding: 2px 8px; font-size: 0.75rem; border-radius: 3px; margin-left: 5px;">{row['grade']}</span>
            <strong style="margin-left: 10px;">{row['benchmark_code']}</strong>
            <span style="margin-left: 10px; color: #666;">| {row['strand']} - {row['standard']}</span>
            <p style="margin: 8px 0 0 0; color: #333;">{row['description']}</p>
        </div>
        """, unsafe_allow_html=True)


def render_access_analysis(access_df, districts_df):
    """Render ACCESS for ELLs assessment analysis."""
    st.header("ACCESS for ELLs Analysis")

    st.markdown("""
    **ACCESS for ELLs** (WIDA) measures English learners' proficiency across four domains:
    Listening, Speaking, Reading, and Writing on a scale of 1.0-6.0.
    """)

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        district = st.selectbox(
            "Select District",
            options=districts_df['district_name'].tolist(),
            key="access_district"
        )

    with col2:
        grade = st.selectbox("Select Grade", options=list(range(3, 9)), key="access_grade")

    with col3:
        year = st.selectbox("Select Year", options=[2025, 2024], key="access_year")

    # Get district ID
    district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]

    # Filter data
    filtered = access_df[
        (access_df['district_id'] == district_id) &
        (access_df['grade'] == grade) &
        (access_df['year'] == year)
    ]

    if not filtered.empty:
        row = filtered.iloc[0]

        st.divider()

        # Domain scores
        st.subheader("ACCESS Domain Scores")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Listening", f"{row['listening_avg']:.1f}")
        with col2:
            st.metric("Speaking", f"{row['speaking_avg']:.1f}")
        with col3:
            st.metric("Reading", f"{row['reading_avg']:.1f}")
        with col4:
            st.metric("Writing", f"{row['writing_avg']:.1f}")

        # Domain comparison chart
        domains = ['Listening', 'Speaking', 'Reading', 'Writing']
        scores = [row['listening_avg'], row['speaking_avg'], row['reading_avg'], row['writing_avg']]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=domains,
            y=scores,
            marker_color=[FL_BLUE, FL_ORANGE, FL_BLUE, FL_ORANGE],
            text=[f"{s:.1f}" for s in scores],
            textposition='outside'
        ))
        fig.update_layout(
            title=f"ACCESS Domain Scores - {district} - Grade {grade} ({year})",
            yaxis_title="Proficiency Level (1-6)",
            yaxis_range=[0, 6.5],
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        # Oral vs Written gap highlight
        oral_avg = (row['listening_avg'] + row['speaking_avg']) / 2
        written_avg = (row['reading_avg'] + row['writing_avg']) / 2
        gap = oral_avg - written_avg

        st.subheader("Oral vs Written Gap")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Oral Average", f"{oral_avg:.2f}", help="(Listening + Speaking) / 2")
        with col2:
            st.metric("Written Average", f"{written_avg:.2f}", help="(Reading + Writing) / 2")
        with col3:
            delta_color = "normal" if gap < 0.5 else "inverse"
            st.metric("Gap", f"{gap:+.2f}", delta=f"{'Flag' if gap > 0.6 else 'OK'}", delta_color=delta_color)


def render_type4_detection(access_df, districts_df):
    """Render Type 4 detection analysis."""
    st.header("Type 4 Detection")

    st.markdown("""
    **Type 4 dyslexia candidates** demonstrate strong oral communication abilities but
    significant challenges with written expression. VERA-FL identifies these students by
    analyzing the delta between ACCESS Speaking and Writing domain scores.

    **Flag Threshold:** Speaking - Writing delta > 0.8 points
    """)

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        district = st.selectbox(
            "Select District",
            options=districts_df['district_name'].tolist(),
            key="type4_district"
        )

    with col2:
        grade = st.selectbox("Select Grade", options=list(range(3, 9)), key="type4_grade")

    with col3:
        year = st.selectbox("Select Year", options=[2025, 2024], key="type4_year")

    # Get district ID
    district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]

    # Run analysis
    result = compute_type4_analysis(access_df, district_id, grade, year)

    if result:
        st.divider()

        # Results
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Speaking Score", f"{result['speaking_avg']:.2f}")
        with col2:
            st.metric("Writing Score", f"{result['writing_avg']:.2f}")
        with col3:
            st.metric("Delta", f"{result['delta']:+.2f}")
        with col4:
            status = "FLAGGED" if result['flagged'] else "OK"
            st.metric("Status", status)

        # Visual delta display
        st.subheader("Oral-Written Delta Analysis")

        fig = go.Figure()

        # Speaking bar
        fig.add_trace(go.Bar(
            name='Speaking',
            x=['Score'],
            y=[result['speaking_avg']],
            marker_color=FL_ORANGE,
            text=[f"{result['speaking_avg']:.2f}"],
            textposition='outside'
        ))

        # Writing bar
        fig.add_trace(go.Bar(
            name='Writing',
            x=['Score'],
            y=[result['writing_avg']],
            marker_color=FL_BLUE,
            text=[f"{result['writing_avg']:.2f}"],
            textposition='outside'
        ))

        fig.update_layout(
            title=f"Speaking vs Writing - {district} - Grade {grade}",
            barmode='group',
            yaxis_range=[0, 6.5],
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)

        # Interpretation
        if result['flagged']:
            st.error(f"""
            **Type 4 Flag Triggered**

            This grade level shows a significant oral-written gap (delta: {result['delta']:+.2f}).

            - **Estimated students affected:** {result['estimated_flagged']} of {result['total_tested']} tested
            - **Recommended action:** Individual student-level screening per Florida Statute 1008.25
            - **Next steps:** Cross-reference with FAST ELA writing performance
            """)
        else:
            st.success(f"""
            **No Type 4 Flag**

            The oral-written gap for this grade level is within normal range (delta: {result['delta']:+.2f}).

            - **Students tested:** {result['total_tested']}
            - **Continue monitoring:** Regular ACCESS domain analysis recommended
            """)

        # All grades comparison for district
        st.subheader(f"All Grades - {district} ({year})")

        all_grades_data = []
        for g in range(3, 9):
            r = compute_type4_analysis(access_df, district_id, g, year)
            if r:
                all_grades_data.append(r)

        if all_grades_data:
            grades_df = pd.DataFrame(all_grades_data)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=grades_df['grade'],
                y=grades_df['speaking_avg'],
                name='Speaking',
                mode='lines+markers',
                line=dict(color=FL_ORANGE, width=3),
                marker=dict(size=10)
            ))
            fig.add_trace(go.Scatter(
                x=grades_df['grade'],
                y=grades_df['writing_avg'],
                name='Writing',
                mode='lines+markers',
                line=dict(color=FL_BLUE, width=3),
                marker=dict(size=10)
            ))

            fig.update_layout(
                title="Speaking vs Writing Across Grades",
                xaxis_title="Grade",
                yaxis_title="Proficiency Level",
                yaxis_range=[0, 6.5],
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)


def render_fast_analysis(fast_df, districts_df):
    """Render FAST assessment analysis."""
    st.header("FAST Assessment Analysis")

    st.markdown("""
    **FAST (Florida Assessment of Student Thinking)** measures student achievement
    in ELA and Mathematics aligned to B.E.S.T. standards. Achievement Levels 1-5.
    """)

    # Filters
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        district = st.selectbox(
            "Select District",
            options=districts_df['district_name'].tolist(),
            key="fast_district"
        )

    with col2:
        grade = st.selectbox("Select Grade", options=list(range(3, 9)), key="fast_grade")

    with col3:
        subject = st.selectbox("Select Subject", options=['ELA', 'Math'], key="fast_subject")

    with col4:
        year = st.selectbox("Select Year", options=[2025, 2024], key="fast_year")

    # Get district ID
    district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]

    # Filter data
    filtered = fast_df[
        (fast_df['district_id'] == district_id) &
        (fast_df['grade'] == grade) &
        (fast_df['subject'] == subject) &
        (fast_df['year'] == year)
    ]

    if not filtered.empty:
        row = filtered.iloc[0]

        st.divider()

        # Performance levels
        st.subheader("Achievement Level Distribution")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Level 3+ (On Grade Level)", f"{row['level3_plus_pct']:.1f}%")
        with col2:
            st.metric("Level 4+ (Above Grade Level)", f"{row['level4_plus_pct']:.1f}%")
        with col3:
            st.metric("Level 5 (Mastery)", f"{row['level5_pct']:.1f}%")

        # Performance chart
        levels = ['Level 3+\n(On Grade)', 'Level 4+\n(Above Grade)', 'Level 5\n(Mastery)']
        values = [row['level3_plus_pct'], row['level4_plus_pct'], row['level5_pct']]
        colors = [FL_ORANGE, FL_BLUE, '#4CAF50']

        fig = go.Figure(data=[
            go.Bar(x=levels, y=values, marker_color=colors, text=[f"{v:.1f}%" for v in values], textposition='outside')
        ])
        fig.update_layout(
            title=f"FAST {subject} Performance - {district} - Grade {grade} ({year})",
            yaxis_title="Percentage",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)


def render_export(access_df, fast_df, districts_df):
    """Render data export page."""
    st.header("Export Data")

    st.markdown("Download assessment data for further analysis.")

    # District filter
    district = st.selectbox(
        "Select District (or All)",
        options=["All Districts"] + districts_df['district_name'].tolist()
    )

    year = st.selectbox("Select Year", options=[2025, 2024])

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("ACCESS Data")
        if district == "All Districts":
            export_access = access_df[access_df['year'] == year]
        else:
            district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]
            export_access = access_df[(access_df['district_id'] == district_id) & (access_df['year'] == year)]

        st.dataframe(export_access, use_container_width=True, hide_index=True)

        csv_access = export_access.to_csv(index=False)
        st.download_button(
            "Download ACCESS CSV",
            csv_access,
            f"vera_fl_access_{year}.csv",
            "text/csv",
            use_container_width=True
        )

    with col2:
        st.subheader("FAST Data")
        if district == "All Districts":
            export_fast = fast_df[fast_df['year'] == year]
        else:
            district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]
            export_fast = fast_df[(fast_df['district_id'] == district_id) & (fast_df['year'] == year)]

        st.dataframe(export_fast, use_container_width=True, hide_index=True)

        csv_fast = export_fast.to_csv(index=False)
        st.download_button(
            "Download FAST CSV",
            csv_fast,
            f"vera_fl_fast_{year}.csv",
            "text/csv",
            use_container_width=True
        )


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    st.set_page_config(
        page_title="VERA-FL | Florida B.E.S.T. Standards & Type 4 Detection",
        page_icon="🌴",
        layout="wide"
    )

    # Custom CSS
    st.markdown(f"""
    <style>
        .stApp {{
            background-color: #fafafa;
        }}
        .block-container {{
            padding-top: 2rem;
        }}
        h1, h2, h3 {{
            color: {FL_BLUE};
        }}
        .stButton > button {{
            background-color: {FL_BLUE};
            color: white;
        }}
        .stButton > button:hover {{
            background-color: {FL_ORANGE};
            color: white;
        }}
    </style>
    """, unsafe_allow_html=True)

    # Authentication
    if not check_password():
        return

    # Load data
    districts_df = load_districts()
    access_df = load_access_data()
    fast_df = load_fast_data()
    standards_df = load_best_standards()

    # Sidebar
    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: {FL_BLUE}; margin: 0;">VERA-FL</h2>
        <p style="color: #666; font-size: 0.85rem; margin-top: 5px;">Florida Implementation</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.divider()

    page = st.sidebar.radio(
        "Navigation",
        ["Overview", "B.E.S.T. Browser", "ACCESS Analysis", "Type 4 Detection", "FAST Analysis", "Export Data"]
    )

    st.sidebar.divider()

    st.sidebar.markdown("""
    **Data Sources:**
    - B.E.S.T. (Curriculum Standards)
    - FAST (Student Assessment)
    - ACCESS for ELLs (WIDA)
    - FLDOE Accountability

    **Type 4 Detection:**
    - Speaking vs Writing delta
    - Flag threshold: > 0.8 points

    ---

    [H-EDU.Solutions](https://h-edu.solutions)
    """)

    # Render selected page
    if page == "Overview":
        render_overview(districts_df, access_df, fast_df)
    elif page == "B.E.S.T. Browser":
        render_best_browser(standards_df)
    elif page == "ACCESS Analysis":
        render_access_analysis(access_df, districts_df)
    elif page == "Type 4 Detection":
        render_type4_detection(access_df, districts_df)
    elif page == "FAST Analysis":
        render_fast_analysis(fast_df, districts_df)
    elif page == "Export Data":
        render_export(access_df, fast_df, districts_df)


if __name__ == "__main__":
    main()
