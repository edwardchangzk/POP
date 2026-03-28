#Streamlit App

#Importing necessary libraries
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

#User class
class User:
    def __init__(self,userID, genrePref):
        self.userID = userID
        self.genrePref = genrePref
        self.watchHistory = []

    def watch(self, movie):
        if movie not in self.watchHistory:
            self.watchHistory.append(movie)

    def rating(self, recommendation, movie, rating):
        recommendation.addRatings(self, movie, rating)

#Movies Class
class Movies:
    def __init__(self, movieID, movieTitle, movieGenre, releaseYear):
        self.movieID = movieID
        self.movieTitle = movieTitle
        self.movieGenre = movieGenre
        self.releaseYear = releaseYear

    def getMovieInfo(self):
        return (f"Movie Title:{self.movieTitle}, Movie Genre: {self.movieGenre},"
                f" Release Date:{self.releaseYear}")

#MRS class
class MRS:
    def __init__(self):
        self.movieRatings = {}
        self.movies = []

    #Admin CRUD
    #Adding new movies into database
    def addMovies(self, movie):
        self.movies.append(movie)

    #Removing  movies from database
    def deleteMovies(self, movieID):
        movie = self.getMovieID(movieID)
        if movie:
            self.movies.remove(movie)

            for userID in self.movieRatings:
                if movieID in self.movieRatings[userID]:
                    del self.movieRatings[userID][movieID]
            return True
        return False

    #Updating existing movies in the database
    def updateMovies(self, movieID, updTitle, updGenre, updYear):
        movie = self.getMovieID(movieID)
        if movie:
            movie.movieTitle = updTitle
            movie.movieGenre = updGenre
            movie.movieYear = updYear
            return True
        return False

    def addRatings(self, user, movie, rating):
        if user.userID not in self.movieRatings:
            self.movieRatings[user.userID] = {}

        self.movieRatings[user.userID][movie.movieID] = rating

    #Calculating Average Movie Ratings
    def AvgMovieRatings(self, movie):
        count = 0
        totalRating = 0

        for userRating in self.movieRatings.values():
            if movie.movieID in userRating:
                totalRating += userRating[movie.movieID]
                count += 1

        if count == 0:
            return 0
        return totalRating / count

    #Recommending unwatched movies for Users
    def moviesRec(self, user):
        movieRecommendations = []
        watchedMovie = [movie.movieID for movie in user.watchHistory]

        #Only providing movies User haven't watched by genre
        for movie in self.movies:
            if movie.movieID not in watchedMovie and movie.movieGenre in user.genrePref:
                avgRating = self.AvgMovieRatings(movie)
                movieRecommendations.append((movie,avgRating))

        #Sorting recommended movies based on rating
        movieRecommendations.sort(key=lambda x: x[1], reverse=True)
        return movieRecommendations

    #Finding Movie ID
    def getMovieID(self, movieID):
        for movie in self.movies:
            if movie.movieID == movieID:
                return movie
        return None

    #Function to search movie title
    def searchTitles(self, title):
        search = []

        for movies in self.movies:
            if title.lower() in movies.movieTitle.lower():
                search.append(movies)
        return search

    #Search through genres
    def searchGenres(self, genre):
        search = []

        for genreResult in self.movies:
            if genreResult.movieGenre.lower() == genre.lower():
                search.append(genreResult)
        return search

    #Search by year
    def searchYears(self, year):
        search = []

        for moviesYr in self.movies:
            if moviesYr.releaseYear == year:
                search.append(moviesYr)
        return search

    #Finding the most popular genre
    def popularGenre(self):
        genreType = {}

        #Identifying which movie belongs to which genre
        for movie in self.movies:
            if movie.movieGenre not in genreType:
                genreType[movie.movieGenre] = genreType.get(movie.movieGenre, 0) + 1

            if len(genreType) == 0:
                return None

        #Genre with the highest count
        mostPopularGenre = max(genreType, key=lambda x: genreType[x])
        return mostPopularGenre

    #The most trending movies
    def trendingMovies(self):
        movieAvgRating = []

        for movie in self.movies:
            avgRating = self.AvgMovieRatings(movie)
            watch_Count = watchCount(movie.movieID)
            trendScore = avgRating + watch_Count
            movieAvgRating.append((movie, trendScore))

        #Identifying top 3 movies
        movieAvgRating.sort(key=lambda x: x[1], reverse=True)
        return movieAvgRating[:3]

