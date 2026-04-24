DESCRIPTION
======================
This project builds a dynamic citation network for Computer Science papers using the OpenAlex API and visualizes it with D3.js.

The system first collects citation data, then cleans and processes it into a graph structure. It applies temporal weighting and clustering to capture how research fields evolve over time. Finally, it provides an interactive visualization where users can explore both global trends and individual papers.

The goal of this project is to help users better understand the growth of research areas and the role of individual papers in the citation network.


INSTALLATION
======================
1. Make sure you have Python 3 installed.

2. Install required Python packages (if needed):
   pip install pandas numpy requests

3. The final output is an HTML file that runs in a browser.


EXECUTION
======================
Step 1: Collect raw data by using 'python build_init_data.py'. (You can change the dataset size by modifying TOTAL_PAPERS in the code.)

Step 2: Clean the dataset by using 'python clean_data.py'
   
Step 3: Prepare visualization data by using 'python prepare_D3_graph_data.py'

Step 4: Run visualization by run 'python -m http.server 8000' in your terminal and open 'd3_graph.html' in your 'http://localhost:8000' web browser.


DEMO VIDEO
======================

