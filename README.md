# Sweepstakes Entry Bot

A program to enter into sweepstakes automatically for a list of email addresses. 


```form_extractor.py``` - Contains all the code to extract forms from a website, specifically forms that can be submitted.

```custom_sweepstakes.py``` - Contains the class & functions to submit a custom sweepstakes entry after checking the deadline, for the maximum number of entries allowed. The original file is overwritten with the updated list & expired URLs are printed.

```add_new_urls.py``` - Updates the file containing the URLs with more sweepstake entry URLs!

The functions to get some website-related / personal information have been obscured in files. These can be customized in a file **custom_website_functions.py**. 
Functions used here as custom_website_functions.<function_name> are:

- ```get_custom_form(form_details=form_details, name=name, email=email)``` : Returns the sweepstakes entry form filled out with name & email address modified.

- ```check_success(website_return_value=website_return_value)``` : Returns true if the website has successfully processed the entry, using the endpoint that's returned after your submission.

- ```is_before_deadline(results)``` : Returns true if the sweepstake is still before the deadline, using the parsed webpage results.

- ```get_entry_limit(results)``` : Returns maximum number of entries allowed for the sweepstake, using the parsed webpage results.
                                                        
A file **myconstants.py** can be used to list the constants in caps. Logging functions have been commented out, but can be customized as needed.
