import sys
print(sys.path)

try:
    import matplotlib.pyplot as plt
    print("matplotlib imported successfully!")
except ModuleNotFoundError as e:
    print(e)
