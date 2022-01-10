
from flask import Flask, render_template, request, flash, redirect, url_for
import numpy as np
import pandas as pd
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'


app = Flask(__name__)
app.secret_key = "wjdghks3#"


# Movie overview data & matrix
# cosine_sim1_1 = np.load('matrixs_meta/cosine_sim1_1_overview.npy')
# cosine_sim1_2 = np.load('matrixs_meta/cosine_sim1_2_overview.npy')
# cosine_sim = np.concatenate((cosine_sim1_1, cosine_sim1_2))
# print(cosine_sim.shape)



# indices = pd.read_csv('matrixs_meta/indices.csv')
# indices.set_index('title', inplace = True)
# print(indices.loc['The Dark Knight Rises'][0])


# Movie metadata & matrix
# cosine_sim2_1 = np.load('matrixs_meta/cosine_sim2_1_metadata.npy')
# cosine_sim2_2 = np.load('matrixs_meta/cosine_sim2_2_metadata.npy')
# cosine_sim2 = np.concatenate((cosine_sim2_1, cosine_sim2_2))
# print(cosine_sim.shape)


# indices2 = pd.read_csv('matrixs_meta/indices2.csv')
# indices2.set_index('title_x', inplace = True)

titles = pd.read_csv('matrixs_meta/titles.csv')
lower_title = [i.lower() for i in titles['title']]
original_titles = [i for i in titles['title']]


@app.route("/", methods = ["POST", "GET"])
def spec_movie0():
    if request.method == "GET":
        return render_template("index_movie0.html")
    else:
        if request.form.get('choice') == 'select':
            return redirect(url_for('spec_movie2'))
        else:
            return redirect(url_for('spec_movie1'))

    

@app.route("/spec_movie1", methods = ["POST", "GET"])
def spec_movie1():
    return render_template("index_movie1.html")

@app.route("/spec_movie2", methods = ["POST", "GET"])
def spec_movie2():
    return render_template("index_movie2.html")

# @app.route("/spec_movie3/<some_list>", methods = ["POST", "GET"])
# def spec_movie3(some_list):
#     if request.method == "GET":

#         similar_titles = []
#         typed_keys = some_list.split("_")
#         for movie in original_titles:
#             for key in typed_keys:
#                 if key.lower() in movie.lower():
#                     similar_titles.append(movie)
#         similar_titles = list(set(similar_titles))
        
#         # return render_template("index_movie3.html", similar_titles = similar_titles,len = len(similar_titles))
#         return render_template("index_movie0.html")

@app.route("/spec_movie4", methods = ["POST", "GET"])
def spec_movie4():
    return render_template("index_movie4.html")
     


