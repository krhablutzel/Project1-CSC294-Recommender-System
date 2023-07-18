# Project 1
### First (of two) course projects

Recalling that the purpose of the projects is to build things that use multiple 
concepts, in this project, you will be thinking about dimension reduction in the context 
of recommender systems. 

This project has 4 parts: choosing a dataset for a recommender task, designing a 
recommender system using a dimension reduction technique, testing your system on 
experts, and finally documenting your work. 

## Part 1 - Choosing a dataset
A recommendation system takes collections of user ratings of items (ie. movies/books/stores) 
and _recommends_ the next item that a particular user would be interested in. 

Choose a dataset for this project that interests you. Your dataset must contain 
**numerical ratings of items**, and you should have a clear idea of how the ratings 
connect to individual users. (Hint: You may need to do some data transformations, 
but ultimately _users_ should be your observations). 

I would recommend looking for data in one of these three places:
* The [UCI repository](http://archive.ics.uci.edu/ml/index.php) 
* [fivethirtyeight's data repository](https://github.com/fivethirtyeight/data)
* [Kaggle](https://www.kaggle.com/search?q=recommendation+in%3Adatasets)

## Part 2 - Designing a recommender system
In a recommender system, we want to make recommendations to users. So the output 
from our recommender system will be of a similar shape to our original data, with 
users as the observations and items as the variables. 

So far in class, we have used dimension reduction to transport our data from 
a higher dimension down to a lower one. We have yet to do much pushing our lower 
dimensional approximation back to the original dimensional space. One can think 
of a recommender system as the process of dimension reducing ratings data and then 
pushing the lower dimension approximation back to the original space. 

In this part, design a recommendation system that recommends 3 items to users that 
they have not yet rated, but that your system believes that they will rate highly. 
Your system should use either PCA (from `sklearn`) or SVD (from `numpy`) as a 
central element of your recommender system. Your code file should be called 
`project1.py`.

You should also design two kinds of unit tests for your recommender system. The 
first type of unit tests should be 'surface' level, checking the size and type 
of your output. The second kind of unit tests should check that you are not 
giving recommendations for items that the user has already rated. Your test 
file should be called `test_project1.py`. 

## Part 3 - Testing your system on experts
For this part, you will be evaluating the quality of the system's recommendations. 
Select two users in the dataset, and note the items they have rated so far. 
Construct narratives for each of these users about what the "latent" or hidden 
preferences of these users are. 

Now look at what your system recommends. Do these results surprise you? Why or 
why not? If possible, ask a friend or two to comment on the quality of these 
recommendations. 

## Part 4 - Documenting and submitting your work
A critical part of our work is documenting what we do. To that end, the last part of 
any project will be writing a coherent report on what you did. These reports should 
**not** feel like a listing of the parts, but rather seek to tell a story of the work 
that you have done and the resulting product. 

For this project, your report should include:
* An explanation of the recommender task that you are investigating and why you are 
  interested in it
* Information about your dataset and why you selected it
* An introduction to your recommender system, including how it works, whether you use 
  PCA or SVD (and why!), and how it selects three _new_ recommendations 
* A brief discussion about the quality of the recommendations for the two selected 
  users
  
Your report should be self-contained, meaning that all necessary figures should be contained 
within the documentation. You should also include any and all resources (beyond common 
materials for this class) at the end of your report. The report should be called `report-p1.pdf` 
and be a PDF. Use 1-inch margins, and double spacing for text in paragraphs. There are no 
page requirements or limits; but if your report is less than 3 pages or more than 8, we 
should check in about it. 

Also, please include any and all code with your report, as well as documentation 
demonstrating that your tests have passed both locally and on travis. 

## Rubric
* 15 points for discussion of data, explanation of the specific recommender task, 
  and the general context for this data
* 35 points for the implementation and discussion of the recommender system
* 15 points for unit tests for the recommender system
* 20 points for examination of recommendations for two users
* 15 points for overall report form, cohesion, and written presentation

## Reminders
* Don't forget to create a `.gitignore` for any notebook checkpoints that you create. 
* Any import statements should be at the top of your python files or in the first 
code block of a notebook. 
