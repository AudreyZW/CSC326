    #integration with frontend
    scores_list = bot.get_docid_score() #get a dictionary of the scores as the value and the doc_id as the key
    sorted_scores = sorted(scores_list.items(), key=operator.itemgetter(1), reverse=True) #sort the dictionary in descending order by value
    list_of_url_ids = [score[0] for score in sorted_scores]#get only the doc_id
    bot._urls_in_score_order = [bot._docid_url[i] for i in list_of_url_ids]#get a list of corresponding doc urls for doc ids
