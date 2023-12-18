import pandas as pd
import time
from vertexai.preview.generative_models import GenerativeModel, Part, Image

def generate_text(project_id: str, location: str, images_dir : str) -> pd.DataFrame:
    import vertexai
    import os
    results = []
    
    vertexai.init(project=project_id, location=location)
    def execute(file :str):
        multimodal_model = GenerativeModel("gemini-pro-vision")
        response = multimodal_model.generate_content(
            [
                "What kind of document is this? Be as specific with the category as possible. Reply like this: This is {0}. It is used for {1}",
                Part.from_image(
                Image.load_from_file(file)
                ),
            ]
        )
        # This helps not to surpass the default quota calls / minute
        time.sleep(10)
        print(response.text)
        return response.text.split('.')[0].replace("This is a ", "")
    
    for dir,_,files in os.walk(images_dir):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png'):
               resp = execute(os.path.join(dir, file))
               result = {
                   "response": resp,
                   "file":os.path.join(dir, file)
               }
               results.append(result)

    return pd.DataFrame(results)

project_id = "wave-record"
location = "us-central1"

pid_dir = './datasets/P&ID-4/train'
schematics_dir = './datasets/S1_D-6/valid'
datasheets_dir = './datasets/datasheets'
logic_diagrams_dir = './datasets/logic_diagrams'
manuals_dir = './datasets/manual'
cause_and_effect_dir = './datasets/cause&effect'

dirs = [pid_dir, schematics_dir, datasheets_dir, 
        logic_diagrams_dir, manuals_dir, cause_and_effect_dir]

merged_dfs : list[pd.DataFrame]= []

for dir in dirs:
    df = generate_text(project_id, location, dir)
    merged_dfs.append(df)
    
pd.concat(merged_dfs).to_csv("./results.csv", index=None)
    