@app.route("/form2", methods = ["POST"])
def form2():

    # Bring personal spec from the form
    try:
        typed_name = request.form.get('name')
    except:
        pass
    try:
        movie_name = request.form.get('movie_sample')
    except:
        pass

    if typed_name:
        if typed_name.lower() in lower_title:

            movie_name = original_titles[lower_title.index(typed_name.lower())]
        else:
            # similar_titles = []
            # typed_keys = typed_name.split(" ")
            # for movie in original_titles:
            #     for key in typed_keys:
            #         if key.lower() in movie.lower():
            #             similar_titles.append(movie)
            # similar_titles = list(set(similar_titles))
            # comma_separated = ','.join(similar_titles)


            # typed_name = typed_name.replace(" ", "_")
            # return redirect(url_for('spec_movie3', some_list=typed_name))

            #flash("We don't have the movie title in our database. <br>Please check spelling and spaces", 'fail')
            return redirect(url_for('spec_movie4'))

    algo = request.form.get('filter')

    # # Function that takes in movie overview as input and outputs most similar movies
    # def get_recommendations(title, cosine_sim=cosine_sim):
    #     # Get the index of the movie that matches the title
    #     idx = indices.loc[title][0]

    #     # Get the pairwsie similarity scores of all movies with that movie
    #     sim_scores = list(enumerate(cosine_sim[idx]))

    #     # Sort the movies based on the similarity scores
    #     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    #     # Get the scores of the 10 most similar movies
    #     sim_scores = sim_scores[1:11]
        

    #     # Get the movie indices
    #     movie_indices = [i[0] for i in sim_scores]

    #     # Return the top 10 most similar movies
    #     return titles.iloc[movie_indices], sim_scores


    # # Function that takes in movie metadata as input and outputs most similar movies
    # def get_recommendations2(title, cosine_sim=cosine_sim2):
    #     # Get the index of the movie that matches the title
    #     idx = indices2.loc[title][0]

    #     # Get the pairwsie similarity scores of all movies with that movie
    #     sim_scores = list(enumerate(cosine_sim2[idx]))

    #     # Sort the movies based on the similarity scores
    #     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    #     # Get the scores of the 10 most similar movies
    #     sim_scores = sim_scores[1:11]

    #     # Get the movie indices
    #     movie_indices = [i[0] for i in sim_scores]

    #     # Return the top 10 most similar movies
    #     return titles.iloc[movie_indices], sim_scores
    
    if algo == 'Plot description':

        cosine_sim1_1 = np.load('matrixs_meta/cosine_sim1_1_overview.npy')
        cosine_sim1_2 = np.load('matrixs_meta/cosine_sim1_2_overview.npy')
        cosine_sim = np.concatenate((cosine_sim1_1, cosine_sim1_2))

        indices = pd.read_csv('matrixs_meta/indices.csv')
        indices.set_index('title', inplace = True)

        # Function that takes in movie overview as input and outputs most similar movies
        def get_recommendations(title, cosine_sim=cosine_sim):
            # Get the index of the movie that matches the title
            idx = indices.loc[title][0]

            # Get the pairwsie similarity scores of all movies with that movie
            sim_scores = list(enumerate(cosine_sim[idx]))

            # Sort the movies based on the similarity scores
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            # Get the scores of the 10 most similar movies
            sim_scores = sim_scores[1:11]
            

            # Get the movie indices
            movie_indices = [i[0] for i in sim_scores]

            # Return the top 10 most similar movies
            return titles.iloc[movie_indices], sim_scores


        results, sim_scores = get_recommendations(movie_name)[0]['title'], get_recommendations(movie_name)[1]
        # to make up similarity gap between plot description and metadata
        sim_scores = [int(i[1]*150) for i in sim_scores]  
    else:

        cosine_sim2_1 = np.load('matrixs_meta/cosine_sim2_1_metadata.npy')
        cosine_sim2_2 = np.load('matrixs_meta/cosine_sim2_2_metadata.npy')
        cosine_sim2 = np.concatenate((cosine_sim2_1, cosine_sim2_2))

        indices2 = pd.read_csv('matrixs_meta/indices2.csv')
        indices2.set_index('title_x', inplace = True)

        # Function that takes in movie metadata as input and outputs most similar movies
        def get_recommendations2(title, cosine_sim=cosine_sim2):
            # Get the index of the movie that matches the title
            idx = indices2.loc[title][0]

            # Get the pairwsie similarity scores of all movies with that movie
            sim_scores = list(enumerate(cosine_sim2[idx]))

            # Sort the movies based on the similarity scores
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            # Get the scores of the 10 most similar movies
            sim_scores = sim_scores[1:11]

            # Get the movie indices
            movie_indices = [i[0] for i in sim_scores]

            # Return the top 10 most similar movies
            return titles.iloc[movie_indices], sim_scores



        results, sim_scores = get_recommendations2(movie_name)[0]['title'], get_recommendations2(movie_name)[1]
        sim_scores = [int(i[1]*100) for i in sim_scores]

    results = [i for i in results]
    top1 = results[0]
    


    #print(results2)
    above50 = 0
    above30 = 0
    for i in sim_scores:
        if i > 49:
            above50 += 1 
        elif i > 19:
            above30 += 1 
        else:
            pass

    


    return render_template("movie_visualization.html", 
                            movie_name = movie_name, 
                            algo = algo,
                            results = results,
                            sim_scores = sim_scores,
                            len = len(results),
                            above50 = above50,
                            above30 = above30,
                            top1 = top1)
                                       
                                    
                                        
                                          


if __name__ == '__main__':
    #os.environ['FLASK_ENV'] = 'development'
    app.run(debug = True)





   