#TODO ----- System Creation -----
def main():
    mrs = MRS()

    #Adding Movies
    mrs.addMovies(Movies(101, "Peaky Blinders", "Drama", 2013))
    mrs.addMovies(Movies(202, "KPop Demon Hunters", "Musical", 2024))
    mrs.addMovies(Movies(303, "War Machines", "Action", 2017))
    mrs.addMovies(Movies(404, "Wake Up Dead Man", "Comedy", 2025))
    mrs.addMovies(Movies(505, "Godzilla", "Action", 2017))
    mrs.addMovies(Movies(606, "Wallace & Gromit", "Comedy", 2024))
    mrs.addMovies(Movies(707, "Red Notice", "Action", 2021))
    mrs.addMovies(Movies(808, "Bird Box", "Action", 2018))
    mrs.addMovies(Movies(909, "The Gray Man", "Action", 2022))
    mrs.addMovies(Movies(1010, "Leave the World Behind", "Sci-Fi", 2023))

    return mrs

#Default Accounts
acct = {
    "Jeff":{
        "password": "123",
        "role": "user",
        "userID": 101,
        "preferences":["Comedy", "Sci-Fi"]
    },
    "Bob":{
        "password": "456",
        "role": "user",
        "userID": 202,
        "preferences":["Action", "Drama"]
    },
    "Anna":{
        "password": "789",
        "role": "user",
        "userID": 303,
        "preferences":["Action", "Musical"]
    },
    "Admin":{
        "password": "999",
        "role": "admin",
        "userID": 000,
        "preferences": []
    }
}

#Creating sessions
if "currentPage" not in st.session_state:
    st.session_state.currentPage = "loginPage"

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

if "login" not in st.session_state:
    st.session_state.login = False

if "mrs" not in st.session_state:
    st.session_state.mrs = main()

if "users" not in st.session_state:
    st.session_state.users = {}

if "currentUser" not in st.session_state:
    st.session_state.currentUser = None

mrs = st.session_state.mrs

#Showing All Available Movies in Table form
def availableMovies():
    df = []

    for movie in mrs.movies:
        df.append({
            "Movie ID": movie.movieID,
            "Movie Title": movie.movieTitle,
            "Movie Genre": movie.movieGenre,
            "Release Year": movie.releaseYear,
            "Average Rating": f"{mrs.AvgMovieRatings(movie):.2f}"
        })
    return pd.DataFrame(df)

#Personalized Movie Recommendation Based on User in Table form
def persRecommendations(recommendation):
    df = []

    for movie, avgRating in recommendation:
        df.append({
            "Movie Title": movie.movieTitle,
            "Movie Genre": movie.movieGenre,
            "Release Year": movie.releaseYear,
            "Average Rating": f"{avgRating:.2f}"
        })
    return pd.DataFrame(df)

#Searching movies based on titles or genres
def searchMovies(mrs, search):
    df = []

    for movie in search:
        df.append({
            "Movie ID": movie.movieID,
            "Movie Title": movie.movieTitle,
            "Movie Genre": movie.movieGenre,
            "Release Year": movie.releaseYear,
            "Average Rating": f"{mrs.AvgMovieRatings(movie):.2f}"
        })
    return pd.DataFrame(df)

#Analyzing watch history of users
def watchHistory(user):
    df = []

    for movies in user.watchHistory:
        df.append({
            "Movie ID": movies.movieID,
            "Movie Title": movies.movieTitle,
            "Movie Genre": movies.movieGenre,
            "Release Year": movies.releaseYear
        })
    return pd.DataFrame(df)

