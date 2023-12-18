# Import the library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Read the file
results = pd.read_csv("results.csv")

# Define the function to verify the category
def verify_category(file_path):
  # Use the file path to determine the category
  if "P&ID" in file_path:
    return "piping and instrumentation diagram (P&ID)"
  elif "S1_D-6" in file_path:
    return "single-line diagram"
  elif "datasheets" in file_path:
    return "data sheet"
  elif "manual" in file_path:
    return "instruction manual"
  elif "cause&effect" in file_path:
    return "cause and effect diagram"
  else:
    return None

def add_category(row):
    file_path = row[1]
    category = verify_category(file_path)
    return category

# Define the function to verify the response
def verify_response(row):
  # Get the prediction from the first column
  prediction = row[0]
  # Get the file path from the second column
  file_path = row[1]
  # Get the category from the file path
  category = verify_category(file_path)
  
  print(prediction, category)
  
  # Compare the prediction with the category
  if category.lower() in prediction.lower():
    return "Correct"
  else:
    return "Incorrect"

results['category'] = results.apply(add_category, axis=1)
# Apply the function to the results and print the results
results["verification"] = results.apply(verify_response, axis=1)

# Calculate the percentage of correct responses
correct = results[results["verification"] == "Correct"]
percentage = len(correct) / len(results) * 100

print(f"The percentage of correct responses is {percentage:.2f}%")

# # Plot the distribution by class
# plt.figure(figsize=(10, 6))
# plt.bar(results['category'].value_counts().index, results['category'].value_counts().values)
# plt.xlabel("Class")
# plt.ylabel("Count")
# plt.title("Distribution by class")
# plt.show()


# Group the results by the prediction and the verification
grouped = results.groupby(["category", "verification"]).size().reset_index(name="count")

# Plot the bar chart using seaborn
sns.barplot(x="category", y="count", hue="verification", data=grouped, palette=["green", "red"])
plt.xlabel("Class")
plt.ylabel("Count")
plt.title("Bar chart for the correctness by class")
plt.legend(labels=["Correct", "Incorrect"])
plt.show()