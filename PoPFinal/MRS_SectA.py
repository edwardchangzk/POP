#AI-based Movie Recommendation System

#User class
class User:
    def __init__(self,userID, genrePref):
        self.userID = userID
        self.genrePref = genrePref
        self.watchHistory = []

    def watch(self, movie):
        self.watchHistory.append(movie)

    def rating(self, recommendation, movie, rating):
        recommendation.addRatings(self, movie, rating)

#Movies Class
class Movies:
    def __init__(self, movieID, movieTitle, movieGenre):
        self.movieID = movieID
        self.movieTitle = movieTitle
        self.movieGenre = movieGenre

    def getMovieInfo(self):
        return f"Movie Title:{self.movieTitle}, Movie Genre: {self.movieGenre}"

#MRS class
class MRS:
    def __init__(self):
        self.movieRatings = {}
        self.movies = []
        self.userEngagement = {}

    def addMovies(self, movie):
        self.movies.append(movie)

    #Determining Watch Count
    def updUserEngagement(self, user):
        self.userEngagement[user.userID] = len(user.watchHistory)

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

        #Only providing movies User prefers by genre
        for movie in self.movies:
            if movie.movieGenre in user.genrePref:
                avgRating = self.AvgMovieRatings(movie)
                movieRecommendations.append((movie,avgRating))

        #Sorting recommended movies based on rating
        movieRecommendations.sort(key=lambda x: x[1], reverse=True)
        return movieRecommendations

    def engagementPatterns(self):
        print("\n ----- Generating User Engagement Patterns ----- ")

        #Printing User & Movies watched
        for userID, watchedMovies in self.userEngagement.items():
            print(f"User ID: {userID}, Watched Movies: {watchedMovies}")

    #Section A Part C (Identifying Most popular genre)
    def popularGenre(self):
        genreType = {}

        #Identifying which movie belongs to which genre
        for movie in self.movies:
            genreType[movie.movieGenre] = genreType.get(movie.movieGenre, 0) + 1

        #Genre with the highest count
        mostPopularGenre = max(genreType, key=lambda x: genreType[x])
        return mostPopularGenre, genreType[mostPopularGenre]

    #Top 3 most trending movies
    def trendingMovies(self):
        movieAvgRating = []

        for movie in self.movies:
            avgMvRating = self.AvgMovieRatings(movie)
            movieAvgRating.append((movie, avgMvRating))

        #Identifying top 3 movies
        movieAvgRating.sort(key=lambda x: x[1], reverse=True)
        return movieAvgRating[:3]

    #Total watch count per user
    def watchCount(self):
        print("\n ----- Generating User Watch Count ----- ")

        # Printing UserID & total watch count
        for userID, watchcount in self.userEngagement.items():
            print(f"User ID: {userID}, Total Watch Count: {watchcount}")

    def insights(self):
        print("\n ----- Generating Insights ----- ")

        #Printing Average Rating for ALL movies
        for movie in self.movies:
            avgRating = self.AvgMovieRatings(movie)
            print(f"Movie Title: {movie.movieTitle}, Average Rating: {avgRating:.2f}")

        #Printing Most Popular Genres
        print("\n ----- Most Popular Genre -----")
        genreType, genreCount = self.popularGenre()
        print(f"Most Popular Genre: {genreType} with {genreCount} movies")

        #Printing top 3 most trending movies
        print("\n ----- The top 3 Most Trending Movies -----")
        movieTrends = self.trendingMovies()
        for movie, rating in movieTrends:
            print(f"Movie Title: {movie.movieTitle}, Average Rating: {rating:.2f}")

        self.watchCount()

#Admin Class
class Admin:
    def __init__(self, adminID):
        self.adminID = adminID

    def addMovies(self, recommendation, movie):
        recommendation.addMovies(movie)

    def reportGenerate(self, recommendation):
        recommendation.insights()
        recommendation.engagementPatterns()

#Admin Creation
admin = Admin(1)

#Movie Recommendation System Creation
MRS = MRS()

#Movies
movie1 = Movies(101, "Peaky Blinders", "Drama")
movie2 = Movies(202, "KPop Demon Hunters", "Musical")
movie3 = Movies(303, "War Machine", "Action")
movie4 = Movies(404, "Wake Up Dead Man", "Comedy")
movie5 = Movies(505, "Godzilla", "Sci-Fi")
movie6 = Movies(606, "Wallace & Gromit", "Comedy")
movie7 = Movies(707, "Red Notice", "Action")
movie8 = Movies(808, "Bird Box", "Sci-Fi")
movie9 = Movies(909, "The Gray Man", "Action")
movie10 = Movies(1010, "Leave the World Behind", "Sci-Fi")

