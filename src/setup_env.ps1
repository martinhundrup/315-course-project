# Step 1: Create a virtual environment in a folder named 'venv'
python -m venv venv

# Step 2: Activate the virtual environment
& "$PWD\venv\Scripts\Activate.ps1"

# Step 3: Upgrade pip
python -m pip install --upgrade pip

# Step 4: Install dependencies from requirements.txt
pip install -r requirements.txt

# Step 5: (Optional) Run your main.py script
python main.py
