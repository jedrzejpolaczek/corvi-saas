# Import all routers with their absolute imports fixed
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from . import auth, users, orgs, projects, datasets, experiments, algorithms, jobs, metrics, artifacts, roi, exports, billing, features, usage, admin, health