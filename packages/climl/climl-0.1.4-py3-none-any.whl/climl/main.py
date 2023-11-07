import requests
import typer
import os
from rich import print

app = typer.Typer()

@app.command()
def main():

    options = ['Y', 'y', 'N', 'n']
    commercial_url = "https://curly-hill-cf61.climl.workers.dev/"
    personal_url = "https://worker-lingering-wildflower-b69e.climl.workers.dev/"

    print("Welcome to CLIML!\n")

    print("CLIML enables you to rapidly automate the creation of powerful supervised learning models:")
    print("- Auto-detection for regression/classification tasks.")
    print("- Automated hyperparameter tuning and model selection.")
    print("- Train models as quickly (or as extensively) as you like.")
    print("- Make easy predictions and output them to a CSV file.")
    print("- Beautifully formatted --help if you get stuck.\n")

    print("Use of CLIML requires a plan. Both plans allow you to train an unlimited amount of models and make an unlimited amount of predictions.\n")

    print("- Commercial Plan ($19/month): for business/commercial use")
    print("- Personal Plan (FREE): for personal and educational projects\n")

    print("If you have any questions, please email hello@climl.com for assistance.\n")

    script_path = os.path.abspath(__file__)
    activated_code = """
import typer
import pickle
import pandas as pd
from AutoClean import AutoClean
from flaml import AutoML
import logging
from sklearn.preprocessing import LabelEncoder
from rich import print
import platform
import subprocess


app = typer.Typer(help="Rapidly Automate the Creation of Powerful Supervised Learning Models")


@app.command()
def train(file: str = typer.Argument(default=...,help="The CSV file you want to train a model on.",show_default=False), 
         time: int = typer.Argument(default=..., help="How many seconds to spend on training your model.",show_default=False)) :
    '''
    Train a model on any number of input columns and a final output column.
    
    The columns can contain numerical data and some string categories.

    CLIML will detect and train a classification or a regression model respectively.
    '''
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

    logging.getLogger('flaml.automl.logger').addHandler(NullHandler())

    print(":file_folder: Loading File")
    df = pd.read_csv(file)
    print(":white_check_mark: File Loaded")
    output = df.columns[-1]
    model = AutoML()
    print(":hourglass_flowing_sand: Training Model for ",time," Seconds")
    if df[output].dtype == 'object' :
        le = LabelEncoder()
        df[output] = le.fit_transform(df[output])
        model.fit(df.iloc[:, :-1],
                  df.iloc[:, -1],
                  mlflow_logging=False,
                  task='classification',
                  time_budget = time)
        df[output] = le.inverse_transform(df[output])
        print(":white_check_mark: Classification Model Trained")  
    else :
        model.fit(df.iloc[:, :-1],
                  df.iloc[:, -1],
                  mlflow_logging=False,
                  task='regression',
                  time_budget = time)
        print(":white_check_mark: Regression Model Trained")

    model_name = file.rsplit('.', 1)[0]
    data_to_pickle = {
    'df': df,
    'model': model
    }

    print(":file_cabinet: Saving Model")
    
    with open(model_name+'.climl', "wb") as f:
        pickle.dump(data_to_pickle, f, pickle.HIGHEST_PROTOCOL)
    print(":white_check_mark: Model Saved as", model_name+".climl")

    print(":information_desk_person: Model Information:")
    print(model_name+".climl is a:", model.best_estimator)
    print("Hyperparameter Configurations:", model.best_config)
    print("Model Accuracy:", round((1-model.best_loss), 2))
    print("Best Training Run Discovered:", round(model.time_to_find_best_model, 2),"Seconds")


@app.command()
def inspect(file: str = typer.Argument(default=...,help="The model you want to inspect.",show_default=False)) :
    '''
    Display model type, hyperparameters, accuracy, and training speed to the terminal.
    '''    
    print(":file_folder: Loading Model")

    with open(file, 'rb') as f:
        data_to_pickle = pickle.load(f)
    print(":white_check_mark: Model Loaded")

    print(":magnifying_glass_tilted_left: Inspecting Model")

    model = data_to_pickle['model']
    
    print(":information_desk_person: Model Information:")
    print(file," is a:", model.best_estimator)
    print("Hyperparameter Configurations:", model.best_config)
    print("Model Accuracy:", round((1-model.best_loss), 2))
    print("Best Training Run Discovered:", round(model.time_to_find_best_model, 2),"Seconds")


@app.command()
def predict(file: str = typer.Argument(default=...,help="The file containing the inputs you want to predict.",show_default=False), 
         model: str = typer.Argument(default=...,help="The model you've trained with these input headers.",show_default=False)) :
    '''
    Display predictions to the command line and insert them as a new column in the CSV file containing your test dataset.

    '''    
    print(":file_folder: Loading Test Data")

    df = pd.read_csv(file)

    print(":white_check_mark: Test Data Loaded")

    print(":file_folder: Loading Model")

    with open(model, 'rb') as f:
        data_to_pickle = pickle.load(f)

    print(":white_check_mark: Model Loaded")

    training_df = data_to_pickle['df']
    autoML_model = data_to_pickle['model']
    output = training_df.columns[-1]

    print(":thinking_face: Generating Predictions")
    if training_df[output].dtype == 'object' :
        le = LabelEncoder()
        training_df[output] = le.fit_transform(training_df[output])
        unique_labels = le.classes_
        dictionary = {encoded: original for encoded, original in enumerate(unique_labels)}
        list = autoML_model.predict(df)
        new_list = [dictionary[item] for item in list]

    else :
        new_list = autoML_model.predict(df)

    df['Predicted Output'] = new_list
    df.to_csv(file, index=False)
    print(":white_question_mark: Model Predictions:")
    print(new_list)

if __name__ == "__main__":
    app()  
    """

    user_input = ""
    while user_input not in options :
        user_input = typer.prompt("Have you already activated your chosen plan via the CLIML.com website?\n(Y/n) ")

    if user_input in ['Y', 'y']:

        user_input = ""
        while user_input not in options :
            user_input = typer.prompt("Do you have a Commercial Plan? (You need this if you plan on using CLIML for business or commercial activities.)\n(Y/n) ")
        
        if user_input in ['Y', 'y']:     
            commercialurl_check = typer.prompt("Enter your the email you used for sign-up and billing in the checkout portal ")
            response = requests.post(commercial_url, data=commercialurl_check)
            if response.text == "True":
                with open(script_path, "w") as file:
                       file.write(activated_code)
                print("CLIML activated. Enter $ climl --help to get started!")
                raise typer.Exit() 
            else:
                print("Commercial Plan account not found. Maybe you entered the wrong email? Try again by entering $ CLIML in the command line. Contact hello@climl.com if you think there is an error.")
                raise typer.Exit()
        else :
            user_input = ""
            while user_input not in options :
                user_input = typer.prompt("Do you have a Personal Plan?\n(Y/n) ")
            if user_input in ['Y', 'y']:     
                personalurl_check = typer.prompt("Enter your the email you used to activate your account on the website")
                response = requests.post(personal_url, data=personalurl_check)
                if response.text == "True":
                    with open(script_path, "w") as file:
                        file.write(activated_code)
                    print("CLIML activated. Enter $ climl --help to get started!")
                    raise typer.Exit() ### ACTIVATE, PRINT ACTIVATED, ENTER CLIML --help TO FIND MORE, QUIT
                else:
                    print("Personal Plan account not found. Maybe you entered the wrong email? Try again by entering $ CLIML in the command line. Contact hello@climl.com if you think there is an error.")
                    raise typer.Exit()
            else :
                print("You need to activate either a Commercial or a Personal Plan via the website to use CLIML.")
                print("If you need help, email hello@climl.com")
                typer.launch("https://climl.com")
                raise typer.Exit()
    else :
        typer.launch("https://climl.com")
        raise typer.Exit()

if __name__ == "__main__":
    app()






