import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_OR_ALL = (('january', 'february', 'march', 'april', 'may', 'june'))

DAYS_OF_WEEK =(('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'))

def get_filters():
    valid = False
    """
    Asks user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). 
    # HINT: Use a while loop to handle invalid inputs
    while valid == False:
      city = str(input("Enter Chicago, New York City, or Washington: \n"))  
      try:
          if type(city) == str:
              city = city.lower()
              if city in CITY_DATA:
                  valid = True
      except (ValueError):
          print("Woops! That's not a valid selection. Try again!\n")

    # get user input for month (all, january, february, ... , june)
    valid = False
    while valid == False:
      month = str(input("Enter a Month\n January, February, March,\n April, May, June,\n or enter All:\n"))  
      try:
          if type(month) == str:
              month = month.lower()
              if month in MONTH_OR_ALL or month == 'all':
                  valid = True
      except (ValueError):
          print("Woops! That's not a valid selection. Try again!\n")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid = False
    while valid == False:
      day = str(input("Enter a Day\n Monday, Tuesday, Wednesday,\n Thursday, Friday, Saturday, Sunday,\n or enter All:\n"))  
      try:
          if type(day) == str:
              day = day.lower()
              if day in DAYS_OF_WEEK or day == 'all':
                  valid = True
      except (ValueError):
          print("Woops! That's not a valid selection. Try again!\n")

    print('-'*40)
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month']= df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # From Practice Solution #3
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    # For extracting the hour
    df['hour'] = df['Start Time'].dt.hour
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    frequent_month = df['month'].mode()[0]
    print('Month most frequented:', frequent_month)

    # display the most common day of week
    frequent_day = df['day_of_week'].mode()[0]
    print('Day most frequented:', frequent_day)
    
    # display the most common start hour
    frequent_hour = df['hour'].mode()[0]
    print('Hour most frequented:', frequent_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print("Most popular start station: ", popular_start)
    
    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print("Most popular end station: ", popular_end)

    # display most frequent combination of start station and end station trip
    frequent_combo = (df['Start Station']+','+df['End Station']).mode()[0]
    print("Most popular route based on stations: ", frequent_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    trip_duration = df['Trip Duration'].sum()
    print('Trip Duration: ',trip_duration,' in seconds or ',trip_duration/3600,'hours')

    # display mean travel time
    mean = df['Trip Duration'].mean()
    print('Average (mean) of the trip: ',mean,'in seconds or ',mean/3600,'hours')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counting user types: \n',df['User Type'].value_counts());

    # Display counts of gender
    if 'Gender' in df:
        print('Count by gender: \n',df['Gender'].value_counts());

    # Display earliest, most recent, and most common year of birth
    if 'Birth day' in df:
        earliest_bd = int(df['Birth day'].min())
        print('\n Earliest Birth Day :\n ',earliest_bd)
        recent_bd =int(df['Birth day'].max())
        print('\n Recent Birth Day :\n ',recent_bd)
        common_bd =int(df['Birth day'].mode()[0])
        print('\n Most Common Birth Year:\n ', common_bd)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_output(df):
    valid = False
    raw_data = 0
    
    while valid == False and raw_data+5<df.shape[0]:
        if raw_data > 0:
            raw_req = str(input('Would you like to continue viewing raw data?. Enter yes or no: \n'))
        else:
            raw_req = str(input('Do you wish to view the raw data?. Enter yes or no: \n'))
        raw_req = raw_req.lower()
        
        if raw_req == 'yes':
            print (df.iloc[raw_data:raw_data+5])
            raw_data += 5
        
        if raw_req == 'no':
            valid = True
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        raw_output(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
