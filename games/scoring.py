import os 
# function text of  all text files in the directory
def get_text_files(dir, required_prefix=None):
    text_files = []
    for file in os.listdir(dir):
        if file.endswith(".txt"):
            text_files.append(os.path.join(dir, file))
    res = []
    for file in text_files:
        if required_prefix is not None:
            if required_prefix not in file:
                continue
        with open(file, 'r') as f:
            res.append(f.read())
    return res

def remove_all_non_numeric(text):
    return "".join([i for i in text if i.isnumeric()])

def get_scoring(texts):
    ratings = []
    for text in texts:
        text = "".join(text.split("######################### Post Experiment Questionnaire #########################")[-1])
        text = "".join(text.split("######################### Stats #########################")[0])
        # get all ratings from text
        cur_ratings = [int(remove_all_non_numeric(i.split(": ")[-1])) for i in text.split(";") if "rating" in i]
        # remove the first rating which is the discourse rating
        cur_ratings = cur_ratings[1:]
        ratings += cur_ratings
    return {
        "average_rating": sum(ratings) / len(ratings),
        "variance": sum([(i - sum(ratings) / len(ratings))**2 for i in ratings]) / len(ratings),
        "median": sorted(ratings)[len(ratings) // 2],
    }


def dissent_ratings():
    print(get_scoring(get_text_files("polarizingDissent/", required_prefix="land")))
    print(get_scoring(get_text_files("polarizingDissent/", required_prefix="legal")))
    print(get_scoring(get_text_files("polarizingDissent/", required_prefix="tax")))

def da_rattings():
    print(get_scoring(get_text_files("devilsAdvocate/", required_prefix="without")))
    print(get_scoring(get_text_files("devilsAdvocate/", required_prefix="with")))
# dissent_ratings()
da_rattings()