#Rating Table
def ratingTable(userID):
    df = []

    if userID in mrs.movieRatings:
        for movieID, mvRating in mrs.movieRatings[userID].items():
            movies = mrs.getMovieID(movieID)
            if movies is not None:
                df.append({
                    "Movie ID": movies.movieID,
                    "Movie Title": movies.movieTitle,
                    "Movie Genre": movies.movieGenre,
                    "Movie Rating": f"{mvRating:.2f}"
                })
    return pd.DataFrame(df)

#Analyzing user watch count
def watchCount(movieID):
    count = 0
    for user in st.session_state.users.values():
        for movie in user.watchHistory:
            if movie.movieID == movieID:
                count += 1
    return count

#Identifying Most watched movies
def mostWatched():
    df = []

    for movies in mrs.movies:
        df.append({
            "Movie Title": movies.movieTitle,
            "Movie Genre": movies.movieGenre,
            "Watch Count": watchCount(movies.movieID)
        })
    return pd.DataFrame(df)

#Identifying Top Users
def topActive():
    df = []

    for username, user in st.session_state.users.items():
        df.append({
            "Username": username,
            "Watch Count": len(user.watchHistory)
        })
    #Sorting users in descending
    df = pd.DataFrame(df, columns = ["Username", "Watch Count"])
    df = df.sort_values(by="Watch Count", ascending=False)
    return pd.DataFrame(df)

#Trending Movies
def trendMovies():
    df = []
    for movies, trendscore in mrs.trendingMovies():
        df.append({
            "Movie Title": movies.movieTitle,
            "Movie Genre": movies.movieGenre,
            "Trend Score": f"{trendscore:.2f}"
        })
    return pd.DataFrame(df)

#Page Title
st.set_page_config(page_title="AI-Based MRS", layout="wide")

#TODO ----- Streamlit Page (Login) -----
if st.session_state.currentPage == "loginPage":
    col1, col2, col3 = st.columns(3)

    with col2:
        st.title("Welcome to the Login Page!")
        st.header("AI-Based Movies Recommendation System")
        st.subheader("Please Login Below")

        #Determine role of user
        username = st.text_input("Enter your Username:", placeholder="Enter username")
        password = st.text_input("Enter your Password:", placeholder="Enter password",
                                type="password")

        if st.button("Login"):
            #Check validity of username & password
            if username in acct:
                if password == acct[username]["password"]:
                    st.session_state.username = username
                    st.session_state.role = acct[username]["role"]
                    st.session_state.loggedIn = True

                    #Determine if login for user or admin
                    if st.session_state.role == "user":
                        if username not in st.session_state.users:
                            st.session_state.users[username] = User(
                                acct[username]["userID"],
                                acct[username]["preferences"]
                            )

                        st.session_state.currentUser = st.session_state.users[username]
                        st.session_state.currentPage = "dashboardUsers"
                    else:
                        st.session_state.currentPage = "dashboardAdmins"

                    st.rerun()
                else:
                    st.error("Incorrect password.")
            else:
                st.error("Username not found.")