#Admin adding Movies into MRS
admin.addMovies(MRS, movie1)
admin.addMovies(MRS, movie2)
admin.addMovies(MRS, movie3)
admin.addMovies(MRS, movie4)
admin.addMovies(MRS, movie5)
admin.addMovies(MRS, movie6)
admin.addMovies(MRS, movie7)
admin.addMovies(MRS, movie8)
admin.addMovies(MRS, movie9)
admin.addMovies(MRS, movie10)

#User creation, watching movie & rating
#1st User
Jeff = User(101, ["Comedy", "Sci-Fi"])

#2nd User
Bob = User(102, ["Action", "Drama"])

#3rd User
Anna = User(103, ["Action", "Musical"])

#Users watching movies
Jeff.watch(movie5)
Jeff.watch(movie2)
Jeff.watch(movie8)
Jeff.watch(movie3)
MRS.updUserEngagement(Jeff)

Bob.watch(movie6)
Bob.watch(movie9)
Bob.watch(movie10)
MRS.updUserEngagement(Bob)

Anna.watch(movie1)
Anna.watch(movie7)
Anna.watch(movie3)
Anna.watch(movie4)
MRS.updUserEngagement(Anna)

#User provides rating
Jeff.rating(MRS,movie5, 5)
Jeff.rating(MRS,movie2, 2)
Jeff.rating(MRS,movie8, 4)
Jeff.rating(MRS, movie10, 4)

Bob.rating(MRS,movie6, 3)
Bob.rating(MRS,movie7, 5)
Bob.rating(MRS,movie10, 1)
Bob.rating(MRS, movie2, 2)

Anna.rating(MRS,movie1, 2)
Anna.rating(MRS,movie7, 5)
Anna.rating(MRS,movie3, 4)
Anna.rating(MRS,movie4, 3)

#Preferences gathered, providing movie personal recommendation
jeffRecommendations = MRS.moviesRec(Jeff)
bobRecommendations = MRS.moviesRec(Bob)
annaRecommendations = MRS.moviesRec(Anna)

#Display Available Movies
print("\n ----- Available Movies -----")
for movie in MRS.movies:
    print(movie.getMovieInfo())

print("\n =======================================")
print("Before New Rating and Watching Event")
print("=======================================")

#Displaying Recommendation
print("\n ----- Movie Recommendations -----")

print("Recommended Movies for Jeff")
for movies, rating in jeffRecommendations:
    print(f"Movie: {movies.movieTitle}, Genre: {movies.movieGenre}, Rating: {rating:.2f}")

print("\n Recommended Movies for Bob")
for movies, rating in bobRecommendations:
    print(f"Movie: {movies.movieTitle}, Genre: {movies.movieGenre}, Rating: {rating:.2f}")

print("\n Recommended Movies for Anna")
for movies, rating in annaRecommendations:
    print(f"Movie: {movies.movieTitle}, Genre: {movies.movieGenre}, Rating: {rating:.2f}")

#Admin Report
print("\n ----- Generating Admin Report -----")
admin.reportGenerate(MRS)

print("\n =======================================")
print("After New Rating and Watching Event")
print("=======================================")

#New watching event
Jeff.watch(movie6)
Jeff.watch(movie7)
Jeff.watch(movie3)
MRS.updUserEngagement(Jeff)

Bob.watch(movie1)
Bob.watch(movie2)
Bob.watch(movie9)
MRS.updUserEngagement(Bob)

Anna.watch(movie2)
Anna.watch(movie3)
Anna.watch(movie6)
MRS.updUserEngagement(Anna)

#New Rating
Jeff.rating(MRS,movie6, 5)
Jeff.rating(MRS,movie7, 5)
Jeff.rating(MRS,movie3, 5)

Bob.rating(MRS,movie1, 5)
Bob.rating(MRS,movie2, 5)
Bob.rating(MRS,movie9, 5)

Anna.rating(MRS,movie2, 5)
Anna.rating(MRS,movie3, 5)
Anna.rating(MRS,movie6, 5)

#Preferences gathered, providing movie personal recommendation
jeffRecommendations = MRS.moviesRec(Jeff)
bobRecommendations = MRS.moviesRec(Bob)
annaRecommendations = MRS.moviesRec(Anna)

#Displaying Recommendation
print("\n ----- Movie Recommendations -----")

print("Recommended Movies for Jeff")
for movies, rating in jeffRecommendations:
    print(f"Movie: {movies.movieTitle}, Genre: {movies.movieGenre}, Rating: {rating:.2f}")

print("\n Recommended Movies for Bob")
for movies, rating in bobRecommendations:
    print(f"Movie: {movies.movieTitle}, Genre: {movies.movieGenre}, Rating: {rating:.2f}")

print("\n Recommended Movies for Anna")
for movies, rating in annaRecommendations:
    print(f"Movie: {movies.movieTitle}, Genre: {movies.movieGenre}, Rating: {rating:.2f}")

#Admin Report
print("\n ----- Generating Admin Report -----")
admin.reportGenerate(MRS)












