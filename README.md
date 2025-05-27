# Deep Vein Thrombosis Analysis

## Skills Used
- Python
- Natural Language Processing
- Regex
- Sentiment Analysis

## Background

This project was originally created for my internship at Knight Cancer Research Institute. A graduate student reached out and had 4300 dictated radiology reports that contained diagnsoses for Deep Vein Thrombosis (DVT). He need an algorithm to quickly sort through the text file and provide him with an output that stated if Deep Vein Thrombosis was found within each scan. To stay compliant with HIPAA, I did not include the original text file that I used for this project and instead asked ChatGPT to generate at least 25 records of fake data to show how the code would work. The file ChatGPT_generated_fake_DVT_data.txt contains fake ChatGPT generated data. No real patient data is shared for this project.

## Initial Approach - Sentiment Analysis 

I researched various methods to analyzing large batches of text at a time. I came across the Natural Language Toolkit (NLTK) Library in Python which is used to perform sentiment analysis at a high accuracy on large batches of text data. One common application of Sentiment Analysis is to quickly analyze reviews for online products and determine the tone of the reviews. I had hoped that I could use this method to determine the tone of the radiology reports in hopes that the tone would be associated with a positive or negative diagnosis. Alas that was not the case, but I chose to include my code in this repository to demonstrate the potential application to medical data. You can read more about NLTK and Sentiment Analysis [here] (https://www.datacamp.com/tutorial/text-analytics-beginners-nltk) and you can see my code in the file called DVT_Project_Python_Sentiment.py.

## Final Approach - Regex

Once I had determined that Sentiment Analysis was not the approach I wanted for this project, I turned to Regex. I decided to continue the project in Python, despite R being my stronger language, so that I could learn more about Python. Through many iterations, I determined an extensive list of keywords that I used to find a diagnosis within the text and then look around the keyword to find words that indicated a positive diagnosis. I also checked for the presence of negating words within each phrase. If there were negating words, my algorithm considered it to be a negative diagnosis. If there were no negating words, my algorithm considered it to be a positive diagnosis. Since multiple body parts were evaluated in each scan, in order for there to be an overall positive diagnosis for DVT, each scan only needed one positive diagnosis to be considered a positive diagnosis regardless of the number of negative diagnoses. 

## Conclusions

My final algorithm provided 98% accuracy on over 4300 dictacted text records. I evaluated this by outputing an Excel spreadsheet containing a random sample of 200 of the dictated reports and evaluating each one of them manually and comparing that to the algorithms output.
