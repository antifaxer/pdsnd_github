import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

#For extra aesthetics, I used time.sleep() throughout the code to make the program look a little retro and interactive. These aren't necessary for the code to work properly.

print("\nBooting\n")
time.sleep(0.25)
print(".")
time.sleep(0.25)
print(".")
time.sleep(0.25)
print(".")
time.sleep(0.25)


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # GET user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    # .keys() turned out to be pretty helpful. With this, python goes through every object in the dictionary.

    #This while loop has not in. Since we haven't given the machine an input for city yet, it will execute the print statement directly below. This method is used also for selecting the month and day
    city = ''
    while city not in CITY_DATA.keys():

        print("\nThis is Bikeshare Data Analyzer (BDA) VER 1.1.4")

        time.sleep(3)

        city = input("Please type one of the following cities: chicago, new york or washington.\n").lower()

        #Now that we gave city a value, we run an if statement to check if whatever was used as input matches the .keys() inside CITY_DATA

        if city not in CITY_DATA.keys():
            print("\nInvalid input, please try again\n")

    print(("\nLoading {} data, please wait").format(city))
    time.sleep(1)
    # GET user input for month (all, january, february, ... , june)
    months = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all':7}

    month = ''

    while month not in months.keys():

        time.sleep(2)

        month = input(("\nSpecify the desired month from january to june to analyze on your selected city, {}. You can also use the option \'all\' to select every month \n \n").format(city)).lower()

        if month not in months.keys():
            print("\nPlease try again with any given month from january to june, or all\n")

    # GET user input for day of week (all, monday, tuesday, ... sunday)
    day_lst = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

    day = ''

    while day not in day_lst:
        time.sleep(2)
        day = input(("\nSpecify the day of the week. You may type any day from monday through sunday, or every day by typing in all \n \n").format(month, city)).lower()

        if day not in day_lst:
            print("\nPlease try again with any given day of the week, or select all")

    print('-'*50)

    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print("\nPlease wait, loading data\n")
    time.sleep(0.5)
    print(".")
    time.sleep(0.5)
    print(".")
    time.sleep(0.5)
    print(".")
    time.sleep(0.5)

    #WE GOT city, month and day from our filters. Now we load the data from CITY_DATA based on these.
    df = pd.read_csv(CITY_DATA[city])

    #Converting Start Time column to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extracting month and day to create new columns
    df['month'] = df['Start Time'].dt.month

    df['day_week'] = df['Start Time'].dt.day_name()

    #Filtering by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    #Filtering by day
    if day != 'all':
        df = df[df['day_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nLoading Travel Time Data for further calculations')
    time.sleep(0.5)
    print(".")
    time.sleep(0.5)
    print(".")
    time.sleep(0.5)
    print(".")
    time.sleep(0.5)

    start_time = time.time()

    # display the most common month
    month = df['month']
    popular_month = df['month'].mode()[0]
    print(('\nThe most popular month is {}').format(popular_month))

    # display the most common day of week
    popular_day = df['day_week'].mode()[0]
    print(('\nThe most popular day is {}').format(popular_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(("\nThe most common start hour is {} hrs").format(popular_hour))


    print("\nCalculations took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nLoading Trip and Station Data')
    time.sleep(0.5)
    print(".")
    time.sleep(0.5)
    print(".")
    time.sleep(0.5)
    print(".")
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print(("\nThe most common start station is {}\n").format(common_start))

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print(("\nThe most common end station is {}\n").format(common_end))

    # display most frequent combination of start station and end station trip
    df['freq_comb'] = df['Start Station'] + " " + "to " + df['End Station']
    freq_common_combo = df['freq_comb'].mode()[0]
    print('\nThe most frequent combination of start station and end station trip is: \n', freq_common_combo)

    print("\nCalculations took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""


    print('\nCalculating Trip Duration')
    time.sleep(0.5)
    print(".")
    time.sleep(0.5)
    print(".")
    time.sleep(0.5)
    print(".")
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()

    def conversion(seconds):
        if total_time >= 86400:
            seconds = total_time % (24*86400)
            days = seconds //86400
            seconds %= 86400
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60

            return "%02d:%02d:%02d:%02d" % (days, hour, minutes, seconds)

        else:
            seconds = total_time % (24*3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds //60
            seconds %= 60

            return "%02d:%02d:%02d" % (hour, minutes, seconds)

    # display mean travel time
    avg_time = round(df['Trip Duration'].mean())

    def conversion2(seconds):
        seconds = avg_time % (24*3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds //60
        seconds %= 60

        return "%02d:%02d:%02d" % (hour, minutes, seconds)

    print('\nThe total travel time of all the bikes in the company in the selected time frame, given in days, hours, minutes and seconds is: ', conversion(total_time))

    print('\nThe average travel time of all the bikes in the company in the selected time frame, given in hours, minutes and seconds is: ', conversion2(avg_time))

    print("\nCalculations took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nLoading User Stats Data')
    time.sleep(0.5)
    print(".")
    time.sleep(0.5)
    print(".")
    time.sleep(0.5)
    print(".")
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nThis is the count of every user type: \n')
    print(user_types)

    # Display counts of gender
    try:
        user_genders = df['Gender'].value_counts()
        print("\nThis is the amount of users by genders:\n", user_genders)

    except:
        print("\nA gender column could not be found in specified city file")

    # Display earliest, most recent, and most common year of birth
    try:
        oldest_guy = str(df['Birth Year'].min())
        youngest_guy = str(df['Birth Year'].max())
        coordinated_pregnancies = str(df['Birth Year'].mode())
        print("\nThe oldest user/s were born in: ", oldest_guy)
        print("\nThe youngest user/s were born in: ", youngest_guy)
        print("\nThe most common birth year among our customers is: ",coordinated_pregnancies)

    except:
        print("\nA birth year column could not be found in specified city file")

    print("\nCalculations took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_data(df):

    counter = 0

    answers = ['yes', 'no']

    showme = ''

    while showme not in answers:
        print("\nShow resulting dataframes? (yes or no)")

        showme = input().lower()

        if showme == 'yes':
            print(df.head())

        elif showme not in answers:
            print("\nInvalid input, please use either yes or no")

    while showme == 'yes':
        print("\nShow 10 more rows of the DataFrame?\n")

        counter += 10

        showme = input().lower()

        if showme == 'yes':
            print(df[counter:counter+10])

        else:
            break

    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
