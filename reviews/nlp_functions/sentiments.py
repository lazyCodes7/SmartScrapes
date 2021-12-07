# Necessary Imports
import pandas as pd
from expertai.nlapi.cloud.client import ExpertAiClient
import os
from tweets.preprocess.preprocess_functions import *
from dotenv import load_dotenv
load_dotenv() 
os.environ["EAI_USERNAME"] = os.environ['EMAIL']
os.environ["EAI_PASSWORD"] = os.environ['PASSWORD']

# Getting the user traits 
def getUserTraits(df):
    # Instantiate the client
    client = ExpertAiClient()
    taxonomy = 'emotional-traits'
    language = 'en'
    headers=""
    reviews = ""
    taxonomy_b = 'behavioral-traits'
    user_review_list = []
    emotional_traits = []
    big_5_traits = []
    big_5_trait_rate = []
    final_traits = []
    preprocessor = Preprocessor()

    # Going through the review headers and reviews itself
    try:
        for header in df['Header']:
            headers+=header
        for review in df['Review']:
            reviews+=review
        user_review_list = [headers,reviews]
        for i in range(2):
            text = user_review_list[i]
            # Getting the emotions and behavorial traits
            output = client.classification(body={"document": {"text": text}}, params={'taxonomy': taxonomy, 'language': language})
            output_b = client.classification(body={"document": {"text": text}}, params={'taxonomy': taxonomy, 'language': language})
            for category in output_b.categories:
                big_5_traits.append(category.hierarchy[0])
                big_5_trait_rate.append(category.hierarchy[1])
                final_traits.append(category.hierarchy[2])
            for category in output.categories:
                emotional_traits.append(category.hierarchy[1])
        
        # Saving the traits as found into a dict
        e_dict = {
            "emotional_traits" : emotional_traits
        }
        b_dict = {
            "big_5_traits":big_5_traits,
            "big_5_trait_rate" : big_5_trait_rate,
            "final_traits" : final_traits
        
        }

        # Converting it into a dataframe
        b_df = pd.DataFrame(b_dict)
        b_df['big_5_trait_rate'] = b_df['big_5_trait_rate'].apply(cleanTraitRate)

        # Returning the dataframe
        reviews_df = pd.DataFrame(e_dict)
    except:

        # Except block if reviews for a company were not found. Then going with a default overview
        emotional_traits = ['Repulsion','Hatred','Happiness','Excitement','Love','Happiness','Excitement']
        big_5_traits = ['Sociality', 'Sociality']
        big_5_trait_rate = ['Sociality low', 'Sociality fair']
        final_traits = ['Asociality', 'Seriousness']
        e_dict = {
            "emotional_traits" : emotional_traits
        }


        b_dict = {
            "big_5_traits":big_5_traits,
            "big_5_trait_rate" : big_5_trait_rate,
            "final_traits" : final_traits
        
        }
        reviews_df = pd.DataFrame(e_dict)
        b_df = pd.DataFrame(b_dict)
        b_df['big_5_trait_rate'] = b_df['big_5_trait_rate'].apply(preprocessor.cleanTraitRate)

        # Return the default dataframe with some sample data
    return (reviews_df,b_df)