#TODO ----- User Dashboard -----
elif st.session_state.currentPage == "dashboardUsers":
    user = st.session_state.currentUser

    st.title("Welcome to the Dashboard")
    st.write("Username: ", st.session_state.username)
    st.write("Role: ", st.session_state.role)
    st.write("Preferences:", ", ".join(user.genrePref))

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Logout"):
            st.session_state.currentPage = "loginPage"
            st.rerun()

    #Show all Available Movies
    st.subheader("All Available Movies")
    st.dataframe(availableMovies(), use_container_width=True)

    #Rating Movies
    st.subheader("Movie Rating")

    #List creation
    movieList = {}

    for movie in mrs.movies:
        movieList[f"{movie.movieID} - {movie.movieTitle}"] = movie.movieID

    col1, col2 = st.columns(2)
    #Select Movie
    with col1:
        moveTitles = st.selectbox("Select movie", list(movieList.keys()))

    #Rate Movies (1 - 5)
    with col2:
        movieRating = st.slider("Select rating", min_value=1, max_value=5, value=3)

    if st.button("Movie Rated"):
        ratedMovieID = movieList[moveTitles]
        ratedMovie = mrs.getMovieID(ratedMovieID)

        if ratedMovie is not None:
            user.watch(ratedMovie)
            user.rating(mrs, ratedMovie, movieRating)
            st.success("Movie Rated Successfully!")

    st.divider()

    #Top N
    st.subheader("Top - N Recommendations")
    nTop = st.number_input("Number of Recommendations", min_value=1, max_value=5, value=5)

    #Recommend Button
    if st.button("Recommend"):
        st.session_state.movieRecommendations = mrs.moviesRec(user)

    #Check for more than 1 recommendations
    if "movieRecommendations" in st.session_state:
        if len(st.session_state.movieRecommendations) > 0:
            st.dataframe(persRecommendations(st.session_state.movieRecommendations), use_container_width=True)
        else:
            st.info("No recommendations available.")

    st.divider()

    #Search Movies
    st.subheader("Search Movies")
    userSearch = st.radio("Select Search Method", ["Title", "Genre"], horizontal= True)

    #User select Title
    if userSearch == "Title":
        title = st.text_input("Enter the Title:", placeholder="Enter here")

        if st.button("Search"):
            if userSearch.strip() == "":
                st.warning("Please enter a valid title.")

            else:
                df = mrs.searchTitles(title)
                if len(df) > 0:
                    st.dataframe(searchMovies(mrs, df), use_container_width=True)

                else:
                    st.error("No movies found.")

    #User selects Genre
    elif userSearch == "Genre":
        genre = []

        for movie in mrs.movies:
            if movie.movieGenre not in genre:
                genre.append(movie.movieGenre)

        #Selecting Genres
        genreSelect = st.selectbox("Select Genre", list(genre))

        if st.button("Search"):
            df = mrs.searchGenres(genreSelect)
            if len(df) > 0:
                st.dataframe(searchMovies(mrs, df), use_container_width=True)

            else:
                st.error("No movies found.")

    st.divider()

    # Top Recommended Movies
    col1, col2 = st.columns(2)

    with col1:
        #Top Recommended Movies
        st.subheader("Top Recommended Movies")
        movieRecommendations = mrs.moviesRec(user)

        if len(movieRecommendations) > 0:
            st.table(persRecommendations(movieRecommendations))

        else:
            st.info("No recommendations available.")

        st.divider()

        #Trending Movies
        st.subheader("Trending Available Movies")
        st.table(trendMovies())

        st.divider()

        #Popular Genres
        st.subheader("Popular Movie Genres")
        popularGenre = mrs.popularGenre()

        if popularGenre is not None:
            st.success(f"The most popular genre is {popularGenre}")

    with col2:
        #User Watch History
        st.subheader("Watch History")

        if len(user.watchHistory) > 0:
            st.table(watchHistory(user))

        else:
            st.error("No watch history found.")

        #Rating Logs
        st.subheader("Rating Logs")
        ratingLogs = ratingTable(user.userID)

        if len(ratingLogs) > 0:
            st.table(ratingLogs)

        else:
            st.error("No rating logs found.")

    st.divider()

    #Insight Display
    col1, col2 = st.columns(2)

    with col1:
        #Highest Rated Movies Graph
        st.subheader("Highest Rated Movies")
        topRatedMovies = []
        for movie in mrs.movies:
            topRatedMovies.append((movie.movieTitle, mrs.AvgMovieRatings(movie)))

        topRatedMovies.sort(key=lambda x: x[1], reverse=True)
        topRatedMovies = topRatedMovies[:5]

        if len(topRatedMovies) > 0:
            titles = [item[0] for item in topRatedMovies]
            ratings = [item[1] for item in topRatedMovies]

            #Plotting Graph
            fig, ax = plt.subplots()
            ax.bar(titles, ratings)
            ax.set_title("Highest Rated Movies")
            ax.set_xlabel("Movie Title")
            ax.set_ylabel("Average Rating")
            plt.xticks(rotation=30)
            st.pyplot(fig)

