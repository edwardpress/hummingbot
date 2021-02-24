# 1) Clean intermediate and compiled files from Cython compilation.
./clean

# 2) Install
./install

# 3) Deactivate old conda environment
conda deactivate

# 4) Activate conda environment
conda activate hummingbot

# 5) Compile
./compile

# 6) Run Hummingbot
bin/hummingbot.py

