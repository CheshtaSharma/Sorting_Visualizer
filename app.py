import streamlit as st
import random
import matplotlib.pyplot as plt
import time
from sorting import bubble_sort, insertion_sort, merge_sort, quick_sort, selection_sort, heap_sort

# Intro popup toggle
if 'show_intro' not in st.session_state:
    st.session_state.show_intro = True

# Page setup
st.set_page_config(page_title="📊 Sorting Visualizer", layout="wide")

# Remove top padding
st.markdown("""
    <style>
        .block-container {
            padding-top: 0rem;
        }
    </style>
""", unsafe_allow_html=True)

# Fonts & Theme
st.markdown("""
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
        }
        .stApp {
            background-color: #053032;
            color: white;
        }
        section[data-testid="stSidebar"] {
            background-color: #053032;
        }
        .sidebar-content {
            color: white;
        }
        .stSelectbox, .stButton > button, .stTextInput > div > div > input {
            background-color: #053032;
            color: white;
        }
        .stButton > button {
            background-color: #1E90FF;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: background-color 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #0f73d8;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Page title
st.title("📊 Sorting Algorithm Visualizer")

# Intro popup
if st.session_state.get('show_intro', True):
    with st.expander("📘 Click to Learn: What Are Sorting Algorithms?", expanded=False):
        st.markdown("""
        <div style="line-height: 1.6;">
        👋 Welcome to the <b>SORTING ALGORITHM VISUALIZER</b>! 🎉<br>
        Sorting helps arrange data in a specific order — like ascending or descending.

        🔍 Here's what you'll explore:

        | 🧠 Algorithm       | 🔧 Concept | ⏱ Time | 🧮 Space |
        |------------------|-----------------------------|----------------|------------|
        | 🔁 Bubble Sort   | Swaps adjacent items repeatedly | O(n²) | O(1) |
        | 🧩 Insertion Sort| Builds sorted array step-by-step | O(n²) | O(1) |
        | 🧬 Merge Sort    | Divide → Sort → Merge | O(n log n) | O(n) |
        | ⚡ Quick Sort    | Partition using a pivot | O(n log n) avg | O(log n) |
        | 🎯 Selection Sort| Selects min and swaps | O(n²) | O(1) |
        | 🏗️ Heap Sort     | Uses heap tree structure | O(n log n) | O(1) |

        ✅ <b>Select an algorithm</b> from the sidebar, choose <b>speed</b>, and click <b>Start Sorting</b> to begin!

        💡 <b>Tip:</b> Try different algorithms on large arrays to see real differences!
        </div>
        """, unsafe_allow_html=True)

# Sidebar controls
algo = st.sidebar.selectbox("🧠 Choose Algorithm", ['bubble', 'insertion', 'merge', 'quick', 'selection', 'heap'])
speed_mode = st.sidebar.selectbox("⚙️ Speed Mode", ["High", "Moderate", "Low"])
input_mode = st.sidebar.radio("📥 Array Input Mode", ["Random", "Custom"])

# Input array handling
if input_mode == "Random":
    size = st.sidebar.slider("📊 Number of Bars", 4, 50, 5)
    if st.sidebar.button("🎲 Generate Random Array") or 'array_data' not in st.session_state:
        st.session_state.array_data = [random.randint(10, 100) for _ in range(size)]
else:
    custom_input = st.sidebar.text_input("✍️ Enter custom array (comma-separated)", value="10,30,20,40")
    try:
        user_array = [int(x.strip()) for x in custom_input.split(",") if x.strip() != ""]
        if user_array:
            st.session_state.array_data = user_array
        else:
            st.sidebar.warning("⚠️ Please enter at least two numbers.")
    except:
        st.sidebar.warning("❌ Invalid input. Format: 5,10,20")

# Start sorting button
start_sorting = st.sidebar.button("🚀 Start Sorting")

# Algorithm descriptions & complexity
descriptions = {
    'bubble': "🔁 Compares adjacent elements and swaps them if needed.",
    'insertion': "🧩 Inserts each element into its correct position.",
    'merge': "🧬 Divides the list, sorts, and merges.",
    'quick': "⚡ Picks a pivot, partitions, and sorts recursively.",
    'selection': "🎯 Finds the minimum and swaps it into place.",
    'heap': "🏗️ Builds a heap and sorts by removing root elements.",
}
st.sidebar.markdown(f"📘 **{algo.capitalize()} Sort:** {descriptions[algo]}")
complexities = {
    'bubble': "⏱ Time: O(n²) | 🧮 Space: O(1)",
    'insertion': "⏱ Time: O(n²) | 🧮 Space: O(1)",
    'merge': "⏱ Time: O(n log n) | 🧮 Space: O(n)",
    'quick': "⏱ Time: O(n log n) avg, O(n²) worst | 🧮 Space: O(log n)",
    'selection': "⏱ Time: O(n²) | 🧮 Space: O(1)",
    'heap': "⏱ Time: O(n log n) | 🧮 Space: O(1)",
}
st.sidebar.caption(complexities[algo])

# Final data setup
data = st.session_state.array_data
copied = data.copy()

# Speed calculation
if speed_mode == "High":
    base_delay = 0.001
elif speed_mode == "Moderate":
    base_delay = 0.01
else:
    base_delay = 0.05
delay = base_delay * (len(copied) / 10)

# Bar plot placeholder
placeholder = st.empty()

# Bar plot function
def draw_bars(values, color_map=None):
    fig, ax = plt.subplots(figsize=(8, 3.7))
    fig.patch.set_facecolor("#053032")
    ax.set_facecolor("#053032")
    colors = [color_map.get(i, '#ff6666') if color_map else '#ff6666' for i in range(len(values))]
    bars = ax.bar(range(len(values)), values, color=colors)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 2, str(val), ha='center', color='white', va='bottom', fontsize=8)
    ax.set_ylim(0, max(values) + 20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color("#888")
    ax.spines['bottom'].set_linewidth(1)
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    fig.tight_layout(pad=0.5)
    placeholder.pyplot(fig)
    for bar in bars:
        bar.set_edgecolor('#333')
        bar.set_linewidth(0.5)

# Initial chart
draw_bars(copied)

# Sorting execution
if start_sorting:
    if len(copied) < 2:
        st.warning("⚠️ Array must have at least 2 elements.")
    else:
        if algo == 'bubble':
            generator = bubble_sort(copied)
        elif algo == 'insertion':
            generator = insertion_sort(copied)
        elif algo == 'merge':
            generator = merge_sort(copied, 0, len(copied) - 1)
        elif algo == 'quick':
            generator = quick_sort(copied, 0, len(copied) - 1)
        elif algo == 'selection':
            generator = selection_sort(copied)
        elif algo == 'heap':
            generator = heap_sort(copied)
        for values, color_map in generator:
            draw_bars(values, color_map)
            time.sleep(delay)
        # Final green finish
        for values, color_map in generator:
            draw_bars(values, color_map)
            time.sleep(delay)