#TODO ----- Admin Dashboard -----
elif st.session_state.currentPage == "dashboardAdmins":
    user = st.session_state.currentUser

    st.title("Welcome to the Admin Dashboard")
    st.write("Username: ", st.session_state.username)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Logout"):
           st.session_state.currentPage = "loginPage"
           st.rerun()

    st.divider()

    #Admin Management
    st.header("Admin Console")

    #CRUD Actions for Admin
    crud = st.radio("Select Operation", ["Add New Movie", "Update Movie",
                                      "Delete Old Movie"], horizontal= True)

    #Adding New Movie
    if crud == "Add New Movie":
        newMovieID = st.number_input("Enter Movie ID",min_value=100, max_value=10000,step=1)
        newMovieTitle = st.text_input("Enter Movie Title", placeholder= "Enter Movie Title Here")
        newMovieGenre = st.text_input("Enter Movie Genre", placeholder= "Enter Movie Genre Here")
        releaseYear = st.number_input("Enter Movie Release Year", min_value=1995, max_value=2030,step=1)

        #Add Button
        if st.button("Add New Movie"):
            #Making sure to only add new Movies through MovieID
            if mrs.getMovieID(newMovieID) is not None:
                st.error("Movie ID already exists.")

            #Make sure all values are entered
            elif newMovieTitle.strip() == "" or newMovieGenre.strip() == "":
                st.error("Please insert all values.")

            else:
                #Success Message
                mrs.addMovies(Movies(newMovieID, newMovieTitle, newMovieGenre, releaseYear))
                st.success("Movie added!")

    elif crud == "Update Movie":
        updMovieID = st.number_input("Enter Movie ID",min_value=100, max_value=10000,step=1)
        updMovieTitle = st.text_input("Enter Movie Title", placeholder= "Enter Movie Title Here")
        updMovieGenre = st.text_input("Enter Movie Genre", placeholder= "Enter Movie Genre Here")
        updReleaseYear = st.number_input("Enter Movie Release Year", min_value=1995, max_value=2030,step=1)

        #Edit/Update Button
        if st.button("Update Movie"):
            if mrs.getMovieID(updMovieID) is None:
                st.error("Movie doesn't exist.")

            #Make sure all values are entered
            elif updMovieTitle.strip() == "" or updMovieGenre.strip() == "":
                st.warning("Please fill in all fields.")

            #Success Message
            else:
                mrs.updateMovies(updMovieID, updMovieTitle, updMovieGenre, updReleaseYear)
                st.success("Movie updated!")

    elif crud == "Delete Old Movie":
        #Only need these 2 to remove, title and genre are redundant here
        deleteMovieID = st.number_input("Enter Movie ID",min_value=100, max_value=10000,step=1)
        deleteMovieTitle = st.text_input("Enter Movie Title", placeholder= "Enter Movie Title Here")

        #Remove Button
        if st.button("Delete Movie"):
            if mrs.getMovieID(deleteMovieID) is None:
                st.error("Movie doesn't exist.")

            else:
                mrs.deleteMovies(deleteMovieID)
                st.success("Movie deleted!")

    st.divider()

    #The current database for movies after admin CRUD
    st.subheader("Current Movie Database")
    st.dataframe(availableMovies(), use_container_width=True)

    st.divider()

    #Engagement Analytics
    st.header("Engagement Analytics")

    col1, col2 = st.columns(2)

    with col1:
        #Engagement Trend (Most Watched)
        st.subheader("Engagement Trend")
        st.table(mostWatched())

        st.divider()

        #Trending Movie List
        st.subheader("Movie Trend List")
        st.table(trendMovies())

    with col2:
        #Top Active Users
        st.subheader("Top Active Users")
        topActiveUsers = topActive()

        if len(topActiveUsers) > 0:
            st.table(topActiveUsers)

        else:
            st.error("No active users found.")
