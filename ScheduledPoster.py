import os.path
import poster
    
if __name__ == "__main__":

    # checks if previous reddit account information exists
    info_exists = os.path.exists('info.txt')

    # creates the reddit account information if no previous info exists
    if not(info_exists):
        poster.init_input()

    # asks the user for their targeted subreddit
    poster.subreddit_input()
    
    
