# Imperial-College-London - Marketing

This repository contains code for a Scorecard Analysis.

This analysis was done in Python for the Marketing Management Final Assignment as part of Managerial Management coursework at Imperial College London.
The analysis uses API calls to the FDA MAUDE and FAERs databases to reteive information on recalls, and product launches in medical devices, and drug related deaths in Pharma of Bayer and it's peer group.
Using the data we compute scores for Bayer and it's peers in 5 categories in Medical devices, and 5 categories in Pharma. A total score for each of the companies is computed as a weighted average.

Dependencies
Python 3.9+
requests
urllib3
pandas
numpy 
matplotlib
seaborn

Run
bash

python raw_data.py

bash

python scorecard.py
