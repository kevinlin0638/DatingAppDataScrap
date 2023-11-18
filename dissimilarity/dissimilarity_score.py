# init
import csv
import os
import json
import argparse
import random
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


from tqdm import tqdm


# 'here_for,'smoke','drink', 'match_age'
union_meta = ['scam','username','age','gender','location','ethnicity','occupation','marital_status','children','religion','sexual_orientation','sex', 'description']

scam_meta = ['email']

tqdm.pandas()

all_profile = pd.read_csv("processed_data.csv")